FROM python:3.13.5-slim

# Définit le dossier de travail dans le conteneur
WORKDIR .

# Copie les dépendances et les installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source de l’application dans le conteneur
COPY . .

# Commande par défaut au lancement du conteneur
CMD ["python", "app.py"]