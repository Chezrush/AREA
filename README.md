# _Nom du produit à définir_

Une suite d'automatisation qui relie les services en ligne que vous utilisez déjà. Quand un événement se produit dans un service (un mail reçu, un fichier ajouté, une issue ouverte), le produit le détecte et déclenche automatiquement une ou plusieurs actions dans d'autres services.

Le produit se compose de trois parties :

- un **serveur d'application**, qui porte toute la logique : comptes, services, workflows et hooks ;
- un **client web**, pour s'abonner aux services et construire ses workflows ;
- un **client mobile Android**, pour suivre ses workflows, les activer ou les désactiver et voir ce qu'ils ont fait.

## Sommaire

- [Vocabulaire](#vocabulaire)
- [Prérequis](#prérequis)
- [Installation et lancement](#installation-et-lancement)
- [Tests](#tests)
- [API publique](#api-publique)
- [Documentation](#documentation)
- [Contribuer](#contribuer)
- [Usage de l'IA](#usage-de-lia)
- [Licence](#licence)

## Vocabulaire

| Terme | Sens |
| --- | --- |
| Service | Une plateforme tierce à laquelle l'utilisateur s'abonne (messagerie, stockage, forge logicielle…) |
| Action | Un événement détecté dans un service ; c'est le déclencheur d'un workflow |
| REAction | Une tâche réalisée par le produit dans un service, en réponse à une Action |
| Hook | Le mécanisme qui détecte les Actions, sans qu'aucun client soit ouvert |
| Workflow | Une chaîne de nœuds : un déclencheur, une ou plusieurs réactions, et au plus une condition à deux branches |
| AREA | Le plus petit workflow possible : une Action reliée à une REAction |

## Prérequis

_À compléter après le choix de la stack._

- [Docker](https://docs.docker.com/get-docker/) et Docker Compose : tout le produit se construit et se lance avec Docker Compose.

## Installation et lancement

_À compléter après le choix de la stack._

```bash
cp .env.example .env   # puis renseigner les valeurs
docker compose up --build
```

| Élément | Où le trouver |
| --- | --- |
| Serveur d'application | _à définir_ |
| Client web | _à définir_ |
| APK Android installable | _à définir_ |

## Tests

_À compléter après le choix de la stack : lint, tests unitaires et fonctionnels, tests de contrat OpenAPI, build._

## API publique

Le serveur sert une description **OpenAPI** de son API HTTP, avec une interface navigable. Il expose aussi la description des services, Actions et REActions disponibles, que les clients lisent pour ne rien coder en dur.

| Ressource | URL |
| --- | --- |
| Description OpenAPI | _à définir_ |
| Interface navigable de l'API | _à définir_ |
| Description des services (`about.json`) | _à définir_ |

## Documentation

Toute la documentation est en français. Elle sera rangée dans `docs/` au fil du projet :

| Rubrique | Contenu |
| --- | --- |
| `docs/adr/` | Journal des décisions d'architecture (à venir avec le jalon Plan) |
| [`HOWTOCONTRIBUTE.md`](HOWTOCONTRIBUTE.md) | Ajouter un service, une Action, une REAction ou un type de nœud |

D'autres rubriques s'ajouteront au fil du projet :

- comparatifs de technologies ;
- modèle de workflow et sémantique d'échec ;
- modèle de persistance ;
- fonctionnalités additionnelles et preuves de sécurité ;
- rapport d'audit d'accessibilité ;
- post-mortem.

## Contribuer

Le déroulé d'une contribution est décrit dans [`CONTRIBUTING.md`](CONTRIBUTING.md) : issue → branche → pull request → relecture → merge. Pour étendre le produit (nouveau service, nouveau nœud), voir [`HOWTOCONTRIBUTE.md`](HOWTOCONTRIBUTE.md). Les participants s'engagent à respecter le [code de conduite](CODE_OF_CONDUCT.md). Les changements notables sont listés dans le [`CHANGELOG.md`](CHANGELOG.md).

## Usage de l'IA

Conformément à la charte IONIS sur l'usage de l'IA, nous déclarons les outils d'intelligence artificielle utilisés dans ce projet et leur usage. Cette liste est mise à jour dans la pull request qui introduit un nouvel usage.

| Outil | Utilisé pour | Non utilisé pour |
| --- | --- | --- |
| Claude Code (Anthropic) | Rédaction de la documentation et des modèles du dépôt, configuration de l'outillage, rédaction et organisation des issues | Commits et push (toujours faits par les membres du groupe) |

Ce qui est produit avec l'aide de l'IA suit exactement les mêmes règles que le reste du projet : relecture en pull request par un autre membre, tests, propreté et sécurité. Les membres du groupe restent auteurs et responsables de chaque commit, et chacun défend lui-même les décisions auxquelles il a contribué.

## Licence

Le code est distribué sous [licence MIT](LICENSE).
