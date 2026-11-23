# Contribuer

Ce document décrit comment une modification arrive dans le projet, de l'idée jusqu'au merge. Il s'applique à tout le monde, membres du groupe compris.

Pour ajouter un service, une Action, une REAction ou un type de nœud, voir aussi [`HOWTOCONTRIBUTE.md`](HOWTOCONTRIBUTE.md).

## Déroulé d'une contribution

1. **Une tâche = une issue.** Chaque issue a un responsable, au moins un label `type:*` et un label `area:*`, une milestone (`Plan`, `MVP` ou `Final Product`), un statut dans le [GitHub Project AREA](https://github.com/orgs/EpitechPGE3-2026/projects/678) et ses dépendances. On crée l'issue à partir des modèles proposés.
2. **Une issue = une branche**, créée depuis `main` à jour (voir [Branches](#branches)). Le statut de l'issue passe à `In progress`.
3. **Des commits au format Conventional Commits** (voir [Commits](#commits)).
4. **Une pull request liée à l'issue**, avec `Closes #N` dans la description, en suivant le modèle de PR. Le statut de l'issue passe à `In review`.
5. **Relecture par un autre membre du groupe.** Personne ne merge sa propre PR sans relecture.
6. **Merge** seulement quand les checks sont verts et la relecture approuvée. L'issue se ferme automatiquement.

Personne ne pousse directement sur `main`. GitHub ne l'empêche pas techniquement, car le groupe n'a pas les droits pour protéger la branche : c'est à nous de le respecter.

## Branches

La stratégie est volontairement simple (*trunk-based*) :

- `main` est la seule branche durable, et elle reste toujours fonctionnelle.
- Toute modification passe par une branche courte, nommée `<type>/<numéro-issue>-<description-courte>` :

| Préfixe | Usage | Exemple |
| --- | --- | --- |
| `feat/` | Nouvelle fonctionnalité | `feat/14-builder-condition` |
| `fix/` | Correction de bug | `fix/27-refresh-token-expire` |
| `docs/` | Documentation | `docs/3-fichiers-depot` |
| `ci/` | Pipeline, Docker Compose, déploiement | `ci/8-pipeline` |
| `test/` | Tests uniquement | `test/31-contrat-openapi` |
| `refactor/` | Restructuration sans changement de comportement | `refactor/40-registre-noeuds` |
| `chore/` | Outillage, configuration, dépendances | `chore/1-claude-code` |

Une branche ne vit que le temps de sa PR. On la supprime après le merge.

## Commits

On utilise [Conventional Commits](https://www.conventionalcommits.org/fr/) :

```text
<type>(<portée optionnelle>): <description à l'impératif>
```

Exemples :

```text
feat(engine): reject references to undeclared keys on save
fix(mobile): keep the server address after restart
docs(adr): add persistence technology decision
test(api): check the OpenAPI description against the routes
```

Types : `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `perf`, `chore`, `build`. Un commit doit rester petit et cohérent : il fait une seule chose. L'historique sert de preuve lors de la défense individuelle : un message clair aide à expliquer sa contribution.

## Avant d'ouvrir une pull request

- [ ] Le lint, les tests et le build passent en local.
- [ ] Les entrées sont **validées côté serveur**, et les chemins de succès comme d'échec sont testés.
- [ ] La **description OpenAPI** décrit tout endpoint ajouté ou modifié, réponses d'erreur comprises.
- [ ] Une fonctionnalité visible existe sur **les deux clients**, ou une issue est ouverte pour le client manquant. C'est le client le moins complet qui compte.
- [ ] Toute interface respecte l'**accessibilité** (WCAG AA), et ses textes sont traduits dans toutes les langues prises en charge.
- [ ] La **documentation** est mise à jour dans la même PR :
  - nouveau service, Action, REAction ou type de nœud → [`HOWTOCONTRIBUTE.md`](HOWTOCONTRIBUTE.md) si la procédure change ;
  - choix d'architecture → nouvel ADR dans `docs/adr/` ;
  - fonctionnalité du catalogue → où chaque critère d'acceptation s'observe ;
  - protection de sécurité (`SEC-*`) → fiche de preuve.
- [ ] Une entrée est ajoutée dans [`CHANGELOG.md`](CHANGELOG.md), section « Non publié », pour tout changement notable.
- [ ] Aucun secret n'est ajouté (jeton, mot de passe, clé), et aucun jeton n'apparaît dans les logs. Toute nouvelle variable d'environnement est documentée dans [`.env.example`](.env.example).
- [ ] Si un outil d'IA a contribué de façon notable, la section « Usage de l'IA » du [README](README.md) est à jour.

## Intégration continue

GitHub Actions n'est pas disponible sur le dépôt principal (facturation de l'organisation). La CI s'exécutera sur un dépôt miroir privé, et ses résultats apparaîtront comme checks dans les PR. La mise en place et le détail des jobs seront documentés dans `docs/`.

Si un check échoue, **on corrige la cause**. On ne désactive jamais un test, on n'ajoute pas de `skip` et on ne coupe pas une règle de lint pour faire passer la CI. Si la cause est hors de portée de la PR, on le signale dans la PR et on ouvre une issue. **Une PR sans checks n'est pas une PR verte.**

## Relecture

La personne qui relit vérifie :

- que le changement répond à l'issue, et seulement à elle ;
- que le code est lisible et testé, sans code mort ni fichier orphelin ;
- que la logique métier reste sur le serveur et que le moteur n'a pas été modifié pour ajouter un connecteur ;
- que la sécurité tient : entrées validées, jetons protégés, aucun secret ;
- le contrat OpenAPI, l'accessibilité, les traductions et la documentation.

Elle laisse des commentaires précis et constructifs, puis approuve ou demande des modifications.

## Versions

Les versions suivent le [versionnage sémantique](https://semver.org/lang/fr/). À chaque jalon (Plan, MVP, Final Product) :

- on déplace la section « Non publié » du `CHANGELOG.md` sous un numéro de version ;
- on pose un tag `vX.Y.Z` sur `main`.
