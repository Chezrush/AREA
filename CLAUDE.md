# Projet AREA (G-YEP-500) : consignes pour Claude

Une suite logicielle d'automatisation, inspirée d'IFTTT et Zapier. Elle comprend un **serveur d'application**, un **client web** et un **client mobile Android**. L'utilisateur s'abonne à des Services et compose des workflows : une Action détectée par un hook déclenche une ou plusieurs REActions, avec au plus une condition. Projet à trois.

Le rôle demandé est celui d'un **architecte logiciel** : comprendre le besoin, comparer des options, décider, intégrer des briques existantes, prouver les choix par des PoC et les défendre. Le code écrit par l'équipe est la colle métier entre ces briques. Ce qui rend le projet difficile n'est pas de relier deux API. C'est d'assembler un produit qui tourne seul, survit à ses propres pannes et peut être repris par quelqu'un d'autre.

Sujet complet, à relire en cas de doute plutôt que supposer :

- `area-project.pdf` : socle commun, exigences techniques, jalons, livrables ;
- `area-additional_features.pdf` : catalogue des fonctionnalités additionnelles et leurs critères d'acceptation ;
- `area-security_evidence.pdf` : modèle de preuve pour chaque fonctionnalité `SEC-*` retenue.

## À compléter par le groupe

- Membres : gigabyteZ390, Chezrush, R0GW1N (M = 3)
- Prochain jalon : **Plan** (date exacte sur My). À mettre à jour après chaque jalon : la skill `verif-jalon` s'en sert.
- Nom du produit : _à définir_
- Stack : _à définir_ par trois comparatifs (front-end, back-end, persistance), un ADR chacun
- Fonctionnalités du catalogue retenues (D ≥ 6) : _à définir_, avec leur responsable
- Question d'architecture de chaque membre : _à définir_
- Langue de la documentation : **français**, partout. Les deux clients, eux, doivent être utilisables dans au moins deux langues.
- Droits GitHub : le groupe n'est **pas administrateur** du dépôt. Pas de protection de branche, ni de secrets, ni d'environnements configurables par nous. GitHub Actions est bloqué sur les dépôts de l'organisation (facturation), comme sur le projet pro : la CI/CD s'exécutera sur un **miroir privé** synchronisé par le NAS, et ses résultats reviendront comme statuts de commit (à décrire dans un ADR). On travaille toujours sur le dépôt principal, jamais sur le miroir.
- Commandes (build, lancement Docker Compose, tests, lint) : _à définir avec la stack_

## Socle commun (non négociable)

- **Comptes** : création et confirmation de compte, authentification locale (identifiant + mot de passe) **et** par un fournisseur d'identité externe en **OIDC**. OIDC dit *qui* est l'utilisateur. OAuth 2.0 dit *ce que* le produit peut faire pour lui chez un Service. On ne mélange pas les deux.
- **Accès délégué** : quand un Service doit agir plus tard pour l'utilisateur, on utilise son mécanisme d'autorisation (souvent OAuth 2.0) et on stocke les identifiants délégués nécessaires aux hooks. Le lien entre identités externes et comptes locaux, et le cycle de vie des jetons, sont documentés.
- **Services, Actions, REActions** : chaque Service offre au moins deux composants. Le catalogue est déclaré par le serveur et exposé aux clients par un **endpoint de découverte lisible par machine** (`about.json` ou équivalent), documenté et versionné. Les clients ne codent jamais le catalogue en dur.
- **Workflows** : un nœud déclencheur (l'Action), des nœuds réaction, et au plus un nœud condition à deux successeurs. La chaîne normale est linéaire, il n'y a pas de condition imbriquée, et les branches se terminent sans se rejoindre. Un AREA (1 Action → 1 REAction) est le plus petit workflow valide. Le modèle de données **ne fixe pas** quatre comme maximum, mais le moteur doit démontrer un workflow utile à au moins quatre réactions. La validité structurelle est vérifiée **à l'enregistrement**.
- **Données entre nœuds** : chaque type de nœud déclare les clés qu'il publie (`{{ trigger.subject }}`, `{{ node_2.file_id }}`). Une référence hors déclaration est refusée à l'enregistrement. Une valeur manquante à l'exécution est traitée de façon déterministe, selon le modèle documenté. La substitution remplace des données et **n'évalue jamais de code fourni par l'utilisateur**.
- **Hooks** : ils détectent les Actions et lancent les workflows sans qu'aucun client soit ouvert. Ils ne traitent jamais la même occurrence comme un nouvel événement. L'identification, la planification et la persistance des événements font l'objet d'un ADR.
- **Builder** : uniquement sur le web (nœuds et mapping des données). Le mobile liste les workflows, les active ou désactive et montre ce qu'ils ont fait. Il ne construit pas de workflow.
- **Quantités** (calculées sur le client **le moins complet**) : S ≥ 4 services, dont au moins la moitié via OAuth2 ; A + R ≥ 8 ; D ≥ 6 points du catalogue. Une fonctionnalité inachevée ne compte pas. Un service ajouté seulement pour faire du chiffre ne vaut rien : chaque connecteur et chaque workflow doit répondre à un vrai besoin.

## Principes d'architecture

- **Le serveur porte toute la logique métier.** Les clients s'occupent de la présentation et de l'interaction. Pas de framework full-stack qui brouille cette frontière.
- **Le contrat OpenAPI fait foi** entre clients et serveur. Il est servi par le serveur avec une interface navigable et couvre **chaque endpoint appelé par les clients, réponses d'erreur comprises**. Un test échoue quand l'implémentation et la description divergent. Tout nouvel endpoint ou changement de réponse met à jour la description dans la même PR.
- **Logique métier isolée derrière des abstractions** : un nouveau Service, une nouvelle Action ou un nouveau type de nœud s'ajoutent sans toucher au moteur.
- **Jamais de confiance dans le client** : chaque entrée est validée côté serveur, chaque nouvelle règle a son test.
- **Pannes** : un Service tiers lent ou en erreur ne bloque pas le reste. La sémantique d'échec des workflows est documentée.
- **Secrets** : jetons tiers et mots de passe ne sont jamais journalisés ni renvoyés aux clients.
- **Construction reproductible** : tout le produit se construit et se lance avec Docker Compose. Serveur et client web sont accessibles en local, et un APK Android installable est produit. Le client mobile permet de configurer l'adresse du serveur.
- **Une décision peut changer** quand une preuve l'invalide, à condition de documenter le changement, sa raison et son coût (nouvel ADR qui remplace l'ancien).

## Accessibilité (WCAG AA) et internationalisation, dès l'écriture du code

- Les deux clients visent WCAG niveau AA. Un rapport d'audit est commité : ce qui a été mesuré, avec quel outil, sur quels écrans, ce qui a été corrigé et ce qui ne l'a pas été, avec la raison.
- Web : HTML sémantique, titres hiérarchisés, libellé sur chaque champ, contraste ≥ 4,5:1, information jamais portée par la seule couleur, erreurs explicites liées au champ avec une suggestion. Le builder est utilisable au clavier.
- Android : libellé accessible (`contentDescription` ou équivalent du framework) sur chaque contrôle, cibles ≥ 48 dp, compatibilité TalkBack et respect de la taille de police du système.
- Au moins deux langues sur tout le parcours principal, de l'inscription à la création d'un AREA. Aucun texte affiché codé en dur hors des fichiers de traduction.

## Workflow Git et GitHub

- **Claude ne fait jamais `git commit` ni `git push`.** Il prépare les fichiers, puis indique les fichiers à ajouter et le message de commit. Ce sont les membres qui commitent et poussent.
- Une tâche = une issue (responsable, labels `type:*` et `area:*`, milestone, statut dans le Project AREA) → une branche `<type>/<N>-<description>` → une pull request liée (`Closes #N`) → relue par un autre membre → merge. `main` n'est pas protégée : jamais de push direct, et jamais de merge tant que les checks ne sont pas verts. C'est à nous de le faire respecter.
- Commits au format Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `refactor:`, `chore:`…).
- Aucun secret dans le dépôt ni dans l'historique. Toute nouvelle variable d'environnement est ajoutée et documentée dans `.env.example`, avec une valeur inoffensive.
- Lockfiles commités, `.gitignore` à jour, pas de code mort ni de fichier orphelin.
- La CI (lint, tests, build) tourne sur chaque contribution. Ne jamais désactiver un test, ajouter un `skip` ou couper une règle de lint pour la faire passer : corriger la cause, ou le signaler.
- Changement notable → entrée dans `CHANGELOG.md`. Versions taguées en semver à chaque jalon.
- Le travail est réparti équitablement : chaque membre doit pouvoir défendre une décision d'architecture à laquelle il a contribué.

## Documentation

La doc fait partie du livrable et s'écrit avec le code, dans la même PR, dans `/docs` en Markdown :

- `README.md` : installation, fonctionnement, API publique, commandes et endpoints ou artefacts obtenus ;
- `HOWTOCONTRIBUTE.md` : comment ajouter un Service, une Action, une REAction ou un type de nœud ;
- modèle de workflow et sémantique d'échec, modèle de persistance et structures de données importantes ;
- choix d'architecture → nouvel ADR dans `docs/adr/` (contexte, vraies alternatives, choix, conséquences). Une option écartée l'est *pour ce projet*, pas parce qu'elle serait mauvaise en général ;
- fonctionnalités du catalogue : où chaque critère d'acceptation s'observe. Chaque `SEC-*` a sa fiche de preuve selon `area-security_evidence.pdf` : scénario, reproduction, observation, protection, vérification, limites.

Un document n'est une preuve que si ses affirmations se démontrent en direct : l'évaluateur peut en choisir une et demander la démonstration. N'écrire que ce qui est vrai et reproductible.

## Usage de l'IA (charte IONIS)

- Le README contient une section qui déclare les outils d'IA utilisés et pour quoi. Quand Claude contribue de façon notable à une PR, on met à jour cette section dans la même PR, ou on le propose.
- Le code et les contenus générés suivent exactement les mêmes règles que le reste : tests, revue en PR, propreté, sécurité.
- La défense est individuelle : Claude explique ses propositions et leurs compromis, pour que chaque membre puisse défendre la décision lui-même.

## Skills du projet

- `/issue` : transforme un besoin, un bug ou une tâche en issue GitHub avec responsable, labels, milestone et statut dans le Project AREA. Elle s'appelle uniquement par la commande slash et ne crée rien sans validation explicite.
- `verif-jalon` : état des lieux du dépôt par rapport au sujet, pour Plan, MVP ou Final Product.
- `a11y-area` : accessibilité WCAG AA du client web et du client Android. Couvre la conception, l'audit, les corrections et le rapport d'audit exigé.
