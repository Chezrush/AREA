# Choix de la technologie serveur : Go vs Rust vs Python vs TypeScript

> **Projet AREA — Étape 1 : Architecture & choix des technologies**
> Document de décision pour le serveur applicatif (application server).
> Date : 2026-11-25

---

## 1. Contexte et objectif

Le projet **AREA** nécessite un **serveur applicatif** exposant une API REST : gestion
des utilisateurs, des *services* (OAuth tiers), des **Actions / REActions**, et un
*trigger engine* qui interroge régulièrement les services externes pour déclencher les
réactions. Ce composant doit être :

- **performant** et capable de tenir une charge concurrente (nombreux workers/polling en
  parallèle) ;
- **fiable** sous charge (pas d'effondrement de latence, pas d'erreurs) ;
- **maintenable** par une équipe d'étudiants, dans le temps imparti du projet.

Quatre langages couramment utilisés pour les services web ont été envisagés : **Go**,
**Rust**, **Python** et **TypeScript**. Ce document les compare, s'appuie d'abord sur un
benchmark public (état de l'art, Go vs Rust), puis sur **notre propre benchmark
reproductible** mesuré sur une seule machine, et justifie enfin la décision.

> **Décision retenue : Go.** La justification complète est en [section 7](#7-décision-et-justification).

> ⚠️ **Deux sources de chiffres — à ne pas confondre.**
> 1. **[Section 5] Chiffres d'un article externe** (Dmytro Misik, Medium, déc. 2024),
>    comparant Go et Rust. Ils **ne sont pas produits par notre équipe**, ont été mesurés
>    sur la machine de l'auteur, et servent d'**état de l'art** — à étayer la décision, pas
>    à la prouver.
> 2. **[Section 6] Notre benchmark reproductible**, où nous avons réimplémenté le **même
>    service dans les quatre langages** (Go, Rust, Python, TypeScript) et les avons testés
>    **sur la même machine** (Apple M2 Max), via Docker + k6. C'est la **preuve pratique (Proof of
>    Concept)** reproductible exigée par le sujet (« un document n'est une preuve que si ses
>    affirmations peuvent être défendues ou reproduites »). Code : [`benchmark/`](benchmark/).
>
> Les chiffres des deux sources **ne sont pas comparables entre eux** (machines
> différentes) : chacun n'est valable qu'en interne.

---

## 2. Vue d'ensemble des quatre candidats

| Critère | **Go** | **Rust** | **Python** | **TypeScript** (Node) |
|---|---|---|---|---|
| Paradigme mémoire | Garbage Collector (GC) | Ownership / Borrow checker, pas de GC | GC (comptage de références) | GC (V8) |
| Concurrence | Goroutines + channels (natif, léger) | `async`/`await` (runtime Tokio) | `asyncio` mono-cœur (**GIL**) ; multi-process pour le CPU | *event loop* mono-thread ; `cluster`/`worker_threads` pour le CPU |
| Multi-cœurs (CPU) | Natif (goroutines) | Natif (worker/cœur) | **Non** sur 1 process (GIL) → N workers | **Non** sur 1 process → N workers (cluster) |
| Typage | Statique (compilé) | Statique (compilé, strict) | Dynamique (hints optionnels) | Statique à l'écriture, effacé à l'exécution (JS) |
| Courbe d'apprentissage | Douce, syntaxe minimale | Raide (ownership, lifetimes) | Très douce | Douce (familier web) |
| Vitesse de compilation | Très rapide | Lente | Interprété | Transpilation rapide (interprété) |
| Perf brute (CPU) | Très bonne | Excellente (proche du C/C++) | Faible par process | Moyenne (JIT V8), bonne pour du JS |
| Sécurité mémoire | GC + runtime | Garantie à la compilation (zero-cost) | GC + runtime | GC + runtime |
| Écosystème web | Mûr (net/http, Fiber, Gin, Echo…) | En croissance (Actix-web, Axum…) | Très mûr (FastAPI, Django, Flask) | Très riche (Hono, Express, Fastify, Nest) |
| Empreinte mémoire | Faible | Très faible | Élevée (× nb de workers) | Élevée (× nb de workers) |
| Productivité équipe | Élevée | Plus faible au démarrage | Très élevée | Très élevée (même langage que le front) |

**Go** privilégie la **simplicité et la productivité** (cloud-native, microservices).
**Rust** privilégie la **sécurité et la performance** via des abstractions à coût nul, avec
**Actix-web**. **Python** (FastAPI) privilégie la **vitesse de développement** mais son
**GIL** impose du multi-process pour le CPU. **TypeScript** (ici **Hono** sur Node) partage
le **langage du front**, avec un typage statique à l'écriture ; comme Node est mono-thread,
il faut aussi du **cluster** multi-process pour exploiter plusieurs cœurs.

---

## 3. Le benchmark de référence

La comparaison chiffrée s'appuie sur l'article de **Dmytro Misik**,
*« Go vs. Rust: Web Service Performance — Which Handles Heavy Traffic Better? »*
(Medium, 6 déc. 2024).

- Article : https://medium.com/@dmytro.misik/go-vs-rust-web-service-performance-7fb10bbf9a9f
- Code source complet : https://github.com/misikdmytro/text-similarity

### 3.1 Méthodologie

On implémente **le même service web CPU-intensif** dans les deux langages, puis on le
soumet à une charge identique.

- **Service testé** : comparaison de similarité entre deux textes.
- **Algorithmes** : **TF-IDF** (Term Frequency-Inverse Document Frequency) pour vectoriser
  les textes, puis **Cosine Similarity** pour mesurer la proximité des deux vecteurs
  (1 = identiques, 0 = totalement différents).
- **Endpoint** : `POST /similarity`, corps JSON `{ "text1": "...", "text2": "..." }`,
  réponse `{ "similarity": <float>, "interpretation": "<label>" }`.
- **Pourquoi ce choix** : la tâche est **gourmande en CPU** (normalisation regex,
  construction de maps de fréquence, produits scalaires), ce qui met en évidence les
  différences de performance brute entre les deux runtimes plutôt que les I/O.
- **Outil de charge** : **k6**, test de **8 minutes** montant par paliers de **100 → 800
  utilisateurs virtuels (VU)** concurrents, avec des paires de textes tirées
  aléatoirement d'un CSV.
- **Frameworks** : **Actix-web** côté Rust, **Fiber** côté Go.
- **Déploiement** : chaque service est containerisé (image distroless pour Rust, Alpine
  pour Go).

### 3.2 Scénario de charge k6

Le test k6 de l'article tire aléatoirement des paires de textes depuis un CSV et les
envoie en `POST` sur `/similarity`, avec une montée en charge par paliers de **100 à 800
VUs sur 8 minutes** (seuils : taux d'échec < 1 %, p95 < 1500 ms).

> Notre version adaptée de ce scénario (paliers plus courts, données en JSON, URL de service
> paramétrable) est dans [`benchmark/load/script.js`](benchmark/load/script.js).

---

## 4. Implémentations (code dans `benchmark/`)

Le même service (normalisation du texte, maps de fréquence, **TF-IDF** puis **similarité
cosinus**) est réimplémenté à l'identique dans chaque langage. **Le code n'est pas recopié
ici** : il est versionné dans [`benchmark/services/`](benchmark/services/) et exécutable tel
quel (voir [`benchmark/README.md`](benchmark/README.md)).

| Langage | Framework | Source | Image |
|---|---|---|---|
| Rust | Actix-web | [`services/rust/src/main.rs`](benchmark/services/rust/src/main.rs) | [`Dockerfile`](benchmark/services/rust/Dockerfile) |
| Go | Fiber | [`services/go/main.go`](benchmark/services/go/main.go) | [`Dockerfile`](benchmark/services/go/Dockerfile) |
| Python | FastAPI + uvicorn | [`services/python/app.py`](benchmark/services/python/app.py) | [`Dockerfile`](benchmark/services/python/Dockerfile) |
| TypeScript | Hono (Node) | [`services/ts/src/index.ts`](benchmark/services/ts/src/index.ts) | [`Dockerfile`](benchmark/services/ts/Dockerfile) |

Notes de déploiement :

- **Rust** : build `cargo --release`, image finale *distroless*.
- **Go** : `CGO_ENABLED=0` → binaire statique, image *Alpine*.
- **Python** : lancé via **uvicorn** avec **un worker par cœur** (le GIL empêche un seul
  processus d'utiliser plusieurs cœurs pour du calcul).
- **TypeScript** : **Hono** sur **Node**, avec le module **cluster** (un worker par cœur —
  même raison : Node exécute le JS sur un seul thread).
### 4.1 Lecture comparée du code

- **Lignes de code quasi identiques** dans les quatre langages, mais le Rust impose de gérer
  explicitement *ownership*, *lifetimes* (`<'a>`), `HashSet`, `unwrap()` et le pattern
  matching exhaustif — là où Go (`map[string]int`, `for range`), Python (duck typing) et
  TypeScript restent directs.
- Parsing du corps : Go via `c.BodyParser`, Rust via `serde` + `web::Json`, Python via
  **Pydantic** (validation à l'exécution), TypeScript via `c.req.json()` de **Hono**.
- **Typage** : Rust et Go le vérifient à la **compilation** ; **TypeScript** est typé à
  l'écriture mais s'exécute en JS non typé ; **Python** est dynamique.
- **Binaire vs interprété** : Go et Rust produisent un **binaire natif** ; Python (uvicorn)
  et TypeScript/Node (cluster) restent interprétés et montent en charge via du multi-process.

---

## 5. Résultats de l'article (état de l'art — Go vs Rust)

> ⚠️ **Chiffres repris de l'article de Dmytro Misik** (voir [section 3](#3-le-benchmark-de-référence)),
> mesurés sur sa machine, test de 8 min jusqu'à 800 VUs. Ils ne sont **pas issus d'une
> mesure de notre équipe**. À considérer comme un repère d'**état de l'art** ; notre propre
> mesure reproductible (les quatre langages) est en [section 6](#6-notre-benchmark-reproductible-4-langages).

### 5.1 Chiffres bruts

| Métrique | **Rust (Actix-web)** | **Go (Fiber)** |
|---|---:|---:|
| Requêtes totales | 1 865 618 | 960 483 |
| Échecs | 13 (~0,00 %) | 0 (100 % succès) |
| **Débit (req/s)** | **3 887** | **2 001** |
| Latence moyenne | 90,77 ms | 177,35 ms |
| Latence médiane (p50) | 74,79 ms | **22,28 ms** |
| p90 | 161,71 ms | 651,66 ms |
| p95 | 219,01 ms | 905,77 ms |
| Données envoyées | 38 GB | 19 GB |
| Données reçues | 310 MB | 159 MB |

### 5.2 Analyse

- **Débit** : Rust traite **~1,9× plus de requêtes** que Go sur la même durée
  (3 887 vs 2 001 req/s).
- **Latence** : Rust est plus régulier (moyenne et queue p95 bien plus basses). Fait
  intéressant, **Go a une médiane plus basse** (22,28 ms vs 74,79 ms) : la majorité des
  requêtes Go sont très rapides, mais la **queue de distribution explose** sous forte
  charge (p95 ≈ 906 ms), signe d'une variabilité plus forte.
- **Fiabilité** : les deux sont excellents. Go a un taux de succès **parfait (100 %)**,
  Rust 99,99 % (13 échecs sur ~1,87 M).

### 5.3 Lecture critique (limites du benchmark)

Pour une décision d'architecture honnête, il faut relativiser ces chiffres (plusieurs
points soulevés en commentaires de l'article, et pertinents) :

1. **La « resource utilization » est trompeuse.** Rust a envoyé 2× plus de données
   simplement parce qu'il a traité 2× plus de requêtes — ce n'est **pas** un surcoût
   réseau par requête, juste une conséquence du débit.
2. **Le GC de Go explique probablement la queue de latence.** La forte dégradation du
   p95 de Go pointe vers les pauses du *Garbage Collector* sous charge. Des optimisations
   existent (réduire les allocations sur le tas, réutiliser les buffers, `sync.Pool`) et
   réduiraient sensiblement cet écart — le code benchmarké n'est pas optimisé.
3. **Benchmark d'une tâche purement CPU.** AREA est surtout un service **I/O-bound**
   (appels réseau aux API tierces, base de données, polling). Sur ce profil, l'écart de
   performance brute entre Go et Rust est **beaucoup moins déterminant**.
4. **Chiffres non reproduits par nous.** Les résultats viennent d'un article tiers,
   mesurés sur une machine inconnue. Le sujet AREA exige qu'une preuve soit
   **reproductible** → c'est précisément l'objet de la [section 6](#6-notre-benchmark-reproductible-4-langages),
   où nous rejouons le test **des quatre langages sur une seule et même machine**. En
   l'état, les chiffres de l'article
   restent un repère d'état de l'art, utile pour la décision mais pas une preuve pratique.

---

## 6. Notre benchmark reproductible (4 langages)

> ✅ **Preuve pratique produite par notre équipe.** Nous avons réimplémenté le **même
> service** (TF-IDF + cosinus) dans les **quatre langages**, puis lancé un test de charge
> **k6 identique** contre chacun, **sur la même machine**, les services tournant **un à la
> fois** (pas de contention CPU → comparaison interne valide). Tout est reproductible via
> [`benchmark/run.sh`](benchmark/run.sh) (`cd doc/benchmark && ./run.sh`).

### 6.1 Conditions de mesure

- **Machine** : Apple **M2 Max, 12 cœurs**, conteneurs Docker (OrbStack).
- **Charge k6** : profil commun aux quatre, paliers 50 → 100 → 200 VUs (~2 min 45),
  volontairement **plus court** que l'article (c'est l'**égalité des conditions** entre
  langages qui compte, pas la durée).
- **Config** : Go (goroutines) et Rust (Actix, worker/cœur) utilisent les 12 cœurs par
  défaut ; **Python = uvicorn avec 12 workers** (un par cœur) pour contourner le GIL ;
  **TypeScript = Node + cluster, 12 workers** (même raison : Node est mono-thread).
- **Jeu de données** : 80 textes synthétiques, paires tirées aléatoirement.

### 6.2 Résultats bruts

| Métrique | **Rust / Actix** | **TypeScript / Hono** (12 w.) | **Python / FastAPI** (12 w.) | **Go / Fiber** |
|---|---:|---:|---:|---:|
| Requêtes totales | 10 782 249 | 7 837 495 | 3 913 233 | 3 660 333 |
| Échecs | **0** | **0** | **0** | **0** |
| **Débit (req/s)** | **65 344** | **47 499** | **23 716** | **22 183** |
| Latence moyenne | 1,00 ms | 1,62 ms | 4,69 ms | 5,04 ms |
| Latence médiane (p50) | 0,52 ms | 0,93 ms | 3,81 ms | 0,69 ms |
| p90 | 2,51 ms | 3,85 ms | 9,44 ms | 18,21 ms |
| p95 | 3,51 ms | 5,32 ms | 11,48 ms | 29,83 ms |
| Latence max | 30,0 ms | 157,7 ms | 69,0 ms | 201,7 ms |
| **Mémoire pic (conteneur)** | **15 MiB** | 2 395 MiB | 513 MiB | 46 MiB |

*(Colonnes triées par débit décroissant.)*

### 6.3 Analyse

- **Rust domine** : ~**65 000 req/s**, latences les plus basses à **tous** les percentiles,
  et de loin la plus petite empreinte mémoire (**15 MiB**). Confirme le classement de
  l'article (Rust > Go).
- **Surprise : TypeScript/Hono est 2ᵉ** (**47 500 req/s**, soit **~2× Go**), avec
  d'excellentes latences (p95 5,3 ms). Le JIT de V8 est très efficace sur ce type de travail
  (chaînes + nombres), et le mode **cluster** exploite les 12 cœurs. **Mais** cela coûte
  **≈ 2,4 Go de RAM** (12 process Node), soit **~52× la mémoire de Go**.
- **Go ≈ Python en débit brut** (22,2k vs 23,7k) — à assumer honnêtement. Go a une
  **excellente médiane** (0,69 ms) mais une **queue de latence longue** (p95 **29,8 ms**,
  max **202 ms**) : c'est la **signature des pauses du Garbage Collector** sous charge,
  exactement la critique formulée en commentaire de l'article. Python est plus régulier ici
  mais plus lent au centre (p50 3,81 ms).
- **Le vrai discriminant est la mémoire par débit.** Go obtient ~22k req/s pour **46 MiB** ;
  Python ~24k req/s pour **513 MiB** (**~11×**) ; TypeScript ~47k req/s pour **2 395 MiB**
  (**~52×**). Rust est imbattable sur les deux axes. Python et TS paient cher le
  multi-process qui contourne leur modèle mono-thread.
- **Fiabilité** : **0 échec** pour les quatre sur plusieurs millions de requêtes.

### 6.4 Limites (à défendre)

- **Micro-benchmark CPU** à textes courts : une bonne part du coût est le HTTP/JSON, ce qui
  avantage les runtimes au HTTP optimisé (Hono/V8) et ne reflète pas le profil **I/O-bound**
  réel d'AREA.
- Chiffres liés à la machine (M2 Max) et à Docker ; **non comparables** à ceux de l'article
  (section 5). Ils ne valent **que les uns par rapport aux autres**.
- Python et TypeScript sont mesurés dans leur **meilleure** config (12 workers) ; en
  **1 worker** ils seraient plusieurs fois plus lents sur cette tâche CPU.
- TypeScript est testé sur **Node** ; **Bun** ou **Deno** donneraient des chiffres différents
  (souvent meilleurs). Le résultat dépend donc aussi du **runtime**, pas seulement de Hono.

---

## 7. Décision et justification

> ### ✅ Technologie serveur retenue : **Go**

Le choix se fait entre **quatre** candidats sérieux. Nos mesures (section 6) montrent que
**Rust est le plus rapide et le plus léger**, que **TypeScript/Hono est étonnamment rapide**
mais **très gourmand en mémoire**, et que **Go et Python** se tiennent en débit — Go
l'emportant nettement sur la **mémoire**. Pour *ce* projet, Go offre le meilleur compromis.

### Pourquoi Go pour AREA

1. **Performance « suffisante et fiable ».** Dans notre benchmark, Go tient **22 000 req/s**
   avec **0 échec** sur une tâche CPU-intensive — bien au-delà des besoins réels d'AREA,
   qui n'a pas de contrainte de latence à la milliseconde.
2. **Profil I/O-bound.** Le cœur d'AREA (polling des services, webhooks, DB, OAuth) est
   dominé par les I/O réseau, où l'avantage brut de Rust s'estompe. Les **goroutines**
   de Go gèrent des milliers de connexions/tâches concurrentes avec un modèle simple —
   **sans** le coût mémoire du multi-process de Python ou Node.
3. **Empreinte mémoire décisive.** 46 MiB, contre **513 MiB** (Python) et **2 395 MiB**
   (TypeScript/Node) à débit comparable ou supérieur. Pour une stack **Docker Compose
   multi-conteneurs** (serveur + DB + reverse proxy…) tournant sur une machine de dev ou un
   petit VPS, c'est l'argument le plus concret : **~11× moins** que Python, **~52× moins**
   que Node.
4. **Typage statique compilé.** Comme Rust et TypeScript (et contrairement à Python), Go est
   typé — un atout pour un **contrat d'API OpenAPI** partagé entre le serveur et les clients
   développés en parallèle.
5. **Productivité & déploiement.** Simplicité proche de Python, mais **binaire statique
   unique** (`CGO_ENABLED=0`) trivial à conteneuriser, compilation rapide, tooling standard
   (`go fmt`, `go test`, `go vet`). La courbe de Rust coûterait trop de temps sur un projet
   scolaire contraint.

### Pourquoi pas Rust / Python / TypeScript

- **Rust** reste imbattable en **perf/mémoire** (3× plus rapide, 3× plus léger que Go), mais
  ce n'est pas le besoin d'AREA (I/O-bound), et sa **courbe d'apprentissage** (ownership,
  lifetimes, borrow checker) est trop coûteuse pour le calendrier.
- **TypeScript/Hono** est un **vrai concurrent** : ~2× le débit de Go, typé, et il partage
  le **langage du front** (web client en TS) — argument de productivité réel. Mais son
  empreinte mémoire (**~2,4 Go** en cluster 12 workers) est rédhibitoire pour notre stack
  multi-conteneurs, et le sujet **décourage de brouiller la frontière client/serveur** et
  valorise l'élargissement des compétences — un back-end Go impose une séparation nette.
- **Python/FastAPI** offre la meilleure vélocité de dev et un écosystème immense, mais le
  **GIL** force le multi-process (mémoire ~11× Go), avec un typage dynamique moins sûr pour
  un contrat d'API strict.

### Synthèse

| Priorité | Classement |
|---|---|
| Vitesse brute / débit max | **Rust** > TypeScript > Python ≈ Go |
| Latence régulière sous charge | **Rust** > TypeScript > Python > Go (queue GC) |
| Empreinte mémoire | **Rust** (15 Mo) > **Go** (46) ≫ Python (513) ≫ TS (2 395) |
| Vitesse de développement | **Python** ≈ **TypeScript** ≈ **Go** |
| Langage partagé avec le front | **TypeScript** |
| Fiabilité « out of the box » | **Égalité** (0 échec partout) |
| Concurrence I/O à faible mémoire | **Go** (goroutines) |
| Typage / contrat d'API robuste | **Rust** ≈ **Go** ≈ **TypeScript** |
| **Adéquation globale au besoin AREA** | **Go** |

Pour le profil d'AREA — un service **I/O-bound** à livrer **vite**, **en équipe**, avec une
**faible empreinte mémoire** et un **typage sûr** — **Go est le meilleur compromis** :
presque aussi simple que Python/TS, bien plus léger, et assez performant là où Rust serait
du sur-mesure coûteux.

> **Note sécurité (exigée par le sujet).** Sur la sûreté mémoire : Rust la garantit à la
> compilation (pas de *data race*) ; Go, Python et TypeScript s'appuient sur un GC +
> runtime. Les quatre évitent les classes de bugs du C/C++. Un comparatif sécurité plus
> complet (gestion des dépendances/CVE, surface d'attaque, gestion des secrets) reste à
> détailler — voir les features `SEC-*` du sujet.

---

## 8. Références

- Dmytro Misik, *Go vs. Rust: Web Service Performance* — Medium, 6 déc. 2024 :
  https://medium.com/@dmytro.misik/go-vs-rust-web-service-performance-7fb10bbf9a9f
- Code source de l'article : https://github.com/misikdmytro/text-similarity
- **Notre benchmark reproductible** : [`benchmark/`](benchmark/) (voir `benchmark/README.md`)
- Fiber (framework web Go) : https://gofiber.io
- Actix-web (framework web Rust) : https://actix.rs
- FastAPI (framework web Python) : https://fastapi.tiangolo.com
- Uvicorn (serveur ASGI) : https://www.uvicorn.org
- Hono (framework web TypeScript) : https://hono.dev
- Node.js `cluster` : https://nodejs.org/api/cluster.html
- k6 (outil de test de charge) : https://k6.io
