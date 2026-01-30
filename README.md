# 🌍 EcoTrack: Climate Impact Analysis App

👥 **Équipe (Groupe)**

- Céline ADOUSSINGANDE - [mauriceteadoussingande@yahoo.com]
- Loukmane BOULANKI [loukmane.boulanki@etu.univ-amu.fr]
- Isaac BESSANH [isaac.bessanh@etu.univ-amu.fr]

📝 **Présentation du Projet**

EcoTrack est une application de données complète permettant de traiter, analyser et visualiser l'impact climatique mondial. L'application compare les indicateurs environnementaux (émissions de CO2, gaz à effet de serre, déforestation) avec des indicateurs économiques (PIB par habitant) pour identifier des corrélations.

L'application s'appuie sur une bibliothèque Python personnalisée développée par nos soins et publiée sur PyPI pour l'extraction des données de la Banque Mondiale.


**Indicateurs**

- "co2_per_capita": "EN.GHG.CO2.PC.CE.AR5",   # CO2 par habitant

- "forest_area": "AG.LND.FRST.ZS",            # Surface forestière (%)

- "gdp_per_capita": "NY.GDP.PCAP.CD",         # PIB par habitant

- "total_ghg": "EN.GHG.ALL.MT.CE.AR5"         # Emissions totales de GES (Mt)


# Exemple pour le PIB de la France uniquement

df_fr_gdp = CO2Extractor.get_co2_data(indicator="NY.GDP.PCAP.CD", country="FR")

🛠 Développement (Installation locale)


🔗 **Liens du Projet**

- Dépôt GitHub Public : https://github.com/Celine-Mauricette-ADOUSSINGANDE/
EcoTrack-Climate-World-Bank-App

- Bibliothèque PyPI : https://pypi.org/project/co2-extractor-wb/

- Image Docker Hub  : https://hub.docker.com/repository/docker/montcho/eco-track-app/general


🛠 **Technologies Utilisées**
- Backend : Python 3.11+
- Analyse de données : Pandas
- Visualisation : Streamlit, Plotly
- Containerisation : Docker, Docker Compose
- Gestion d'API : Bibliothèque co2-extractor-wb (Source : World Bank API)


🏗 **Structure du Projet**

FINAL_PROJECT/

├── Dockerfile              # Configuration de l'image Docker

├── compose.yml             # Orchestration des services

├── requirements.txt        # Dépendances Python

├── main.py                 # Script principal d'acquisition/analyse

├── config.py               # Configuration et Logging

├── app/

│   └── streamlit_app.py    # Interface utilisateur Streamlit

├── src/

│   ├── data_loader.py      # Module d'acquisition (utilise la lib PyPI)

│   ├── processor.py        # Module de nettoyage des données

│   └── analyzer.py         # Module d'analyse statistique

├── data/

│   ├── raw/                # Données brutes (ignorées par Git si > 5Mo)

│   └── processed/          # Données nettoyées et tendances

└── co2-extractor-wb/       # Code source de la bibliothèque personnalisée


## 🐳 Docker Hub
Retrouvez l'image Docker de l'application ici :  
https://hub.docker.com/repository/docker/montcho/eco-track-app/general

Vous pouvez également récupérer l'image directement avec la commande :
*docker pull montcho/eco-track-app:latest*


🚀 **Installation et Utilisation**

1. **Utilisation avec Docker** 
Le projet est entièrement containerisé. Pour lancer l'application sans installer Python, faites ce qui suit:


🚀 **Lancement rapide (Docker Hub)**
Si vous avez Docker, vous pouvez lancer mon application sans télécharger le code source :
*docker run -p 8501:8501 montcho/eco-track-app:latest*
Une fois le processus terminé, l'application est accessible sur : http://localhost:8501


2. **Installation Locale (Développement)**
Si vous souhaitez lancer le projet manuellement :

- Créez un environnement virtuel : python -m venv venv
- Activez-le : .\venv\Scripts\activate (Windows) ou source venv/bin/activate (Mac/Linux)
- Installez les dépendances : pip install -r requirements.txt
- Installez la bibliothèque locale : pip install -e ./co2-extractor-wb
- Lancez le pipeline de données : python main.py
- Lancez l'interface : streamlit run app/streamlit_app.py


📊 **Fonctionnalités Clés**
- Multi-Indicateurs : Analyse du CO2, du PIB, de la surface forestière et des gaz à effet de serre.
- Comparaison Interactive : Sélection dynamique de pays pour comparer leurs trajectoires historiques.
- Moyenne Mondiale : Comparaison automatique des performances d'un pays par rapport à la tendance globale.
- Analyse de Corrélation : Visualisation de l'impact du développement économique (PIB) sur les émissions de CO2.



💡 **Bonnes Pratiques Respectées**
- Qualité du code : Utilisation de Type Hints, Docstrings et respect de la PEP 8.
- Logging : Suivi complet des étapes d'acquisition et de traitement via le module logging.
- Gestion du Cache : Système de cache local pour limiter les appels aux API externes et permettre un mode dégradé.
- Docker : Image optimisée (slim) avec gestion des volumes pour la persistence des données.