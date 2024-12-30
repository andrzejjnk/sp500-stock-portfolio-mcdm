import streamlit as st
from app_utils.pages.topsis_page import topsis_page
from app_utils.pages.aras_page import aras_page
from app_utils.pages.vikor_page import vikor_page
from app_utils.pages.copras_page import copras_page
from app_utils.pages.waspas_page import waspas_page

st.set_page_config(
    page_title="SP500 Portfolio Optimization",
    page_icon="📈",
    layout="wide",
)

with st.sidebar:
    tabs = st.radio(
        "Navigate", 
        ["Main Page", "TOPSIS", "ARAS", "VIKOR", "COPRAS", "WASPAS"],
        index=0
    )


if tabs == "Main Page":
    st.title("📊 SP500 Portfolio Optimization using MCDM methods")
    st.write("""
    Welcome to the SP500 Portfolio Optimization application!  
    Several MCDM methods are being used to help identify the best companies based on multi-criteria decision-making analyses.  
    Use the sidebar menu to navigate to the analysis results.
    """)

elif tabs == "TOPSIS":
    topsis_page()

elif tabs == "ARAS":
    aras_page()

elif tabs == "VIKOR":
    vikor_page()

elif tabs == "COPRAS":
    copras_page()

elif tabs == "WASPAS":
    waspas_page()