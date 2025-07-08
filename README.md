# Groupe 4 — `gateway-service` & `stats-service`

## Objectif du service

Nous sommes responsables de deux micro-services essentiels dans l’architecture distribuée de l’IRC CanaDuck :

### 1. `gateway-service` — Point d’entrée unique (proxy intelligent)

Ce service joue le rôle de **passerelle centrale** entre les clients (utilisateurs, interface front-end, outils de test comme Hoppscotch) et les autres micro-services internes : `user-service`, `message-service` et `channel-service`.

Le `gateway-service` est le **seul service exposé publiquement via Traefik**. Il est chargé de :

- **Relayer** les requêtes REST vers les bons services internes,
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

Voici un complément structuré pour ton `README.md`, à intégrer à la suite du texte existant. Ce complément décrit l'installation, l'utilisation, les routes disponibles, la structure des messages et l'organisation du projet, comme attendu dans le sujet du TP.

---

## Installation et exécution

### Prérequis

* `Docker` et `docker-compose`
* Un terminal compatible avec `curl` ou `Hoppscotch` pour les tests API

### Lancement

```bash
docker-compose up --build
```

> Le `gateway-service` est accessible via `http://localhost/` (proxy Traefik).
> Les autres services ne sont pas exposés directement.

---

## Structure des services

### gateway-service

* Port interne : `5004`
* Exposé publiquement via Traefik
* Redirige les routes vers :

  * `/register`, `/login`, `/whois` → `user-service`
  * `/msg`, `/msg/...` → `message-service`
  * `/channel`, `/channel/...` → `channel-service`
  * `/stats/...` → `stats-service`
* Route spéciale : `/fullinfo?user=roger&channel=tech` → agrégation multi-services

### stats-service

* Port interne : `5005`
* Non exposé publiquement
* Interroge `message-service` pour obtenir :

  * L’activité horaire
  * Les canaux actifs
  * Le nombre de messages par utilisateur
  * Les messages les plus réactés

---

## Authentification JWT

Les deux services attendent un header HTTP :

```
Authorization: Bearer <token>
```

Le `token` est vérifié via la fonction `verify_token()` dans `auth.py`, qui utilise la clé secrète `JWT_SECRET` partagée.

---

## Routes exposées

### `gateway-service` (public)

| Méthode | Route                            | Description                        |
| ------- | -------------------------------- | ---------------------------------- |
| `POST`  | `/register`                      | Proxy vers `user-service`          |
| `POST`  | `/login`                         | Authentification et retour JWT     |
| `GET`   | `/channel`                       | Liste des canaux publics           |
| `POST`  | `/msg`                           | Envoi de message                   |
| `GET`   | `/msg?channel=...`               | Récupère les messages              |
| `GET`   | `/fullinfo?user=...&channel=...` | Agrège données user/canal/messages |
| `GET`   | `/stats/messages-per-user`       | Délègue à `stats-service`          |
| etc.    | ...                              | Redirigé selon la route            |

### `stats-service` (interne)

| Méthode | Route                         | Description                              |
| ------- | ----------------------------- | ---------------------------------------- |
| `GET`   | `/stats/messages-per-user`    | Nombre total de messages par utilisateur |
| `GET`   | `/stats/hourly-activity`      | Volume horaire                           |
| `GET`   | `/stats/active-channels`      | Canaux les plus actifs                   |
| `GET`   | `/stats/top-reacted-messages` | Messages les plus réactés                |

---

## Structure des messages JSON

Exemple de message récupéré depuis `message-service` :

```json
{
  "id": 17,
  "from": "roger",
  "channel": "tech",
  "text": "Salut tout le monde !",
  "timestamp": "2025-07-08T11:30:42",
  "reactions": {
    "👍": ["roger", "ginette"],
    "❤️": ["luc"]
  }
}
```

---

## Exemple d’appel curl

```bash
curl -H "Authorization: Bearer <votre_token>" http://localhost/stats/messages-per-user
```
