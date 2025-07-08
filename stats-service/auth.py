import jwt

SECRET_KEY = "on-ny-arrivera-jamais-enfin-peut-etre"
ALGORITHM = "HS256"

def verify_token(input_json: dict):

    token = input_json.get("token", "")
    if not token:
        return {"valid": False, "error": "Aucun token fourni"}

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"valid": True, "payload": payload}

    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token expiré"}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Token invalide"}
