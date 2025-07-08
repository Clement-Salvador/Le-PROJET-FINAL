# Suivi de projet — Groupe 4 (`gateway-service` + `stats-service`)

**Rôles répartis**

| Membre            | Rôle                 |
| ----------------- | -------------------- |
| Clément SALVADOR  | Responsable doc      |
| Guillaume POMIÈS  | Coordinateur API     |
| Émilien RESTOUEIX | Dev principal Python |

## Journal de bord

### Lundi 07 Juillet

- **08h30** : Prise en main du sujet, lecture complète du README et du découpage des responsabilités. Création du repository git, des dossiers et fichiers.
- **09h15** : Répartition des rôles :
  - Clément → gestion des `Dockerfile` pour `gateway-service` et `stats-service`. Gestion des différents fichiers .md .
  - Émilien → développement Flask (routes, logique JWT, proxy...).
  - Guillaume → mise en place du `docker-compose.yml`, configuration Traefik, tests de connectivité entre services.
- **10h40** : Premier build Docker réussi le gateway-service.
- **11h10** : Intégration de Traefik dans le `docker-compose.yml`, ajout des labels pour le `gateway-service`.

