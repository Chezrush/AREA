# Modèles des livrables d'accessibilité

Le sujet exige un **rapport d'audit commité** pour les deux clients : ce qui a été mesuré, avec quel outil, sur quels écrans, ce qui a été corrigé, et ce qui ne l'a pas été avec la raison. Les fichiers vont dans `docs/accessibilite/`.

## 1. Rapport d'audit

Fichier : `docs/accessibilite/audit-<AAAA-MM-JJ>.md`. On met le même rapport à jour au fil des PR de correction, plutôt que d'en écrire un nouveau.

```markdown
# Audit d'accessibilité : <client web | client Android | les deux> (<date>)

## Méthode
- Version auditée : <commit ou tag>, <URL locale ou build APK>
- Référentiel : WCAG 2.2 niveau AA (critères retenus : voir la skill a11y-area)
- Revue statique du code
- Outils automatiques : <axe x.y, Lighthouse x.y, Accessibility Scanner x.y, Espresso AccessibilityChecks…>, <navigateur, appareil, version d'Android>
- Tests manuels : <lecteur d'écran web, TalkBack, clavier seul, zoom 200 %, police système agrandie>

## Écrans audités
| Client | Écran | Outils | Tests manuels |
|---|---|---|---|
| Web | Inscription | axe, Lighthouse | Clavier, NVDA |
| Android | Liste des workflows | Accessibility Scanner | TalkBack |

## Résumé
<n> non-conformités, dont <b> bloquantes pour le parcours principal.
Rappel : un score automatique ne vaut pas conformité.

## Non-conformités
| # | Critère WCAG | Client | Où | Problème | Correction | Gravité | Statut |
|---|---|---|---|---|---|---|---|
| 1 | 2.5.7 Glissement | Web | `src/builder/Canvas.tsx:42` | Réordonner un nœud exige un glisser | Boutons « Monter » et « Descendre » | Bloquant | Corrigé (#57) |

## Non corrigé, et pourquoi
| # | Critère | Raison | Contournement | Échéance éventuelle |
|---|---|---|---|---|

## Critères vérifiés conformes
<liste courte, avec la manière dont chacun a été vérifié>

## Avant / après
| Outil | Client / écran | Avant (<date>) | Après (<date>) |
|---|---|---|---|

## Hors périmètre
- Pages des fournisseurs OAuth et OIDC tiers (non maîtrisées par le groupe)
```

## 2. Protocole de test au lecteur d'écran

Fichier : `docs/accessibilite/test-lecteur-ecran.md`. Claude rédige le protocole. Un membre du groupe réalise le test sur un vrai appareil et remplit lui-même les colonnes « Observé » et « OK/KO ».

```markdown
# Test au lecteur d'écran : parcours principal

## Conditions
- Date : … · Testeur : …
- Web : navigateur …, lecteur d'écran (NVDA, VoiceOver macOS, Orca) …
- Android : appareil …, version d'Android …, TalkBack …
- Version du produit : <commit ou tag>

## Parcours web
| # | Étape | Attendu | Observé | OK/KO | Issue |
|---|---|---|---|---|---|
| 1 | S'inscrire avec un mot de passe trop court | Erreur annoncée, liée au champ, avec suggestion | | | |
| 2 | Confirmer le compte, se connecter | Titre de page et résultat annoncés | | | |
| 3 | Connecter un service (OAuth) | Retour sur le produit annoncé, service marqué « connecté » en texte | | | |
| 4 | Créer un AREA : choisir l'Action, la REAction, mapper une clé | Chaque étape et chaque champ annoncés ; aucun glisser obligatoire | | | |
| 5 | Ajouter une condition | Branches « si vrai » et « si faux » identifiables | | | |
| 6 | Enregistrer un workflow invalide | Erreurs annoncées et reliées au nœud fautif | | | |
| 7 | Enregistrer, puis changer de langue | Confirmation annoncée ; la langue de la page change | | | |

## Parcours Android
| # | Étape | Attendu | Observé | OK/KO | Issue |
|---|---|---|---|---|---|
| 1 | Configurer l'adresse du serveur (adresse invalide puis valide) | Champ libellé ; erreur annoncée | | | |
| 2 | Se connecter | Champs libellés, mot de passe collable | | | |
| 3 | Parcourir la liste des workflows | Chaque carte annoncée avec son nom et son état | | | |
| 4 | Activer ou désactiver un workflow | Nouvel état annoncé | | | |
| 5 | Consulter l'historique d'exécution | Statut lisible sans la couleur | | | |
| 6 | Passer la police système à 200 % | Aucun texte tronqué | | | |

## Bilan
<ce qui marche, ce qui bloque, issues ouvertes>
```
