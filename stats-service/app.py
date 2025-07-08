"""
stats-service — Application Flask

Ce microservice expose des routes statistiques accessibles via :
  - /stats/active-channels
  - /stats/message-per-user
  - /stats/hourly-activity
  - /stats/top-reacted-messages

Chacune de ces routes :
  - récupère les messages auprès du `message-service`
  - traite les données pour produire une statistique spécifique
  - retourne les résultats au format JSON
  - exige un token JWT valide transmis dans l'en-tête Authorization

Le JWT est vérifié via la fonction `verify_token()` importée depuis auth.py.
"""

from flask import Flask, jsonify, request
from collections import defaultdict
from auth import verify_token
import os
import requests

# Initialisation de l'application Flask
app = Flask(__name__)

# URL du message-service, récupérée depuis les variables d’environnement
MESSAGE_SERVICE_URL = os.getenv("MESSAGE_SERVICE_URL", "http://message-service:5002")


def get_messages():
    """
    Récupère la liste des messages depuis le message-service.

    Effectue une requête GET sur /msg?channel=tech (canal "tech" par défaut).

    Retour :
        - Une liste de messages (list[dict])
        - Lève une RuntimeError en cas d’échec réseau ou HTTP
    """
    try:
        response = requests.get(f"{MESSAGE_SERVICE_URL}/msg?channel=tech")
        response.raise_for_status()
        return response.json().get("result", [])
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur lors de la requête vers message-service : {str(e)}")


def check_token():
    """
    Vérifie le token JWT envoyé dans l'en-tête Authorization.

    Extrait le token de l’en-tête "Authorization: Bearer <token>".
    Passe ce token à la fonction `verify_token()` définie dans auth.py.

    Retour :
        - None si le token est valide
        - jsonify({ "error": ... }), 401 si le token est invalide ou manquant
    """
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    result = verify_token({"token": token})

    if not result["valid"]:
        return jsonify({"error": result["error"]}), 401
    return None  # OK


@app.route("/stats/active-channels")
def stats_active_channels():
    """
    GET /stats/active-channels

    Calcule le nombre de messages par canal.

    Exemple de retour :
    {
      "result": [
        {"channel": "tech", "messages": 12},
        {"channel": "général", "messages": 5}
      ]
    }
    """
    error = check_token()
    if error:
        return error
    try:
        messages = get_messages()
        compte = defaultdict(int)
        for msg in messages:
            canal = msg.get("channel", "inconnu")
            compte[canal] += 1
        result = [{"channel": ch, "messages": n} for ch, n in compte.items()]
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats/message-per-user")
def stats_message_per_user():
    """
    GET /stats/message-per-user

    Calcule le nombre de messages envoyés par utilisateur.

    Exemple de retour :
    {
      "result": [
        {"user": "roger", "messages": 8},
        {"user": "ginette", "messages": 3}
      ]
    }
    """
    error = check_token()
    if error:
        return error
    try:
        messages = get_messages()
        compte = defaultdict(int)
        for msg in messages:
            auteur = msg.get("from", "inconnu")
            compte[auteur] += 1
        result = [{"user": u, "messages": n} for u, n in compte.items()]
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats/hourly-activity")
def stats_hourly_activity():
    """
    GET /stats/hourly-activity

    Regroupe les messages par heure d’envoi.

    Exemple de retour :
    {
      "result": [
        {"hour": "2025-07-08T10", "messages": 4},
        {"hour": "2025-07-08T11", "messages": 7}
      ]
    }

    L'heure est extraite du champ timestamp (format ISO 8601).
    """
    error = check_token()
    if error:
        return error
    try:
        messages = get_messages()
        compte = defaultdict(int)
        for msg in messages:
            heure = msg.get("timestamp", "")[:13]  # ex : "2025-07-08T11"
            compte[heure] += 1
        result = [{"hour": h, "messages": n} for h, n in sorted(compte.items())]
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats/top-reacted-messages")
def stats_top_reacted_messages():
    """
    GET /stats/top-reacted-messages

    Retourne les 10 messages ayant reçu le plus de réactions.

    Chaque message est représenté par :
      - son id
      - son texte
      - le total de réactions

    Exemple de retour :
    {
      "result": [
        {"id": "abc123", "text": "hello", "reactions": 5},
        ...
      ]
    }
    """
    error = check_token()
    if error:
        return error
    try:
        messages = get_messages()
        scores = []
        for msg in messages:
            total = sum(len(p) for p in msg.get("reactions", {}).values())
            scores.append({
                "id": msg.get("id"),
                "text": msg.get("text", ""),
                "reactions": total
            })
        top = sorted(scores, key=lambda m: -m["reactions"])[:10]
        return jsonify({"result": top})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(500)
def handle_500(error):
    """
    Gestion centralisée des erreurs internes du serveur (500).
    """
    return jsonify({"error": "Erreur interne du serveur"}), 500


if __name__ == "__main__":
    # Lancement local du serveur Flask (utile pour les tests hors Docker)
    app.run(host="0.0.0.0", port=5005)
