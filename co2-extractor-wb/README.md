# CO2 Extractor WB
Librairie d'extraction de données CO2 de la Banque Mondiale.

📦 co2-extractor-wb
![alt text](https://img.shields.io/pypi/v/co2-extractor-wb.svg)

![alt text](https://img.shields.io/pypi/pyversions/co2-extractor-wb.svg)
co2-extractor-wb est une bibliothèque Python légère et robuste conçue pour extraire facilement des indicateurs climatiques et économiques depuis l'API de la Banque Mondiale. Elle gère automatiquement les basculements entre les sources de données (WDI et Climate Change) pour garantir un accès fiable aux données.
✨ Fonctionnalités
🚀 Extraction Simplifiée : Récupérez des données complexes en une seule ligne de code.
🔄 Multi-Source : Gère intelligemment les codes sources de la Banque Mondiale (Source 2, Source 40).
📊 Format Pandas : Retourne directement des DataFrames Pandas prêts pour l'analyse.
🌍 Couverture Mondiale : Accès à plus de 260 pays et régions depuis 1960.
⚙️ Pagination Automatique : Récupère jusqu'à 16 000 enregistrements par appel pour éviter les données tronquées.
🛠 Installation
Vous pouvez installer la bibliothèque via pip :
code
Bash
pip install co2-extractor-wb
🚀 Utilisation Rapide
Voici comment extraire les émissions de CO2 par habitant pour tous les pays :
code
Python
from co2_extractor import CO2Extractor

# Initialisation de l'extracteur et récupération des données
# Indicateur : EN.GHG.CO2.PC.CE.AR5 (CO2 par habitant)
df = CO2Extractor.get_co2_data(indicator="EN.GHG.CO2.PC.CE.AR5")

if df is not None:
    print(df.head())
    # Sauvegarder en CSV
    df.to_csv("data_co2.csv", index=False)
💡 Exemples d'Indicateurs
Vous pouvez utiliser n'importe quel code d'indicateur de la Banque Mondiale :
Indicateur	Code	Source recommandée
CO2 par habitant	EN.GHG.CO2.PC.CE.AR5	Climate (40)
Surface Forestière	AG.LND.FRST.ZS	WDI (2)
PIB par habitant	NY.GDP.PCAP.CD	WDI (2)
Total GES	EN.ATM.GHGT.KT.CE	Climate (40)
code
Python
# Exemple pour le PIB de la France uniquement
df_fr_gdp = CO2Extractor.get_co2_data(indicator="NY.GDP.PCAP.CD", country="FR")
🛠 Développement (Installation locale)
Si vous souhaitez contribuer ou modifier la librairie localement :
code
Bash
git clone https://github.com/votre-compte/co2-extractor-wb.git
cd co2-extractor-wb
pip install -e .
📝 License
Distribué sous la licence MIT. Voir LICENSE pour plus d'informations.
👥 Auteurs
Céline ADOUSSINGANDE -  mauriceteadoussingande@yahoo.com
