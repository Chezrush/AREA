# Benchmark back-end : Go vs Rust vs Python vs TypeScript

Preuve pratique (*Proof of Concept*) accompagnant le document de choix technologique
[`../choix-techno-serveur.md`](../choix-techno-serveur.md). Le même micro-service
(comparaison de similarité de deux textes via **TF-IDF + Cosine Similarity**) est
implémenté dans les quatre langages, puis soumis à **une charge identique sur la même
machine**, afin d'obtenir des chiffres **comparables et reproductibles** (ce que le sujet
AREA exige d'une preuve).

## Arborescence

```
benchmark/
├── run.sh                  # orchestrateur : build + run + k6 + mémoire, un service à la fois
├── services/
│   ├── go/                 # Fiber (Go 1.23)
│   ├── rust/               # Actix-web (Rust, build --release)
│   ├── python/             # FastAPI + uvicorn (Python 3.13)
│   └── ts/                 # Hono + cluster (Node 22, via tsx)
├── load/
│   ├── script.js           # scénario k6 (profil de charge commun aux 4)
│   └── data.json           # 80 textes synthétiques, tirés aléatoirement par paires
└── results/                # sorties k6 (JSON) + mémoire pic, générées par run.sh
```

## Prérequis

- **Docker** (testé avec OrbStack). Go, Rust et k6 **n'ont pas besoin** d'être installés
  sur l'hôte : tout passe par des conteneurs.

## Lancer

```bash
cd doc/benchmark
./run.sh            # les quatre langages
./run.sh go ts      # un sous-ensemble
```

Pour chaque service, `run.sh` :
1. construit l'image Docker ;
2. démarre le conteneur et attend `/health` ;
3. échantillonne la mémoire du conteneur (`docker stats`) pendant le test ;
4. lance **k6** (conteneur `grafana/k6`) avec le même `load/script.js` ;
5. écrit le résumé dans `results/<lang>.json` et le pic mémoire dans `results/<lang>.mem.json`.

## Méthodologie & équité

- **Services lancés un par un** : pas de contention CPU entre eux, chacun dispose de
  toute la machine → comparaison interne valide.
- **Profil de charge identique** pour les quatre (défini dans `script.js`). Il est
  volontairement **plus court** que celui de l'article d'origine (8 min jusqu'à 800 VUs)
  pour garder une durée totale raisonnable ; ce qui compte est qu'il soit **le même**
  pour les quatre langages.
- **Configuration multi-cœurs** : Go (goroutines) et Rust (Actix, un worker/cœur)
  utilisent tous les cœurs par défaut. **Python** (GIL) et **TypeScript/Node** (mono-thread)
  ne peuvent pas utiliser plusieurs cœurs dans un seul processus pour du calcul : on lance
  donc **un worker par cœur** (`WEB_CONCURRENCY = nproc`) — uvicorn pour Python, le module
  `cluster` pour Node — afin de leur donner leur meilleure configuration réaliste. En un
  seul worker, ils seraient environ N fois plus lents sur cette tâche CPU (au prix d'une
  mémoire bien plus élevée en multi-worker).

## Limites (à défendre honnêtement)

- Les chiffres dépendent de la machine de test (ici **Apple M2 Max, 12 cœurs**) et de
  Docker Desktop/OrbStack ; ils ne sont **pas** directement comparables à ceux de
  l'article d'origine (machine différente). Ils ne valent que **les uns par rapport aux
  autres**.
- Micro-benchmark **CPU-bound** : il ne modélise pas le profil réel d'AREA, majoritairement
  **I/O-bound** (appels réseau, base de données). À lire comme un indicateur, pas comme
  une vérité absolue.
