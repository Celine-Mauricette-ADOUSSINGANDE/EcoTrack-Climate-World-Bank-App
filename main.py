import os  
from src.data_loader import fetch_world_bank_data
from src.processor import clean_climate_data
from src.analyzer import calculate_global_trends 
from config import logger

def main():
    # 1. Création des dossiers de données s'ils n'existent pas
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # 2. Liste de vos 4 indicateurs
    indicators = {
        "co2_per_capita": "EN.GHG.CO2.PC.CE.AR5",   # CO2 par habitant
        "forest_area": "AG.LND.FRST.ZS",            # Surface forestière (%)
        "gdp_per_capita": "NY.GDP.PCAP.CD",         # PIB par habitant
        "total_ghg": "EN.GHG.ALL.MT.CE.AR5"         # Emissions totales de GES (Mt)
    }

    logger.info("DÉMARRAGE DU PIPELINE D'ACQUISITION ET D'ANALYSE")

    for name, code in indicators.items():
        logger.info(f"--- Analyse de l'indicateur : {name} ({code}) ---")
        
        # 3. Acquisition via la librairie (avec gestion du cache)
        raw_df = fetch_world_bank_data(code)

        if raw_df is not None:
            # 4. Nettoyage générique
            cleaned_df = clean_climate_data(raw_df)
            
            if not cleaned_df.empty:
                # 5. Sauvegarde du fichier nettoyé
                output_path = f"data/processed/{name}_cleaned.csv"
                cleaned_df.to_csv(output_path, index=False)
                logger.info(f"SUCCÈS : Fichier nettoyé créé : {output_path}")

                # 6. ÉTAPE D'ANALYSE : Calcul des tendances mondiales
                logger.info(f"Calcul des tendances mondiales pour {name}...")
                trends_df = calculate_global_trends(cleaned_df)
                
                if not trends_df.empty:
                    # Sauvegarde des tendances
                    trends_path = f"data/processed/{name}_global_trends.csv"
                    trends_df.to_csv(trends_path, index=False)
                    logger.info(f"SUCCÈS : Fichier de tendances créé : {trends_path}")
                else:
                    logger.warning(f"Impossible de calculer les tendances pour {name}")

            else:
                logger.warning(f"Le nettoyage a renvoyé un résultat vide pour {name}.")
        else:
            logger.error(f"ÉCHEC : Impossible de récupérer l'indicateur {name}.")

    logger.info("PIPELINE TERMINÉ AVEC SUCCÈS.")

if __name__ == "__main__":
    main()