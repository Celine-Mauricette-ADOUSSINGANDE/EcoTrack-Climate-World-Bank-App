import os
import time
import pandas as pd
from typing import Optional
from config import logger

# Import de votre librairie personnalisée
try:
    # On utilise le chemin complet vers le module web_api pour plus de sécurité
    from co2_extractor.web_api import CO2Extractor
except ImportError:
    logger.error("CRITIQUE : La librairie 'co2-extractor-wb' n'est pas installée.")
    logger.info("Conseil : Allez dans le dossier 'co2-extractor-wb' et lancez 'pip install -e .'")
    CO2Extractor = None  # Évite une NameError plus bas

def is_cache_valid(filepath: str, max_days: int = 7) -> bool:
    """Vérifie si le fichier de cache existe et s'il est récent."""
    if not os.path.exists(filepath):
        return False
    
    file_age_seconds = time.time() - os.path.getmtime(filepath)
    return file_age_seconds < (max_days * 86400)

def fetch_world_bank_data(indicator: str, country: str = "all", force_refresh: bool = False) -> Optional[pd.DataFrame]:
    """
    Récupère les données en utilisant la librairie personnalisée avec un système de cache.
    """
    # Préparation du chemin du cache
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    
    # Nettoyage du nom de fichier (certains indicateurs ont des points)
    cache_filename = f"{indicator}.csv"
    cache_path = os.path.join(raw_dir, cache_filename)

    # 1. Vérification du cache local
    if not force_refresh and is_cache_valid(cache_path, max_days=7):
        logger.info(f"INDICATEUR [{indicator}] : Chargement depuis le CACHE local.")
        try:
            return pd.read_csv(cache_path)
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du cache {cache_path}: {e}")

    # 2. Vérification de la présence de la librairie
    if CO2Extractor is None:
        logger.error(f"Action impossible : La librairie est manquante pour l'indicateur {indicator}")
        return None

    # 3. Appel de VOTRE librairie
    logger.info(f"INDICATEUR [{indicator}] : Appel de la LIBRAIRIE externe...")
    try:
        df = CO2Extractor.get_co2_data(indicator=indicator, country=country)

        if df is not None and not df.empty:
            # Sauvegarde dans le cache pour la prochaine fois
            df.to_csv(cache_path, index=False)
            logger.info(f"INDICATEUR [{indicator}] : Données mises en CACHE avec succès.")
            return df
        else:
            logger.warning(f"INDICATEUR [{indicator}] : La librairie n'a trouvé aucune donnée.")
            # Secours : on tente de charger un vieux cache s'il existe
            if os.path.exists(cache_path):
                logger.warning(f"INDICATEUR [{indicator}] : Utilisation du cache existant (données potentiellement anciennes).")
                return pd.read_csv(cache_path)
            return None

    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de la librairie pour {indicator} : {e}")
        return None

def save_raw_data(df: pd.DataFrame, filename: str) -> None:
    """Sauvegarde manuelle d'un DataFrame dans le dossier data/raw."""
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    path = os.path.join(raw_dir, filename)
    try:
        df.to_csv(path, index=False)
        logger.info(f"Sauvegarde manuelle réussie : {path}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde manuelle : {e}")