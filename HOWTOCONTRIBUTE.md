# Étendre le produit

Ce guide explique comment ajouter un **Service**, une **Action**, une **REAction** ou un **type de nœud** de workflow. Il est rédigé pour quelqu'un qui découvre le code : chaque procédure doit pouvoir être suivie pas à pas, sans aide.

Pour le déroulé d'une contribution (issue, branche, pull request, relecture), voir [`CONTRIBUTING.md`](CONTRIBUTING.md).

> **État : squelette.** Les procédures seront écrites quand l'architecture du moteur et des connecteurs sera en place. Chaque procédure sera vérifiée en ajoutant réellement un élément en la suivant.

## Principes

- Ajouter un Service, une Action, une REAction ou un type de nœud **ne modifie pas le moteur de workflows**.
- Le catalogue est déclaré **une seule fois**, côté serveur. Les clients le découvrent via l'endpoint de description des services : aucun catalogue codé en dur ailleurs.
- Chaque type de nœud déclare les clés de données qu'il publie. Les nœuds suivants ne peuvent référencer que ces clés.
- Les identifiants délégués d'un service (jetons OAuth 2.0) ne sont jamais journalisés ni renvoyés aux clients.

## Ajouter un Service

_À rédiger : déclaration du service, mécanisme d'autorisation (OAuth 2.0 ou autre), variables d'environnement à ajouter dans `.env.example`, tests._

## Ajouter une Action

_À rédiger : déclaration, paramètres, clés publiées, hook de détection, identification des événements pour ne jamais retraiter la même occurrence, tests._

## Ajouter une REAction

_À rédiger : déclaration, paramètres, clés publiées, exécution, gestion des erreurs du service tiers, tests._

## Ajouter un type de nœud

_À rédiger : interface commune (validation et exécution), enregistrement au démarrage, clés publiées, tests._

## Vérifier l'ajout

_À rédiger : où le nouvel élément apparaît (description des services, client web, client mobile), tests à lancer, mise à jour de la description OpenAPI si un endpoint change._
