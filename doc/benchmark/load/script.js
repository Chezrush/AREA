import http from 'k6/http';
import { check } from 'k6';
import { SharedArray } from 'k6/data';

// Texts loaded once and shared across all virtual users.
const texts = new SharedArray('texts', function () {
    return JSON.parse(open('/load/data.json'));
});

const SERVICE_URL = __ENV.SERVICE_URL;
const SERVICE = __ENV.SERVICE || 'unknown';

// Load profile — identical for every language so results are comparable.
// Shortened vs the original article (which ran 8 min up to 800 VUs) to keep the
// total run reasonable; what matters is that all three use the SAME profile.
export const options = {
    stages: [
        { duration: '15s', target: 50 },
        { duration: '30s', target: 50 },
        { duration: '15s', target: 100 },
        { duration: '30s', target: 100 },
        { duration: '15s', target: 200 },
        { duration: '45s', target: 200 },
        { duration: '15s', target: 0 },
    ],
    thresholds: {
        http_req_failed: ['rate<0.01'],
        http_req_duration: ['p(95)<1500'],
    },
};

export default function () {
    const text1 = texts[Math.floor(Math.random() * texts.length)];
    const text2 = texts[Math.floor(Math.random() * texts.length)];

    const payload = JSON.stringify({ text1: text1, text2: text2 });
    const params = {
        headers: { 'Content-Type': 'application/json' },
        tags: { service: SERVICE },
    };

    const response = http.post(SERVICE_URL, payload, params);
    check(response, {
        OK: (r) => r.status === 200,
        'Similarity Returned': (r) => {
            try {
                return typeof JSON.parse(r.body).similarity === 'number';
            } catch (e) {
                return false;
            }
        },
    });
}

export function handleSummary(data) {
    const out = {};
    out[`/results/${SERVICE}.json`] = JSON.stringify(data, null, 2);
    out['stdout'] =
        `\n=== ${SERVICE} ===\n` +
        `reqs=${data.metrics.http_reqs.values.count} ` +
        `rps=${data.metrics.http_reqs.values.rate.toFixed(1)} ` +
        `fail_rate=${data.metrics.http_req_failed.values.rate}\n` +
        `avg=${data.metrics.http_req_duration.values.avg.toFixed(2)}ms ` +
        `med=${data.metrics.http_req_duration.values.med.toFixed(2)}ms ` +
        `p90=${data.metrics.http_req_duration.values['p(90)'].toFixed(2)}ms ` +
        `p95=${data.metrics.http_req_duration.values['p(95)'].toFixed(2)}ms\n`;
    return out;
}
