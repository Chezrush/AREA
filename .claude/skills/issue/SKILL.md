---
name: issue
description: Transformer une idée, un besoin, un bug ou une tâche technique du projet AREA en issue GitHub conforme au sujet (responsable, labels, milestone, statut dans le GitHub Project AREA, dépendances). Vérifie les doublons. Création uniquement après validation explicite.
argument-hint: "[idée, besoin ou problème]"
disable-model-invocation: true
---

# Issue : de l'idée à l'issue GitHub

## Rôle

Aider un membre du groupe à transformer une idée, une fonctionnalité, un bug ou une tâche technique en **issue GitHub** claire et actionnable, rattachée au **GitHub Project « AREA »**.

Cette skill sert uniquement à planifier et à créer des issues. **Ne jamais écrire de code, créer de branche, commiter, ouvrir de PR ni modifier les fichiers du dépôt.**

Communiquer en français.

## Contexte fixe

- Dépôt : `Chezrush/AREA`
- GitHub Project : `AREA` (n° 678, organisation `EpitechPGE3-2026`). Il appartient à l'organisation Epitech mais accepte les issues de `Chezrush/AREA`. C'est le seul outil de suivi. Le livrable du jalon Plan exige un découpage où **chaque tâche est actionnable, planifiée, assignée et a ses dépendances identifiées**.
- Groupe : `gigabyteZ390`, `Chezrush`, `R0GW1N`. Le sujet demande une répartition équitable : signaler si les issues se concentrent sur une seule personne.
- Sujet : serveur d'application, client web et client mobile Android pour composer des workflows (Action → REActions, une condition au plus). Les PDF sont à la racine (`area-project.pdf`, `area-additional_features.pdf`, `area-security_evidence.pdf`).

### Exigences transverses, à rappeler dans les critères d'acceptation quand elles s'appliquent

- **Contrat OpenAPI** : tout endpoint ajouté ou modifié est décrit, réponses d'erreur comprises, et le test de contrat passe.
- **Catalogue** : un nouveau Service, une nouvelle Action ou REAction apparaît dans l'endpoint de découverte, sans catalogue codé en dur côté client.
- **Les deux clients** : une fonctionnalité visible est comptée sur le client le moins complet. Préciser si l'issue couvre le web, le mobile ou les deux, ou créer deux issues.
- **Accessibilité WCAG AA** pour toute interface, et **i18n** (au moins deux langues) sur le parcours principal.
- **Sécurité** : validation côté serveur, aucun jeton tiers dans les logs ni dans les réponses. Pour une fonctionnalité `SEC-*`, une fiche de preuve au format de `area-security_evidence.pdf`.
- **Tests** : succès et échec de la logique touchée.
- **Documentation** : README, HOWTOCONTRIBUTE, doc technique ou ADR selon le cas.
- **Fonctionnalité du catalogue** : recopier ses critères d'acceptation depuis `area-additional_features.pdf` (`pdftotext -layout area-additional_features.pdf -`), sans les reformuler. Une fonctionnalité n'est livrée que si **tous** ses critères s'observent.

## Prérequis (à vérifier au début)

1. `gh auth status` doit montrer les scopes `repo` et `project`. Sinon, demander à l'utilisateur de lancer `gh auth refresh -s project` (commande interactive : il la lance lui-même).
2. Charger les labels (`gh label list`), les milestones (`gh api repos/{owner}/{repo}/milestones`) et les champs du Project (`gh project field-list 678 --owner EpitechPGE3-2026 --format json`).

Ne pas créer de label, de milestone ou de champ manquant sans accord explicite.

## Taxonomie

### Labels

Mettre **un label de type** et **au moins un label de zone** :

| Type | Usage |
| --- | --- |
| `type:feature` | Nouvelle fonctionnalité |
| `type:bug` | Comportement incorrect |
| `type:chore` | Outillage, configuration, dépendances, CI/CD |
| `type:docs` | Documentation uniquement |
| `type:test` | Tests uniquement |

| Zone | Périmètre |
| --- | --- |
| `area:server` | Serveur d'application : API HTTP, logique métier, persistance |
| `area:web` | Client web, dont le builder de workflows |
| `area:mobile` | Client mobile Android |
| `area:engine` | Moteur de workflows, nœuds, données entre nœuds, hooks |
| `area:services` | Services, Actions et REActions (connecteurs) |
| `area:auth` | Comptes locaux, OIDC, OAuth 2.0 des services |
| `area:api` | Contrat OpenAPI et description des services (`about.json`) |
| `area:security` | Sécurité et preuves des fonctionnalités `SEC-*` |
| `area:a11y` | Accessibilité WCAG AA et rapport d'audit |
| `area:i18n` | Internationalisation des deux clients |
| `area:ci-cd` | Pipeline, Docker Compose, déploiement |
| `area:planning` | Pilotage : comparatifs de technos, planning, post-mortem |
| `area:tooling` | Outillage du dépôt : modèles, conventions, Claude Code |

### Milestones (jalons du sujet)

| Milestone | Échéance | Attendu |
| --- | --- | --- |
| `Plan` | début + 1 semaine | 3 comparatifs (front, back, persistance) avec PoC, sélection du catalogue avec responsables, une question d'architecture par membre, découpage complet des tâches, méthode et outils |
| `MVP` | début + 4 semaines | Produit déployable de façon reproductible, workflow trigger + 2 réactions + 1 condition, première doc technique, plan mis à jour, au moins un tiers des points du catalogue avancés, CI sur chaque contribution, OpenAPI servie |
| `Final Product` | fin du projet | Produit complet avec tout le catalogue, README + HOWTOCONTRIBUTE, audit a11y, post-mortem, soutenance avec un workflow à 4 réactions |

Les échéances exactes sont sur My et dans les milestones GitHub. Choisir la milestone d'après le contenu de l'issue **et** la date du jour. Ne pas affecter une milestone déjà passée sans le signaler.

### Statut dans le Project

Créer les issues avec le statut `Backlog`, ou `Ready` si l'utilisateur dit qu'elles sont prêtes à démarrer. Utiliser les valeurs réelles renvoyées par `gh project field-list`.

## Phase 1 : Comprendre la demande

Déterminer :

- le problème à résoudre et pour qui (utilisateur final, membre du groupe, évaluateur) ;
- le résultat attendu, observable ;
- la partie du produit concernée (serveur, web, mobile, moteur, service) ;
- les contraintes et cas limites (jeton expiré, Service tiers indisponible, événement déjà traité, valeur manquante…) ;
- ce qui est explicitement hors périmètre.

Ne poser de questions que si la réponse change le contenu de l'issue. Ne pas inventer de décision d'architecture : présenter les options et laisser le groupe trancher, puis proposer une issue d'ADR si la décision le mérite.

## Phase 2 : Contexte et doublons

- Lire `CLAUDE.md`, les ADR (`docs/adr/`) et le code concerné, de façon ciblée.
- Chercher les doublons : `gh issue list --state all --search "<mots-clés>"`.
- Si une issue existante couvre déjà la demande, proposer de la compléter plutôt que d'en créer une nouvelle.

## Phase 3 : Découpage

Une issue donne **un résultat vérifiable** et correspond à **une PR**. Si la demande est trop large, proposer un découpage en plusieurs issues avec leurs dépendances (« Bloquée par #N »), en séparant serveur, web et mobile quand des personnes différentes les prennent. Ne rien créer avant validation du découpage.

## Phase 4 : Rédiger le brouillon

Suivre le modèle d'issue du dépôt (`.github/ISSUE_TEMPLATE/`) qui correspond au type. Afficher aussi les métadonnées proposées :

- **responsable** : demander lequel des trois membres s'il n'est pas évident, par défaut `@me` ;
- **labels** ;
- **milestone** ;
- **statut** ;
- **dépendances**.

## Phase 5 : Validation

Attendre un **« ok » explicite**. Intégrer les modifications demandées, et représenter le brouillon si elles sont importantes.

## Phase 6 : Création

`gh issue create --project` ne fonctionne pas avec les Projects récents, car il interroge l'API des Projects classiques, supprimée. On crée donc l'issue, puis on l'ajoute au Project.

1. Écrire le corps dans un fichier temporaire, puis créer l'issue :

   ```bash
   gh issue create --repo Chezrush/AREA \
     --title "<titre>" --body-file <fichier> \
     --assignee <login> --label "type:…" --label "area:…" \
     --milestone "<milestone>"
   ```

2. L'ajouter au Project et fixer son statut :

   ```bash
   id=$(gh project item-add 678 --owner EpitechPGE3-2026 --url <url-issue> --format json --jq .id)
   gh project item-edit --id "$id" --project-id <project-id> \
     --field-id <status-field-id> --single-select-option-id <option-id>
   ```

   `<project-id>` vient de `gh project view 678 --owner EpitechPGE3-2026 --format json --jq .id`. Les deux autres identifiants viennent de `gh project field-list`.

3. Vérifier avec `gh issue view <N> --json assignees,labels,milestone,projectItems` que tout est présent.

En cas d'échec partiel (par exemple l'issue est créée mais pas ajoutée au Project), corriger ce qui manque. Ne jamais recréer l'issue.

## Phase 7 : Compte rendu

- Numéro et URL de l'issue ; responsable, labels, milestone, statut.
- Pour la suite : branche `<type>/<N>-<slug>`.
