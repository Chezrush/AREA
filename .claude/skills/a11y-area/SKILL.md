---
name: a11y-area
description: Accessibilité du projet AREA selon les WCAG niveau AA, pour le client web (dont le builder de workflows) et le client mobile Android. Couvre la conception accessible, l'audit, les corrections et le rapport d'audit exigé par le sujet (ce qui a été mesuré, avec quel outil, sur quels écrans, ce qui a été corrigé et ce qui ne l'a pas été). À utiliser dès qu'on crée ou relit un écran, un formulaire (inscription, connexion, abonnement à un service), le builder, une liste de workflows, une palette ou un thème, ou qu'on parle de contraste, aria, lecteur d'écran, TalkBack, focus, clavier, taille de police, zoom, cibles tactiles, Lighthouse, axe, Accessibility Scanner ou rapport d'audit, même si le mot « accessibilité » n'est pas prononcé.
---

# Accessibilité AREA

Le sujet exige que les **deux clients** atteignent le niveau **AA des WCAG**, et qu'un **rapport d'audit honnête** soit commité. Le rapport indique ce qui a été mesuré, avec quel outil, sur quels écrans, ce qui a été corrigé, et ce qui ne l'a pas été avec la raison. L'évaluateur peut demander une démonstration en direct. Ajoutée à la fin, l'accessibilité coûte cher : il faut refaire le builder, les formulaires, la palette. Prévue dès la conception, elle ne coûte presque rien.

Le point le plus difficile du projet est le **builder** : un éditeur de workflows en canvas avec glisser-déposer est très coûteux à rendre accessible. Si le groupe hésite sur la forme du builder, rappeler qu'une liste d'étapes ou un assistant à formulaires est accessible presque par construction. Le sujet accepte les deux formes, à condition de justifier le choix.

## Périmètre

| Surface | Référentiel | Écrans |
| --- | --- | --- |
| Client web | WCAG 2.2 AA | Inscription, confirmation, connexion (locale et OIDC), abonnement aux services, catalogue, builder, liste et historique des workflows, réglages |
| Client Android | WCAG 2.2 AA appliquées au mobile (et Material Design accessibility) | Configuration de l'adresse du serveur, inscription, connexion, liste des workflows, activation et désactivation, historique d'exécution |

L'**internationalisation** est liée : au moins deux langues sur le parcours principal, avec la langue déclarée (`lang`, locale Android) pour que le lecteur d'écran prononce correctement.

## Références

- `references/criteres.md` : critères retenus pour ce projet, comment les vérifier dans le code web et Android, pièges du builder. À lire pour toute conception ou tout audit.
- `references/livrables.md` : modèle du rapport d'audit et protocole de test au lecteur d'écran.
- `scripts/contraste.py` : calcule les ratios de contraste WCAG. Utilise-le au lieu d'estimer à l'œil :
  `python3 .claude/skills/a11y-area/scripts/contraste.py "#1a1a2e:#ffffff" "#7c3aed:#0b0b1f"`

## Choisir le mode

Déduis le mode de la demande. S'il y a un doute, commence par auditer.

### 1. Concevoir (avant de coder)

Avant d'écrire un écran, un composant ou une palette, donne les décisions à prendre tout de suite :

- quel élément natif (HTML ou composant Android) utiliser ;
- quel libellé accessible ;
- quelle alternative au glisser-déposer ;
- quelle taille de cible ;
- quelles annonces de statut (enregistrement du workflow, erreur de validation, exécution terminée) ;
- comment les textes passent par les fichiers de traduction.

Si une décision engage l'architecture (forme du builder, bibliothèque de composants, framework mobile), propose de l'écrire dans un ADR.

### 2. Auditer (lecture seule)

1. **Inventorie** les écrans des deux clients.
2. **Revue statique** avec `references/criteres.md`. Note chaque problème avec `fichier:ligne`.
3. **Outils automatiques**, en utilisant d'abord ceux déjà présents dans le projet :
   - web : `npx @axe-core/cli <url>`, `npx lighthouse <url> --only-categories=accessibility --output=json --output-path=<fichier>`, ou `@axe-core/playwright` dans les tests de bout en bout (le plus durable, car il tourne en CI) ;
   - Android : Accessibility Scanner sur l'appareil, les vérifications d'accessibilité d'Espresso (`AccessibilityChecks.enable()`) ou l'équivalent du framework choisi, et le lint Android (`contentDescription`, `ClickableViewAccessibility`).

   Demande avant d'ajouter une dépendance au projet.
4. **Contrastes** : récupère les couleurs réellement utilisées (variables CSS, thème Material, `colors.xml`) et passe chaque paire dans `scripts/contraste.py`.
5. **Ce qui demande un humain** (TalkBack sur un vrai téléphone, lecteur d'écran web, zoom à 200 %, police système agrandie) : liste-le sans conclure à la place du testeur.

Gravité :

- **bloquant** : empêche le parcours principal (inscription → abonnement → création d'un AREA sur le web ; connexion → activation d'un workflow sur mobile) ;
- **majeur** : gêne forte ailleurs ;
- **mineur** : le reste.

### 3. Corriger

Seulement à la demande, après un audit ou sur un problème précis. Suis le workflow du `CLAUDE.md` (issue → branche → PR ; Claude ne commite pas). Cite le critère WCAG dans la description de la PR, pour alimenter la colonne « corrections » du rapport. Corrige la cause dans le composant partagé plutôt qu'écran par écran.

### 4. Produire le rapport

Range-le dans `docs/accessibilite/` avec le modèle de `references/livrables.md` : `audit-<date>.md`, et `test-lecteur-ecran.md` pour le protocole. Le test, lui, est réalisé par un membre sur un vrai appareil : ne remplis jamais les résultats à sa place.

## Honnêteté des conclusions

Les outils automatiques ne détectent qu'une partie des problèmes, de l'ordre d'un tiers. Un score Lighthouse de 100 ne prouve pas la conformité. N'écris jamais « conforme » sans base. Le sujet demande explicitement ce qui **n'a pas** été corrigé et pourquoi : un rapport qui liste honnêtement ses limites vaut mieux qu'une conformité affirmée que l'évaluateur démonte en direct.
