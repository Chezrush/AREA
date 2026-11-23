---
name: verif-jalon
description: Fait l'état des lieux du projet AREA (G-YEP-500) par rapport au sujet. Inspecte le dépôt, l'historique git et GitHub (issues, Project, CI, PR) et produit une checklist fait / partiel / manquant avec preuves, pour le jalon Plan, MVP ou Final Product. À utiliser dès qu'on demande où en est le projet, ce qu'il reste à faire, si on est prêts pour un jalon, une démo ou la soutenance, si les quantités (services, actions, réactions, points du catalogue) sont atteintes, si une fonctionnalité du catalogue est vraiment livrée, ce qu'un évaluateur pourrait reprocher, ou s'il faut vérifier la conformité au sujet, même si le mot « jalon » n'est pas prononcé.
---

# Vérifier un jalon AREA

Le sujet compte des dizaines d'exigences réparties sur trois jalons, un catalogue de fonctionnalités aux critères d'acceptation précis et des seuils de quantité. Beaucoup s'oublient sans bruit : une réponse d'erreur absente de l'OpenAPI, un client mobile moins complet que le web (et c'est lui qui compte), un critère de catalogue non observable qui annule toute la fonctionnalité. Cette skill transforme le sujet en état des lieux factuel du dépôt, pour que le groupe sache quoi faire avant la prochaine échéance.

## 1. Choisir la cible

Par ordre de priorité :

1. le jalon nommé par l'utilisateur (« Plan », « MVP », « final », « soutenance ») ;
2. sinon, la ligne « Prochain jalon » du `CLAUDE.md` ;
3. sinon, une déduction à partir de la date du jour (`date +%F`) et des échéances des milestones GitHub (`gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.title) \(.due_on)"'`). Annonce-la comme une hypothèse en tête du rapport.

| Jalon | Échéance | Attendu (résumé du sujet) |
| --- | --- | --- |
| Plan | début + 1 semaine | Trois comparatifs (front, back, persistance) avec preuve pratique, sélection du catalogue avec justification d'apprentissage et responsables, une question d'architecture par membre, découpage complet des tâches, méthode de gestion et outils |
| MVP | début + 4 semaines | Produit déployable de façon reproductible, workflow trigger + ≥ 2 réactions + 1 condition de bout en bout, première doc technique, plan mis à jour et analyse des changements, ≥ 1/3 des points du catalogue avancés, CI sur chaque contribution, OpenAPI servie |
| Final Product | fin du projet | Produit complet avec tout le catalogue retenu, README + HOWTOCONTRIBUTE, audit a11y des deux clients, planning final, post-mortem, soutenance avec démo et workflow à ≥ 4 réactions, enregistrement de secours |

Les jalons sont **cumulatifs** : vérifie les items de la cible, ceux des jalons précédents et les items transverses.

## 2. Charger la grille

Lis `references/grille.md`. Chaque item a un identifiant, l'exigence tirée du sujet, le jalon à partir duquel elle est attendue et la manière de la vérifier. Pour citer le sujet mot pour mot : `pdftotext -layout area-project.pdf -` (et `area-additional_features.pdf` pour le catalogue).

## 3. Collecter les preuves

Reste en **lecture seule** : cette skill observe, elle ne corrige rien.

Sources, de la plus fiable à la moins fiable :

1. **Exécuter.** Lance lint, tests et build via les commandes du README. Lance la stack Docker Compose seulement si l'utilisateur est d'accord (c'est long et ça occupe des ports). Un test qui passe vaut plus qu'un fichier qui existe. Ne déploie rien et n'appelle aucun Service tiers réel.
2. **GitHub via `gh`** : issues, Project 678, PR, statuts de commit. `gh project` demande le scope `project` : si la commande échoue, suggère `gh auth refresh -s project`.
3. **Git local** : historique, auteurs, tags.
4. **Lecture** du code, de la configuration et de la doc.

**Présence ≠ conformité.** Un fichier `hooks/gmail.ts` ne prouve pas que le hook tourne sans client ouvert ni qu'il ignore les doublons. Réserve ✅ à « un test ou une exécution le prouve ».

## 4. Statuts

- ✅ **Fait** : preuve concrète (`chemin:ligne`, commande et résultat, URL).
- ⚠️ **Partiel / à risque** : commencé mais incomplet, non testé, absent d'un des deux clients, ou démontrable seulement avec un tiers instable.
- ❌ **Manquant** : aucune trace.
- ❓ **Non vérifiable ici** : il faut une action humaine (téléphone Android, compte tiers, TalkBack). Dis laquelle.

Un **bloquant** est un item ❌ ou ⚠️ attendu au jalon cible ou avant, ou un seuil de quantité non atteint.

## 5. Rapport

Réponds dans la conversation avec ce plan. Ne l'écris dans un fichier que si l'utilisateur le demande ; dans ce cas, propose `docs/jalons/<jalon>.md`.

```markdown
# État des lieux : <jalon> (<date prévue>, J-<n>)

## Verdict
<x> ✅ · <y> ⚠️ · <z> ❌ · <w> ❓ sur les items attendus.
<2-3 phrases : prêt ou pas, et le principal risque.>

## Quantités (client le moins complet)
| Mesure | Seuil (M = 3) | Web | Mobile | Retenu |
|---|---|---|---|---|
| Services S (dont OAuth2) | ≥ 4 (≥ 2 OAuth2) | | | |
| Actions + REActions | ≥ 8 | | | |
| Points du catalogue livrés D | ≥ 6 | | | |

## Bloquants
1. **<ID> <exigence>** : <ce qui manque> → <action concrète>

## Détail
| ID | Exigence | Statut | Preuve ou manque |
|---|---|---|---|

## Catalogue
| Fonctionnalité | Catégorie | Responsable | Critères observables | Statut |
|---|---|---|---|---|

## À vérifier à la main
- <ID> : <quoi faire, sur quel appareil ou quel compte>

## À anticiper pour <jalon suivant>
<3 à 5 items lents à produire>

## Prochaines actions
<liste priorisée, chaque action assez petite pour devenir une issue, avec qui pourrait la prendre>
```

Reste factuel : « OpenAPI : `POST /workflows` sans réponse 422 décrite » sert ; « l'API pourrait être mieux documentée » ne sert à rien.

## 6. Après le rapport

Propose, sans le faire toi-même, de créer les issues qui correspondent aux prochaines actions, via `/issue`. Attends un accord explicite.
