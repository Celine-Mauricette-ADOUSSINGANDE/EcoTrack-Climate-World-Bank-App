import pandas as pd
from config import logger

def clean_climate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données brutes de la Banque Mondiale de manière générique.
    Fonctionne pour le CO2, le PIB, la Forêt et les GES.
    """
    if df is None or df.empty:
        logger.warning("Le DataFrame est vide, nettoyage annulé.")
        return pd.DataFrame()

    logger.info("Début du nettoyage des données...")
    
    try:
        # 1. Extraction sécurisée du nom et du code du pays
        # On vérifie que 'x' est bien un dictionnaire avant d'extraire
        df['country_name'] = df['country'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
        df['country_code'] = df['country'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
        
        # 2. Sélection des colonnes utiles
        # On utilise 'value' comme nom générique pour que ça marche pour TOUS les indicateurs
        df_cleaned = df[['country_name', 'country_code', 'date', 'value']].copy()
        df_cleaned.columns = ['country', 'code', 'year', 'value'] # <--- NOM GÉNÉRIQUE
        
        # 3. Conversion propre des types
        # errors='coerce' transforme les valeurs invalides en NaN (évite les plantages)
        df_cleaned['year'] = pd.to_numeric(df_cleaned['year'], errors='coerce')
        df_cleaned['value'] = pd.to_numeric(df_cleaned['value'], errors='coerce')
        
        # 4. Suppression des lignes sans valeur ou sans pays
        df_cleaned = df_cleaned.dropna(subset=['value', 'country'])
        
        # 5. Tri par pays et par année (plus récent en dernier)
        df_cleaned = df_cleaned.sort_values(['country', 'year'])
        
        logger.info(f"Nettoyage terminé. {len(df_cleaned)} lignes valides conservées.")
        return df_cleaned

    except Exception as e:
        logger.error(f"Erreur lors du nettoyage : {e}")
        return pd.DataFrame()