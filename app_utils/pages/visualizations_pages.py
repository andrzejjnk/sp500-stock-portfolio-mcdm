import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import shutil
import os

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.visualizations.visualizations import plot_mcdm_heatmap, plot_borda_copeland_scores, plot_radar_chart, save_plot_to_bytes


def save_and_move_file(file_data, file_name):
    target_directory = PROJECT_ROOT / "results" / "visualizations"
    target_directory.mkdir(parents=True, exist_ok=True)
    
    file_path = target_directory / file_name
    
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    return file_path

def visualizations_page():
    st.title("Visualizations of SP500 Rankings")

    # Load data
    mcdm_file = "results/mcdm_rankings.csv"
    aggregated_file = "results/aggregated_rankings.csv"

    try:
        rankings_df = pd.read_csv(mcdm_file)
        aggregated_df = pd.read_csv(aggregated_file)
    except FileNotFoundError:
        st.error("One or both required files (mcdm_rankings.csv, aggregated_rankings.csv) not found.")
        return

    method_names = ["TOPSIS", "ARAS", "VIKOR", "COPRAS", "WASPAS", "TAXONOMY"]

    # Heatmap for MCDM Rankings
    st.write("### Heatmap of Rankings Across MCDM Methods")
    top_n = st.slider("Select the number of top companies to display:", min_value=1, max_value=len(rankings_df['Symbol']), value=10)
    heatmap_plot = plot_mcdm_heatmap(rankings_df, method_names, top_n=top_n)
    st.plotly_chart(heatmap_plot, use_container_width=True)
    
    heatmap_data = save_plot_to_bytes(heatmap_plot)
    if st.download_button(
        label="Download Heatmap",
        data=heatmap_data,
        file_name=f"mcdm_rankings_heatmap_top_{top_n}.png",
        mime="image/png",
    ):
        file_path = save_and_move_file(heatmap_data, f"mcdm_rankings_heatmap_top_{top_n}.png")
        st.success(f"Heatmap saved to {file_path}")
        
    # Bar plot for Borda and Copeland Scores
    st.write("### Borda and Copeland Scores")
    borda_copeland_plot = plot_borda_copeland_scores(aggregated_df, top_n=top_n)
    st.plotly_chart(borda_copeland_plot, use_container_width=True)
    
    borda_copeland_data = save_plot_to_bytes(borda_copeland_plot)
    if st.download_button(
        label="Download Borda and Copeland Scores Plot",
        data=borda_copeland_data,
        file_name="borda_copeland_scores.png",
        mime="image/png",
    ):
        file_path = save_and_move_file(borda_copeland_data, "borda_copeland_scores.png")
        st.success(f"Borda and Copeland Scores Plot saved to {file_path}")

    # Radar Chart for a Selected Company
    st.write("### Radar Chart for Aggregated Scores")
    company_name = st.selectbox(
        "Select a company to view its radar chart:",
        aggregated_df["Company Name"].unique()
    )
    radar_chart = plot_radar_chart(company_name, aggregated_df)
    st.plotly_chart(radar_chart, use_container_width=True)
    
    radar_data = save_plot_to_bytes(radar_chart)
    if st.download_button(
        label=f"Download Radar Chart for {company_name}",
        data=radar_data,
        file_name=f"{company_name.replace(' ', '_').lower()}_radar_chart.png",
        mime="image/png",
    ):
        file_name = f"{company_name.replace(' ', '_').lower()}_radar_chart.png"
        file_path = save_and_move_file(radar_data, file_name)
        st.success(f"Radar chart saved to {file_path}")
