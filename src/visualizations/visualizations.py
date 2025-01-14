import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from math import pi
from io import BytesIO

def plot_mcdm_heatmap(rankings_df, method_names, top_n=10, data_type="Normal"):
    """
    Creates an interactive heatmap comparing rankings across MCDM methods using Plotly.

    Parameters:
    - rankings_df (pd.DataFrame): DataFrame with MCDM rankings.
    - method_names (list): List of MCDM methods to include in the heatmap.
    - top_n (int): Number of top companies to display in the heatmap.
    - data_type (str): Type of data (e.g., "Normal" or "Forecasted").

    Returns:
    - Plotly figure object.
    """
    top_companies = rankings_df.sort_values(by="TOPSIS").head(top_n)

    fig = px.imshow(
        top_companies[method_names].set_index(top_companies["Symbol"]),
        text_auto=True,
        color_continuous_scale="viridis",
        labels={"color": "Rank"},
        title=f"Comparison of Rankings Across MCDM Methods (Top {top_n} Companies) - {data_type} Data"
    )
    fig.update_layout(
        xaxis_title="MCDM Methods",
        yaxis_title="Companies",
        coloraxis_colorbar=dict(title="Rank")
    )
    return fig

def plot_borda_copeland_scores(aggregated_df, top_n=10, data_type="Normal"):
    """
    Creates a grouped bar plot comparing Borda and Copeland scores for each alternative using Plotly.
    """
    aggregated_df = aggregated_df.head(top_n)
    df = aggregated_df[["Alternative", "Borda Count Score", "Copeland Score"]].melt(
        id_vars="Alternative", var_name="Score Type", value_name="Score"
    )
    fig = px.bar(
        df,
        x="Alternative",
        y="Score",
        color="Score Type",
        barmode="group",
        labels={"Alternative": "Companies", "Score": "Scores"},
        title=f"Borda and Copeland Scores by Company - {data_type} Data",
        color_discrete_map={"Borda Count Score": "blue", "Copeland Score": "green"}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_radar_chart(company_name, aggregated_df, data_type="Normal"):
    """
    Creates an interactive radar chart showing performance across criteria for a single company using Plotly.
    """
    criteria = ["Mean Rank Score", "Borda Count Score", "Copeland Score"]
    company_data = aggregated_df[aggregated_df["Company Name"] == company_name][criteria].values.flatten()

    min_values = aggregated_df[criteria].min().values
    max_values = aggregated_df[criteria].max().values
    normalized_values = (company_data - min_values) / (max_values - min_values)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized_values.tolist() + [normalized_values[0]],
        theta=criteria + [criteria[0]],
        fill="toself",
        name=company_name
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title=f"Performance of {company_name} Across Aggregated Methods - {data_type} Data"
    )
    return fig

def save_plot_to_bytes(fig):
    """
    Saves a Plotly figure to a BytesIO object in PNG format.
    """
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    return buf.getvalue()
