# Groupe 4 — `gateway-service` & `stats-service`

## Objectif du service

Nous sommes responsables de deux micro-services essentiels dans l’architecture distribuée de l’IRC CanaDuck :

### 1. `gateway-service` — Point d’entrée unique (proxy intelligent)

Ce service joue le rôle de **passerelle centrale** entre les clients (utilisateurs, interface front-end, outils de test comme Hoppscotch) et les autres micro-services internes : `user-service`, `message-service` et `channel-service`.

Le `gateway-service` est le **seul service exposé publiquement via Traefik**. Il est chargé de :

- **Relayer dynamiquement** les requêtes REST vers les bons services internes,
- **Transmettre les en-têtes d’authentification (JWT)** de manière sécurisée,
- **Analyser les tokens JWT** pour vérifier les droits d’accès avant transmission,
- **Fusionner les réponses** issues de plusieurs services pour certaines routes complexes (ex. `/fullinfo`).

Il simplifie l’usage de l’API côté client tout en garantissant un bon découplage entre les services.

---

### 2. `stats-service` — Statistiques internes

Le `stats-service` a pour mission de **fournir des métriques** sur l’activité de la plateforme IRC. Il agrège les données issues des autres micro-services, notamment le `message-service`, pour produire des analyses utiles telles que :

- les canaux les plus actifs,
- l’activité horaire des utilisateurs,
- le nombre total de messages par utilisateur,
- les messages les plus réactés.

Ce service **n’est pas exposé publiquement**, mais il peut être interrogé par le `gateway-service` via des routes `/stats/...`.

---

➡️ Ce dépôt contient le développement, la documentation, les fichiers de test et la conteneurisation (Docker) de ces deux services.
