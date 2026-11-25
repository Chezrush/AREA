# Critères WCAG 2.2 AA pour AREA

Le sujet demande le niveau AA des WCAG, sans fixer de version : on vise la 2.2, la plus récente, qui ajoute notamment 2.4.11, 2.5.7, 2.5.8, 3.3.7 et 3.3.8.

Les commandes `git grep` repèrent des candidats, pas des verdicts. Regarde chaque résultat, et adapte les commandes au framework (React, Vue, Svelte, Flutter, Jetpack Compose, React Native…).

## Sommaire

1. [Pièges propres au projet](#1-pièges-propres-au-projet)
2. [Structure et lecteurs d'écran (web)](#2-structure-et-lecteurs-décran-web)
3. [Android](#3-android)
4. [Contrastes et couleur](#4-contrastes-et-couleur)
5. [Formulaires et authentification](#5-formulaires-et-authentification)
6. [Clavier et focus (web)](#6-clavier-et-focus-web)
7. [Mise en page, zoom, cibles](#7-mise-en-page-zoom-cibles)
8. [Langues](#8-langues)

---

## 1. Pièges propres au projet

**Builder et glisser-déposer : 2.5.7 Mouvements de glissement (AA) et 2.1.1 Clavier (A).** Tout ce qui se fait en glissant (ajouter un nœud, le relier, le réordonner) doit aussi se faire par un appui simple **et** au clavier : boutons « Ajouter une réaction », « Monter », « Descendre », menu de choix du nœud suivant. Un canvas (`<canvas>`, SVG sans rôles) est invisible aux lecteurs d'écran : la structure du workflow doit aussi exister en HTML (liste ordonnée des nœuds, branches de la condition nommées « si vrai » et « si faux »).

**Mapping des données : 4.1.2 Nom, rôle, valeur (A) et 3.3.2 Étiquettes (A).** Le choix d'une clé (`{{ trigger.subject }}`) se fait par une liste ou une combobox accessible, avec un libellé qui nomme le nœud source. Une erreur « référence inconnue » renvoyée à l'enregistrement est liée au champ fautif (voir §5).

**Messages d'état : 4.1.3 (AA).** « Workflow enregistré », « 2 erreurs de validation », « Service connecté », « Exécution terminée » sont annoncés via `role="status"` ou `aria-live="polite"` sur le web, et `announceForAccessibility` ou une `liveRegion` sur Android, sans déplacer le focus. Vérifier : `git grep -nE 'aria-live|role="(status|alert)"|liveRegion|announceForAccessibility'`.

**Redirections OAuth et OIDC.** Le retour d'un fournisseur externe remet l'utilisateur sur une page qui annonce clairement le résultat (titre de page, message de statut), et le focus est placé au début du contenu. L'écran du fournisseur lui-même est hors périmètre de l'audit : le mentionner dans le rapport.

**Historique d'exécution.** Statut d'une exécution (succès, échec, en attente) jamais porté par la seule couleur (1.4.1) : texte ou icône nommée en plus.

**Délais : 2.2.1 (A).** Une session qui expire prévient l'utilisateur et lui permet de prolonger, ou ne fait perdre aucun travail en cours dans le builder.

## 2. Structure et lecteurs d'écran (web)

| Critère | Ce qu'on attend ici | Vérifier |
| --- | --- | --- |
| 1.3.1 Info et relations (A) | HTML sémantique : `<main>`, `<nav>`, `<header>`, vraies listes pour les workflows et les services, `<button>` et `<a>` natifs, tableaux avec `<th>` pour l'historique | `git grep -nE '<(div\|span)[^>]*on(Click\|click)'` |
| 2.4.6 En-têtes et étiquettes (AA) | Un `<h1>` par écran, pas de saut de niveau | Lister les titres par page |
| 2.4.2 Titre de page (A) | `document.title` mis à jour à chaque route (« Modifier le workflow X – `<Produit>` ») | Routeur de la SPA |
| 2.4.1 Contourner des blocs (A) | Lien d'évitement vers le contenu principal | `git grep -n 'skip'` |
| 4.1.2 Nom, rôle, valeur (A) | Bouton icône avec nom accessible ; interrupteur actif/inactif avec `role="switch"` + `aria-checked` ou `<input type="checkbox">` | `git grep -nE '<button'` sans texte ni `aria-label` |
| 2.5.3 Étiquette dans le nom (A) | Le nom accessible contient le texte visible | Comparer texte visible et `aria-label` |
| 1.1.1 Contenu non textuel (A) | Logos de services avec `alt` = nom du service, ou `alt=""` si le nom est écrit à côté | `git grep -nP '<img(?![^>]*\balt=)'` |

## 3. Android

| Critère | Ce qu'on attend ici | Vérifier |
| --- | --- | --- |
| 1.1.1 / 4.1.2 | Chaque contrôle a un libellé : `contentDescription` (vues), `Modifier.semantics { contentDescription = … }` (Compose), `Semantics`/`semanticsLabel` (Flutter), `accessibilityLabel` (React Native). Icônes décoratives masquées | Lint Android, Accessibility Scanner |
| 4.1.2 | Interrupteur d'activation d'un workflow : composant natif (`Switch`) avec son état annoncé | TalkBack |
| 2.5.8 Taille de cible (AA) | 24 × 24 px CSS minimum selon WCAG ; viser **48 × 48 dp** (recommandation Android) | Accessibility Scanner |
| 1.4.4 Redimensionnement (AA) | Textes en `sp` ; l'interface reste utilisable avec la police système à 200 % | Réglages > Taille de police |
| 1.3.4 Orientation (AA) | Pas de verrouillage d'orientation | Manifeste (`screenOrientation`) |
| 2.4.3 Ordre du focus (A) | Ordre TalkBack logique ; regroupement des éléments d'une carte de workflow | TalkBack |
| 3.3.1 / 3.3.3 | Erreurs de saisie (adresse du serveur, identifiants) affichées sur le champ (`setError`, `supportingText`) et annoncées | TalkBack |

## 4. Contrastes et couleur

| Critère | Seuil | Où regarder |
| --- | --- | --- |
| 1.4.3 Contraste minimum (AA) | 4,5:1 pour le texte courant ; 3:1 pour le gros texte (≥ 24 px, ou ≥ 18,66 px en gras) | Palette, texte sur fonds colorés, thème sombre s'il existe |
| 1.4.11 Contraste du non-textuel (AA) | 3:1 pour les bords de champs, l'anneau de focus, les connecteurs du builder, les icônes porteuses de sens | Styles des composants |
| 1.4.1 Utilisation de la couleur (A) | Jamais la couleur seule : statut d'exécution, branche vraie ou fausse de la condition, erreurs | États et badges |

Utilise `scripts/contraste.py` sur chaque paire. Ne jamais arrondir vers le haut : 4,49:1 échoue.

## 5. Formulaires et authentification

Formulaires concernés : inscription, connexion, mot de passe oublié, paramètres d'Action et de REAction, condition, adresse du serveur (mobile).

| Critère | Attendu |
| --- | --- |
| 3.3.2 Étiquettes (A) | `<label for>` visible sur chaque champ ; un placeholder ne compte pas |
| 3.3.1 Identification des erreurs (A) | Message en texte, lié au champ (`aria-describedby`), champ en `aria-invalid="true"`, annoncé |
| 3.3.3 Suggestion (AA) | Le message propose une correction (« L'adresse doit commencer par http:// ou https:// ») |
| 1.3.5 Finalité des champs (AA) | `autocomplete="username"`, `"email"`, `"current-password"`, `"new-password"` |
| 3.3.7 Saisie redondante (A) | Ne pas redemander une information déjà fournie dans le même parcours (paramètres d'un nœud après retour en arrière) |
| 3.3.8 Authentification accessible (AA) | Coller un mot de passe autorisé, gestionnaire de mots de passe compatible, pas de test cognitif ; un CAPTCHA éventuel (anti-abus) doit avoir une alternative |

Les erreurs renvoyées par le serveur (validation du workflow, identifiants refusés, limite de tentatives) sont traitées de la même façon. Vérifier : `git grep -nE 'aria-describedby|aria-invalid'`.

## 6. Clavier et focus (web)

| Critère | Attendu |
| --- | --- |
| 2.1.1 Clavier (A) / 2.1.2 Pas de piège (A) | Tout le parcours, builder compris, se fait au clavier ; les modales rendent le focus à leur fermeture |
| 2.4.3 Ordre du focus (A) | Ordre logique ; pas de `tabindex` positif (`git grep -nE 'tabindex="[1-9]'`) |
| 2.4.7 Focus visible (AA) | Jamais d'`outline: none` sans remplacement (`git grep -nE 'outline:\s*(none\|0)'`) |
| 2.4.11 Focus non masqué (AA) | L'élément focalisé n'est pas caché par un bandeau collant ou un panneau latéral |

## 7. Mise en page, zoom, cibles

| Critère | Attendu |
| --- | --- |
| 1.4.4 Redimensionnement (AA) | Zoom navigateur à 200 % sans perte de contenu ; jamais `user-scalable=no` (`git grep -nE 'user-scalable\|maximum-scale'`) |
| 1.4.10 Redistribution (AA) | Pas de défilement horizontal à 320 px de large, sauf dans le canvas du builder s'il existe (le mentionner) |
| 1.4.12 Espacement du texte (AA) | Pas de hauteurs fixes qui tronquent le texte |
| 2.5.8 Taille de la cible (AA) | 24 × 24 px CSS minimum, ou espacement équivalent |

## 8. Langues

| Critère | Attendu |
| --- | --- |
| 3.1.1 Langue de la page (A) | `<html lang>` mis à jour quand l'utilisateur change de langue ; locale de l'application Android |
| 3.1.2 Langue d'un passage (AA) | `lang` sur un passage dans une autre langue (nom de service étranger long, contenu tiers) si nécessaire |

Les libellés accessibles (`aria-label`, `contentDescription`) passent eux aussi par les fichiers de traduction.
