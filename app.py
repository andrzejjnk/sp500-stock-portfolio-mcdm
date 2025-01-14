import streamlit as st
from app_utils.pages.main_page import main_page
from app_utils.pages.topsis_page import topsis_page
from app_utils.pages.aras_page import aras_page
from app_utils.pages.vikor_page import vikor_page
from app_utils.pages.copras_page import copras_page
from app_utils.pages.waspas_page import waspas_page
from app_utils.pages.taxonomy_page import taxonomy_page
from app_utils.pages.aggregation_page import aggregation_page
from app_utils.pages.visualizations_pages import visualizations_page
from app_utils.pages.forecast_page import forecast_page

st.set_page_config(
    page_title="SP500 Portfolio Optimization",
    page_icon="📈",
    layout="wide",
)

with st.sidebar:
    tabs = st.radio(
        "Navigate", 
        ["Main Page", "Forecast", "TOPSIS", "TAXONOMY", "ARAS", "VIKOR", "COPRAS", "WASPAS", "AGGREGATION", "VISUALIZATIONS"],
        index=0
    )

if tabs == "Main Page":
    main_page()

elif tabs == "Forecast":
    forecast_page()

elif tabs == "TOPSIS":
    topsis_page()

elif tabs == "ARAS":
    aras_page()

elif tabs == "TAXONOMY":
    taxonomy_page()

elif tabs == "VIKOR":
    vikor_page()

elif tabs == "COPRAS":
    copras_page()

elif tabs == "WASPAS":
    waspas_page()

elif tabs == "AGGREGATION":
    aggregation_page()

elif tabs == "VISUALIZATIONS":
    visualizations_page()