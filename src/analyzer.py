import pandas as pd
from typing import Optional
from config import logger

def calculate_global_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la moyenne mondiale par année pour un indicateur donné.
    """
    try:
        if df.empty:
            return pd.DataFrame()
        
        # S'assurer que les données sont numériques avant de calculer la moyenne
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Groupement par année et calcul de la moyenne mondiale
        trends = df.groupby('year')['value'].mean().reset_index()
        logger.info(f"Tendances mondiales calculées sur {len(trends)} années.")
        return trends
    except Exception as e:
        logger.error(f"Erreur lors du calcul des tendances mondiales : {e}")
        return pd.DataFrame()

def get_top_countries(df: pd.DataFrame, year: int, n: int = 10) -> pd.DataFrame:
    """
    Récupère les N pays ayant les valeurs les plus élevées (ou faibles) pour une année.
    Renommé 'countries' au lieu de 'polluters' pour être générique (PIB, Forêt, etc.).
    """
    try:
        if df.empty:
            return pd.DataFrame()

        # Filtrage sur l'année demandée
        year_data = df[df['year'] == year]
        
        if year_data.empty:
            logger.warning(f"Aucune donnée disponible pour l'année {year}.")
            return pd.DataFrame()

        # Récupération des N plus grandes valeurs
        result = year_data.nlargest(n, 'value')[['country', 'code', 'value']]
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du Top {n} : {e}")
        return pd.DataFrame()

def calculate_correlation(df1: pd.DataFrame, df2: pd.DataFrame, label1: str, label2: str) -> pd.DataFrame:
    """
    Fusionne deux indicateurs pour analyser leur corrélation (ex: PIB vs CO2).
    """
    try:
        if df1.empty or df2.empty:
            logger.warning("L'un des DataFrames est vide. Corrélation impossible.")
            return pd.DataFrame()

        # Fusion (Inner Join) sur le pays et l'année pour avoir des points de données comparables
        merged = pd.merge(
            df1, 
            df2, 
            on=['country', 'code', 'year'], 
            suffixes=(f'_{label1}', f'_{label2}')
        )
        
        logger.info(f"Fusion réussie pour corrélation : {len(merged)} points de données communs.")
        return merged
    except Exception as e:
        logger.error(f"Erreur lors de la fusion pour corrélation : {e}")
        return pd.DataFrame()