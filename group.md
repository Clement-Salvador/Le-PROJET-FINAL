# Suivi de projet — Groupe 4 (`gateway-service` + `stats-service`)

## 👥 Répartition des rôles

| Membre                | Rôle principal                           |
| --------------------- | ---------------------------------------- |
| **Clément SALVADOR**  | Responsable documentation & Dockerfiles  |
| **Guillaume POMIÈS**  | Coordinateur API & infrastructure réseau |
| **Émilien RESTOUEIX** | Développeur principal Flask / JWT        |

---

## Journal de bord

### Lundi 07 Juillet

* **08h30** — Démarrage du projet :

  * Lecture approfondie du sujet et clarification des responsabilités.
  * Création de l’arborescence du projet, initialisation du dépôt Git.

* **09h15** — Répartition initiale des tâches :

  * **Clément** : création des `Dockerfile` pour `gateway-service` et `stats-service`, gestion des fichiers `README.md`, `group.md`.
  * **Émilien** : implémentation des routes Flask pour le `gateway-service`, gestion du JWT, logique de reverse proxy.
  * **Guillaume** : configuration du `docker-compose.yml`, intégration de Traefik, vérification de la connectivité inter-services.

* **10h40** — Premier build Docker fonctionnel du `gateway-service`.

* **11h10** — Intégration réussie de Traefik :

  * Ajout des labels nécessaires dans le `docker-compose.yml`
  * Routage opérationnel via Traefik vers `gateway-service`.

---

### Mardi 08 Juillet

* **13h30** — Réorganisation ponctuelle des rôles :

  * **Clément** : développement des routes et calculs statistiques dans le `stats-service`.
  * **Émilien** : finalisation de la configuration Traefik, vérification des redirections et des routes exposées.
  * **Guillaume** : gestion du JWT (passage d'en-têtes, compatibilité inter-services).

  
