# Grille de vérification AREA

Chaque item indique **à partir de quel jalon** il est attendu : P (Plan), M (MVP), F (Final Product). Un item « continu » doit rester vrai à chaque jalon.

La stack n'est pas imposée. Adapte les commandes au dépôt, et commence par repérer l'arborescence : `git ls-files | head -100`.

## Sommaire

- [Q. Quantités](#q-quantités)
- [CB. Socle commun fonctionnel](#cb-socle-commun-fonctionnel)
- [T. Exigences techniques](#t-exigences-techniques)
- [F. Fichiers et documentation](#f-fichiers-et-documentation)
- [G. Méthode : Project, issues, PR, historique](#g-méthode--project-issues-pr-historique)
- [C. CI/CD](#c-cicd)
- [K. Catalogue de fonctionnalités](#k-catalogue-de-fonctionnalités)
- [P. Jalon Plan](#p-jalon-plan)
- [M. Jalon MVP](#m-jalon-mvp)
- [FP. Jalon Final Product](#fp-jalon-final-product)

---

## Q. Quantités

Dès M (en progression), exigées à F. M = nombre de membres = 3. Le calcul se fait sur le client **le moins complet** : un service présent sur le web mais absent du mobile ne compte pas.

| ID | Seuil | Vérifier |
| --- | --- | --- |
| Q1 | S ≥ 1 + M = 4 services, dont au moins la moitié via OAuth2 | Lire l'endpoint de découverte (`about.json`) avec la stack lancée, puis vérifier dans chaque client que le service est vraiment utilisable |
| Q2 | A + R ≥ 2M + 2 = 8 | Idem, en comptant Actions et REActions disponibles **dans les deux clients** |
| Q3 | D ≥ 2M = 6 points | Somme des catégories des fonctionnalités du catalogue **entièrement livrées** (section K) |

Un service ou une Action sans cas d'usage concret : ⚠️ (« Quality » quantity »), à signaler.

## CB. Socle commun fonctionnel

**CB1. Comptes** (M) : inscription, confirmation de compte, connexion locale, connexion OIDC par un fournisseur externe. Tests sur les chemins d'échec (mauvais mot de passe, compte non confirmé).

**CB2. Accès délégué** (M) : abonnement à un Service par son mécanisme d'autorisation (OAuth 2.0), stockage des identifiants délégués, rafraîchissement des jetons. Le lien identité externe ↔ compte local et le cycle de vie des jetons sont documentés.

**CB3. Services** (M) : chaque Service offre au moins deux composants (Actions ou REActions).

**CB4. Workflows : modèle** (M) : trigger, réactions, au plus une condition à deux successeurs, sans imbrication ni fusion de branches. Le modèle n'encode **pas** de maximum de quatre réactions (chercher une constante 4 ou un tableau de taille fixe). Validation structurelle **à l'enregistrement**, avec tests des cas refusés. Les décisions non spécifiées (branche vide valide ou non…) sont documentées.

**CB5. Données entre nœuds** (M) : chaque type de nœud déclare ses clés publiées ; une référence hors déclaration est refusée à l'enregistrement (test) ; valeur manquante à l'exécution traitée selon le modèle documenté ; la substitution **n'évalue jamais de code** (chercher `eval`, `Function(`, moteurs de templates à expressions).

**CB6. Hooks** (M) : lancent les workflows sans client ouvert ; une même occurrence n'est pas retraitée (déduplication persistée, testée). ADR sur l'identification, la planification et la persistance des événements.

**CB7. Builder web** (M, complet à F) : nœuds et mapping des données édités depuis le web ; forme justifiée (ADR ou doc).

**CB8. Mobile** (M) : liste les workflows, les active ou désactive, montre ce qu'ils ont fait ; ne construit pas de workflow ; adresse du serveur configurable.

**CB9. Workflow à quatre réactions** (F) : un workflow utile avec au moins quatre nœuds réaction, démontrable.

## T. Exigences techniques

**T1. Frontière clients / serveur** (P, continu) : la logique métier est sur le serveur. Pas de framework full-stack ; s'il y en a un, ⚠️ avec justification attendue.

**T2. OpenAPI** (M, complet à F) : servie par le serveur avec une interface navigable ; couvre chaque endpoint appelé par les clients, **réponses d'erreur comprises** ; un test échoue quand implémentation et description divergent. Comparer les routes déclarées dans le serveur avec les chemins de la description, et les appels des clients avec la description.

**T3. Découverte des services** (M) : endpoint lisible par machine (identifiants, descriptions, paramètres), schéma documenté et versionné, cohérent avec ce que les clients proposent. Chercher un catalogue codé en dur côté client : ❌.

**T4. Docker Compose** (M) : `docker compose up --build` construit et lance tout ; serveur et client web accessibles en local ; un APK Android installable est produit. Commandes et endpoints documentés dans le README.

**T5. Navigateurs et Android** (F) : le web fonctionne sur les navigateurs courants ; le mobile cible Android.

**T6. Accessibilité** (F, à concevoir dès M) : WCAG AA sur les deux clients ; rapport d'audit commité (mesures, outils, écrans, corrections, non-corrigés et pourquoi). Voir la skill `a11y-area`.

**T7. Internationalisation** (F, à concevoir dès M) : au moins deux langues sur tout le parcours inscription → création d'un AREA, dans les deux clients. Chercher des chaînes affichées codées en dur hors des fichiers de traduction.

**T8. Secrets** (continu) : aucun `.env` réel suivi (`git ls-files | grep -E '(^|/)\.env($|\.)' | grep -v example`) ; recherche dans l'historique (`gitleaks git .` s'il est installé) ; aucun jeton tiers dans les logs ou les réponses d'API.

## F. Fichiers et documentation

| ID | Élément | Dès | Vérifier |
| --- | --- | --- | --- |
| F1 | `README.md` | P | Installation, fonctionnement, **API publique**, commandes, endpoints et artefacts obtenus, section « Usage de l'IA » |
| F2 | `HOWTOCONTRIBUTE.md` | M | Procédure reproductible pour ajouter un Service, une Action, une REAction et un type de nœud |
| F3 | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE` | P | Présents |
| F4 | `CHANGELOG.md` | P | Présent **et vivant** : `git log -1 --format=%cs -- CHANGELOG.md` contre `git log -1 --format=%cs` |
| F5 | `.github/` | P | Modèles d'issue et de PR |
| F6 | `.env.example` | P | Chaque variable lue dans le code y figure, commentée, avec une valeur inoffensive |
| F7 | `.gitignore` | P | Aucun fichier de dépendances, de build ou d'éditeur suivi |
| F8 | Doc technique | M | Modèle de workflow et **sémantique d'échec** ; modèle de persistance et structures de données |
| F9 | ADR | P | `docs/adr/` : contexte, vraies alternatives, décision, conséquences, date, statut, remplacements chaînés |
| F10 | Catalogue documenté | M | Pour chaque fonctionnalité retenue : où chaque critère d'acceptation s'observe |
| F11 | Preuves `SEC-*` | M | Une fiche par fonctionnalité `SEC-*`, au format de `area-security_evidence.pdf` : scénario, reproduction, observation, protection, vérification, limites |

## G. Méthode : Project, issues, PR, historique

**G1. Project tenu à jour** (P, continu) : `gh project item-list 678 --owner EpitechPGE3-2026 --format json --limit 300`. Issue fermée encore « In progress » : ⚠️.

**G2. Tâches complètes** (P) : chaque issue a un responsable, des labels, une milestone et ses dépendances (« Bloquée par #N »). `gh issue list --state all --limit 300 --json number,title,assignees,labels,milestone,body`.

**G3. PR liées et relues** (continu) : `gh pr list --state merged --limit 100 --json number,author,closingIssuesReferences,reviews`. PR sans issue, sans relecture ou auto-approuvée : ⚠️. Commits directs sur `main` (`git log --first-parent main --no-merges`) : ⚠️.

**G4. Répartition** (continu) : `git shortlog -sne --no-merges` et responsables des issues. Le sujet exige une répartition équitable : un fort déséquilibre est ⚠️, à signaler sans juger.

**G5. Conventional Commits et tags semver** (continu) : ratio de messages non conformes ; au moins un tag par jalon passé.

## C. CI/CD

**C1. Automatisations sur chaque contribution** (M) : lint, tests et build ; un échec est visible sur la contribution (statut de commit ou check dans la PR). GitHub Actions est bloqué sur le dépôt principal : vérifier les statuts reçus par les derniers commits (`gh api repos/{owner}/{repo}/commits/<sha>/statuses`).

**C2. Déploiement sans étape manuelle** (F).

**C3. État réel** : branche principale rouge depuis longtemps : ⚠️.

## K. Catalogue de fonctionnalités

Pour chaque fonctionnalité retenue (lister depuis le `CLAUDE.md`, la doc ou les issues) :

1. Recopier ses critères d'acceptation depuis `area-additional_features.pdf`.
2. Pour chaque critère, chercher la preuve observable (test, commande, écran, document démontrable).
3. Statut de la fonctionnalité : ✅ seulement si **tous** les critères sont observables. Sinon elle ne compte pas dans D.

Rappels du sujet : sélection décidée au Plan, modifiable **une seule fois** au MVP, puis gelée. Au MVP, au moins un tiers des points doit être observablement avancé. Dépendances : AI-EVAL exige AI-NODE.

## P. Jalon Plan

**P1. Trois comparatifs** : front-end, back-end, persistance. Chacun compare plusieurs technologies sur des critères pertinents, **sécurité comprise**, documente la comparaison et conclut par un choix justifié, appuyé par une preuve pratique (code exploratoire, PoC commité ou lié).

**P2. Sélection du catalogue** : D ≥ 6, justification d'apprentissage (contre les faiblesses du groupe, plusieurs domaines si possible), responsable par fonctionnalité.

**P3. Une question d'architecture par membre**, identifiée et documentée.

**P4. Découpage complet** : socle commun, catalogue, documentation, vérification et échéance du MVP ; chaque tâche actionnable, planifiée, assignée, avec dépendances (G1, G2).

**P5. Méthode de gestion et outils** choisis et justifiés.

**P6. Chaque membre a participé à l'exploration** (historique, PoC, comparatifs).

## M. Jalon MVP

**M1.** Produit déployable de façon reproductible (T4).

**M2.** Workflow de bout en bout : trigger, au moins deux réactions, une condition.

**M3.** Première doc technique de l'architecture centrale (F8).

**M4.** Plan mis à jour, avec une analyse écrite des changements : preuve qui a causé chaque changement et son coût.

**M5.** Au moins un tiers des points du catalogue observablement avancés ; sélection éventuellement révisée (dernière occasion).

**M6.** Tests sur les comportements importants ; CI sur chaque contribution (C1) ; OpenAPI servie et couvrant les endpoints du MVP (T2).

## FP. Jalon Final Product

**FP1.** Produit complet, tout le catalogue retenu livré (K).

**FP2.** README et HOWTOCONTRIBUTE à jour ; quelqu'un d'extérieur peut construire et lancer le projet en suivant la doc (le tester depuis un clone neuf si possible).

**FP3.** Rapport d'audit d'accessibilité honnête pour les deux clients (T6).

**FP4.** Artefacts de planning finaux, reflétant ce qui s'est réellement passé.

**FP5.** Post-mortem : réussites, échecs, changements, preuves qui ont fait changer d'avis, ce qu'on referait autrement, leçons des expériences ratées, fonctionnalités plus dures que prévu.

**FP6.** Soutenance : démo en direct, workflow à au moins quatre réactions (CB9), **enregistrement de secours** pour les démos qui dépendent de tiers peu fiables, chaque membre défend une décision d'architecture à laquelle il a contribué (besoin, alternatives, preuves, décision, compromis, résultat observé).

**FP7.** Tests unitaires et fonctionnels sur les chemins de succès et d'échec importants ; tests de contrat OpenAPI.

**FP8.** Clients responsives, visuellement cohérents, navigation intuitive ; hooks autonomes ; logique métier isolée derrière des abstractions.
