import cluster from 'node:cluster';
import { serve } from '@hono/node-server';
import { Hono } from 'hono';

const PUNCTUATION_RE = /[^\w\s]/g;
const WHITESPACE_RE = /\s+/g;

interface SimilarityRequest {
  text1: string;
  text2: string;
}

function normalizeText(text: string): string {
  const lower = text.toLowerCase();
  const noPunct = lower.replace(PUNCTUATION_RE, '');
  const clean = noPunct.replace(WHITESPACE_RE, ' ');
  return clean.trim();
}

function generateFrequencyMap(words: string[]): Map<string, number> {
  const freq = new Map<string, number>();
  for (const word of words) {
    freq.set(word, (freq.get(word) ?? 0) + 1);
  }
  return freq;
}

function calculateTf(unique: string[], fm: Map<string, number>, total: number): number[] {
  if (total === 0) return unique.map(() => 0);
  return unique.map((w) => (fm.get(w) ?? 0) / total);
}

function calculateIdf(
  unique: string[],
  fm1: Map<string, number>,
  fm2: Map<string, number>,
): number[] {
  return unique.map((w) => {
    const df = (fm1.has(w) ? 1 : 0) + (fm2.has(w) ? 1 : 0);
    return Math.log(1.0 + 2.0 / (df + 1.0));
  });
}

function calculateTfIdf(tf: number[], idf: number[]): number[] {
  return tf.map((v, i) => v * idf[i]);
}

function calculateSimilarity(a: number[], b: number[]): number {
  let dot = 0;
  for (let i = 0; i < a.length; i++) dot += a[i] * b[i];

  let mag1 = 0;
  for (const v of a) mag1 += v * v;
  mag1 = Math.sqrt(mag1);

  let mag2 = 0;
  for (const v of b) mag2 += v * v;
  mag2 = Math.sqrt(mag2);

  if (mag1 <= 1e-9 || mag2 <= 1e-9) return 0;
  return dot / (mag1 * mag2);
}

function interpretSimilarity(s: number): string {
  if (s <= 0.2) return 'Dissimilar';
  if (s <= 0.4) return 'Slightly Similar';
  if (s <= 0.6) return 'Moderately Similar';
  if (s <= 0.8) return 'Quite Similar';
  if (s <= 1) return 'Highly Similar';
  return 'Unknown';
}

function startServer(): void {
  const app = new Hono();

  app.get('/health', (c) => c.text('ok'));

  app.post('/similarity', async (c) => {
    const { text1, text2 } = await c.req.json<SimilarityRequest>();

    const t1 = normalizeText(text1);
    const t2 = normalizeText(text2);

    const words1 = t1.split(' ');
    const words2 = t2.split(' ');

    const fm1 = generateFrequencyMap(words1);
    const fm2 = generateFrequencyMap(words2);

    const unique = [...new Set([...fm1.keys(), ...fm2.keys()])];

    const tf1 = calculateTf(unique, fm1, words1.length);
    const tf2 = calculateTf(unique, fm2, words2.length);

    const idf = calculateIdf(unique, fm1, fm2);

    const tfidf1 = calculateTfIdf(tf1, idf);
    const tfidf2 = calculateTfIdf(tf2, idf);

    let similarity = calculateSimilarity(tfidf1, tfidf2);
    similarity = Math.round(similarity * 1000) / 1000;

    return c.json({ similarity, interpretation: interpretSimilarity(similarity) });
  });

  serve({ fetch: app.fetch, port: 8080, hostname: '0.0.0.0' });
}

// Node runs JS on a single thread. To use several cores (like Go/Rust do by
// default, and like Python's multi-worker setup), we fork one cluster worker
// per core; cluster shares the listening socket across workers.
const workers = parseInt(process.env.WEB_CONCURRENCY ?? '1', 10);

if (cluster.isPrimary && workers > 1) {
  for (let i = 0; i < workers; i++) cluster.fork();
} else {
  startServer();
}
