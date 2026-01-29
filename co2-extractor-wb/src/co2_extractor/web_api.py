import requests
import pandas as pd
import logging
from typing import Optional

# Configuration du logger
logger = logging.getLogger(__name__)

class CO2Extractor:
    """Librairie pour extraire les données climatiques et économiques de la Banque Mondiale."""
    
    BASE_URL = "https://api.worldbank.org/v2"

    @staticmethod
    def get_co2_data(indicator: str, country: str = "all") -> Optional[pd.DataFrame]:
        """
        Récupère les données d'un indicateur en testant les différentes sources (WDI et Climate).
        """
        # Ordre de test : 
        # 1. Sans source (Auto-détection)
        # 2. Source 2 (Pour PIB et Forêt)
        # 3. Source 40 (Pour GES et CO2 AR5)
        sources = ["", "&source=2", "&source=40"]
        
        for src_param in sources:
            url = f"{CO2Extractor.BASE_URL}/country/{country}/indicator/{indicator}?format=json&per_page=16000{src_param}"
            
            try:
                logger.info(f"[LIB] Tentative sur : {url}")
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                data = response.json()

                # Une réponse valide de la BM est une liste : [metadata, data_list]
                if isinstance(data, list) and len(data) > 1 and data[1] is not None:
                    df = pd.DataFrame(data[1])
                    if not df.empty:
                        logger.info(f"[LIB] Succès pour {indicator} avec la source '{src_param}'")
                        return df
                
                # Si l'API renvoie un message d'erreur spécifique
                if isinstance(data, list) and len(data) == 1 and 'message' in data[0]:
                    msg = data[0]['message'][0].get('value', 'Erreur')
                    logger.debug(f"[LIB] Source {src_param} rejetée : {msg}")
                    continue

            except Exception as e:
                logger.error(f"[LIB] Erreur sur {url} : {e}")
                continue
        
        logger.error(f"[LIB] Échec définitif pour l'indicateur : {indicator}")
        return None