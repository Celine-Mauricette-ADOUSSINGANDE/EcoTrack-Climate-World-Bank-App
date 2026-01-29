import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuration de la page
st.set_page_config(
    page_title="EcoTrack: Climate Impact Analysis",
    layout="wide",
    page_icon="🌍"
)

# Style CSS pour améliorer l'apparence (Correction du paramètre unsafe_allow_html)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Fonctions de chargement des données
@st.cache_data
def load_processed_data(indicator_name, data_type="cleaned"):
    """Charge les fichiers CSV depuis data/processed/."""
    file_path = f"data/processed/{indicator_name}_{data_type}.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

# 3. Sidebar - Configuration
st.sidebar.title("🌿 Configuration")

# Mapping des noms lisibles vers les noms de fichiers
indicator_map = {
    "CO2 par habitant": "co2_per_capita",
    "Surface Forestière (%)": "forest_area",
    "PIB par habitant ($)": "gdp_per_capita",
    "Émissions totales GES (Mt)": "total_ghg"
}

display_name = st.sidebar.selectbox(
    "Indicateur à visualiser :",
    options=list(indicator_map.keys())
)
indicator_selected = indicator_map[display_name]

# Chargement des données sélectionnées
df_main = load_processed_data(indicator_selected, "cleaned")
df_trends = load_processed_data(indicator_selected, "global_trends")

if df_main is not None:
    # --- GESTION SÉCURISÉE DES PAYS PAR DÉFAUT ---
    countries_available = sorted(df_main['country'].unique())
    
    # Liste de pays cibles pour l'affichage initial
    desired_defaults = ["France", "United States", "China", "Brazil", "India"]
    
    # On vérifie dynamiquement quels pays cibles existent dans les données actuelles
    valid_defaults = [c for c in desired_defaults if c in countries_available]

    selected_countries = st.sidebar.multiselect(
        "Sélectionnez les pays à comparer :",
        options=countries_available,
        default=valid_defaults
    )

    # 4. Interface Principale
    st.title(f"🌍 EcoTrack : {display_name}")
    st.markdown(f"Analyse des données historiques pour l'indicateur sélectionné.")

    # KPI Metrics (Dernière année disponible)
    latest_year = df_main['year'].max()
    avg_val = df_main[df_main['year'] == latest_year]['value'].mean()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Dernière année disponible", int(latest_year))
    m2.metric("Moyenne (Sélection)", f"{avg_val:.2f}")
    m3.metric("Total Pays", len(countries_available))

    # 5. Graphique Temporel
    st.divider()
    
    filtered_df = df_main[df_main['country'].isin(selected_countries)]
    
    if not filtered_df.empty:
        fig = px.line(
            filtered_df,
            x="year",
            y="value",
            color="country",
            title=f"Évolution temporelle : {display_name}",
            labels={"value": "Valeur", "year": "Année"},
            template="plotly_white",
            markers=True
        )

        # Ajout de la ligne de tendance mondiale (Moyenne calculée par analyzer.py)
        if df_trends is not None:
            fig.add_scatter(
                x=df_trends['year'], 
                y=df_trends['value'], 
                name="MOYENNE MONDIALE",
                line=dict(color='black', width=3, dash='dash'),
                mode='lines'
            )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Veuillez sélectionner au moins un pays dans la barre latérale.")

    # 6. Analyse de Corrélation (PIB vs CO2)
    # On n'affiche ce bloc que si on n'est pas déjà sur le PIB ou le CO2 pour éviter les doublons
    st.divider()
    st.subheader("📊 Focus : Richesse économique vs Impact CO2")
    
    df_gdp = load_processed_data("gdp_per_capita", "cleaned")
    df_co2 = load_processed_data("co2_per_capita", "cleaned")

    if df_gdp is not None and df_co2 is not None:
        # Fusion des données sur le pays et l'année (Inner Join)
        merged = pd.merge(df_gdp, df_co2, on=['country', 'year'], suffixes=('_gdp', '_co2'))
        
        # On utilise la dernière année commune
        last_year_merged = merged['year'].max()
        df_scatter = merged[merged['year'] == last_year_merged]

        fig_scatter = px.scatter(
            df_scatter,
            x="value_gdp",
            y="value_co2",
            size="value_co2",
            color="country",
            hover_name="country",
            log_x=True, # PIB en échelle log pour une meilleure lisibilité
            title=f"Lien entre PIB/Habitant et CO2/Habitant ({int(last_year_merged)})",
            labels={"value_gdp": "PIB par habitant ($)", "value_co2": "CO2 par habitant (tonnes)"},
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.info("ℹ️ L'axe du PIB est en échelle logarithmique pour comparer équitablement les pays.")

    # 7. Affichage des données brutes
    with st.expander("🔎 Explorer les données brutes"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.error("⚠️ Données introuvables.")
    st.info("Veuillez exécuter le script 'python main.py' pour générer les fichiers de données.")