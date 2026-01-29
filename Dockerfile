# Image de base légère
FROM python:3.11-slim

# Dossier de travail dans le container
WORKDIR /app

# Installation des dépendances système (nécessaires pour certaines libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie et installation de VOTRE bibliothèque locale
COPY co2-extractor-wb/ ./co2-extractor-wb/
RUN pip install -e ./co2-extractor-wb

# Copie de tout le reste du projet
COPY . .

# Création des dossiers de données pour éviter les erreurs de permission
RUN mkdir -p data/raw data/processed

# Port utilisé par Streamlit
EXPOSE 8501

# Commande de lancement : 
# 1. On exécute main.py pour générer les données
# 2. On lance l'interface Streamlit
CMD ["sh", "-c", "python main.py && streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]