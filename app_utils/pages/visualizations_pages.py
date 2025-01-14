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

def display_visualizations(mcdm_file, aggregated_file, title):
    st.write(f"### {title} Visualizations")

    try:
        rankings_df = pd.read_csv(mcdm_file)
        aggregated_df = pd.read_csv(aggregated_file)
    except FileNotFoundError:
        st.error(f"One or both required files ({mcdm_file}, {aggregated_file}) not found.")
        return

    method_names = ["TOPSIS", "ARAS", "VIKOR", "COPRAS", "WASPAS", "TAXONOMY"]

    # Heatmap for MCDM Rankings
    st.write(f"### Heatmap of Rankings Across MCDM Methods ({title} Data)")
    top_n = st.slider(f"Select the number of top companies to display for {title}:", min_value=1, max_value=len(rankings_df['Symbol']), value=10, key=f"top_n_{title}")
    heatmap_plot = plot_mcdm_heatmap(rankings_df, method_names, top_n=top_n, data_type=title)
    st.plotly_chart(heatmap_plot, use_container_width=True)

    heatmap_data = save_plot_to_bytes(heatmap_plot)
    if st.button(f"Save {title} Heatmap"):
        file_path = save_and_move_file(heatmap_data, f"{title.lower()}_mcdm_rankings_heatmap_top_{top_n}.png")
        st.success(f"{title} Heatmap saved to {file_path}")

    # Bar plot for Borda and Copeland Scores
    st.write(f"### Borda and Copeland Scores ({title} Data)")
    borda_copeland_plot = plot_borda_copeland_scores(aggregated_df, top_n=top_n, data_type=title)
    st.plotly_chart(borda_copeland_plot, use_container_width=True)

    borda_copeland_data = save_plot_to_bytes(borda_copeland_plot)
    if st.button(f"Save {title} Borda and Copeland Scores Plot"):
        file_path = save_and_move_file(borda_copeland_data, f"{title.lower()}_borda_copeland_scores.png")
        st.success(f"{title} Borda and Copeland Scores Plot saved to {file_path}")

    # Radar Chart for a Selected Company
    st.write(f"### Radar Chart for Aggregated Scores ({title} Data)")
    company_name = st.selectbox(
        f"Select a company to view its {title} radar chart:",
        aggregated_df["Company Name"].unique(),
        key=f"company_select_{title}"
    )
    radar_chart = plot_radar_chart(company_name, aggregated_df, data_type=title)
    st.plotly_chart(radar_chart, use_container_width=True)

    radar_data = save_plot_to_bytes(radar_chart)
    if st.button(f"Save {title} Radar Chart for {company_name}"):
        file_name = f"{title.lower()}_{company_name.replace(' ', '_').lower()}_radar_chart.png"
        file_path = save_and_move_file(radar_data, file_name)
        st.success(f"{title} Radar chart saved to {file_path}")

def visualizations_page():
    st.title("Visualizations of SP500 Rankings")

    # Load data
    mcdm_file = "results/normal_mcdm_rankings.csv"
    aggregated_file = "results/normal_aggregated_rankings.csv"
    forecasted_mcdm_file = "results/forecasted_mcdm_rankings.csv"
    forecasted_aggregated_file = "results/forecasted_aggregated_rankings.csv"

    display_visualizations(mcdm_file, aggregated_file, "Normal")
    display_visualizations(forecasted_mcdm_file, forecasted_aggregated_file, "Forecasted")
