import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import sys
from src.aggregation.aggregation_methods import mean_rank_method, borda_count_method, copeland_method
from src.aggregation.process_results import create_mcdm_ranking_wrapper

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

def display_aggregation_results(rankings_file, title):
    try:
        rankings_df = pd.read_csv(rankings_file)
        st.write(f"### {title} Rankings from MCDM Methods")
        st.write(f"Below is a summary of {title} rankings from individual MCDM methods.")
        st.dataframe(rankings_df)
    except FileNotFoundError:
        st.error(f"{title} rankings file not found. Please ensure the file exists.")
        return

    rankings = rankings_df.iloc[:, 2:].values
    shortnames = rankings_df.iloc[:, 1].values
    alternatives = rankings_df.iloc[:, 0].values

    mean_rank_agg, mean_ranks = mean_rank_method(rankings)
    st.write(f"### {title} Mean Rank Method")
    with st.expander(f"Learn more about the {title} Mean Rank Method"):
        st.write("""
        The Mean Rank Method is a simple and effective way to aggregate rankings from multiple decision-making methods.
        It calculates the average rank across all MCDM methods for each alternative (e.g., stock or company).

        **Steps**:
        1. Collect the ranks of each alternative from all MCDM methods.
        2. Compute the mean rank for each alternative.
        3. Sort the alternatives by their mean rank (lower mean rank indicates a better alternative).
        """)
    mean_rank_df = pd.DataFrame({
        "Alternative": alternatives,
        "Company Name": shortnames,
        "Mean Rank": mean_ranks,
        "Final Rank (Mean Rank)": mean_rank_agg
    }).sort_values("Final Rank (Mean Rank)")
    st.dataframe(mean_rank_df)

    borda_agg, borda_scores = borda_count_method(rankings)
    st.write(f"### {title} Borda Count Method")
    with st.expander(f"Learn more about the {title} Borda Count Method"):
        st.write("""
        The Borda Count Method is a voting-based aggregation technique that ranks alternatives based on their performance across multiple criteria.
        It assigns scores to each alternative by counting how many times it ranks higher than other alternatives in each MCDM method.

        **Steps**:
        1. For each pair of alternatives, count the number of MCDM methods in which one alternative ranks higher than the other.
        2. Sum these counts across all pairwise comparisons to calculate the Borda Score for each alternative.
        3. Rank the alternatives based on their Borda Scores (higher score indicates a better alternative).
        """)
    borda_df = pd.DataFrame({
        "Alternative": alternatives,
        "Company Name": shortnames,
        "Borda Score": borda_scores,
        "Final Rank (Borda)": borda_agg
    }).sort_values("Final Rank (Borda)")
    st.dataframe(borda_df)

    copeland_agg, copeland_scores = copeland_method(rankings)
    st.write(f"### {title} Copeland Method")
    with st.expander(f"Learn more about the {title} Copeland Method"):
        st.write("""
        The Copeland Method builds on the concept of pairwise comparisons and calculates the difference between wins and losses for each alternative.
        An alternative "wins" when it ranks higher than another alternative in a specific MCDM method.

        **Steps**:
        1. For each alternative, count the number of "wins" (times it ranks higher than another alternative) across all MCDM methods.
        2. Similarly, count the number of "losses" (times it ranks lower than another alternative).
        3. Compute the Copeland Score as the difference between wins and losses.
        4. Rank the alternatives based on their Copeland Scores (higher score indicates a better alternative).
        """)
    copeland_df = pd.DataFrame({
        "Alternative": alternatives,
        "Company Name": shortnames,
        "Copeland Score": copeland_scores,
        "Final Rank (Copeland)": copeland_agg
    }).sort_values("Final Rank (Copeland)")
    st.dataframe(copeland_df)

    st.write(f"### {title} Combined Aggregated Rankings")
    st.write(f"Below is a combined table showing {title} rankings from all aggregation methods.")
    combined_df = pd.merge(mean_rank_df, borda_df, on=["Alternative","Company Name"], how="inner")
    combined_df = pd.merge(combined_df, copeland_df, on=["Alternative","Company Name"], how="inner")
    combined_df = combined_df.rename(columns={
        "Mean Rank": "Mean Rank Score",
        "Final Rank (Mean Rank)": "Rank (Mean Rank)",
        "Borda Score": "Borda Count Score",
        "Final Rank (Borda)": "Rank (Borda)",
        "Copeland Score": "Copeland Score",
        "Final Rank (Copeland)": "Rank (Copeland)"
    })
    combined_df = combined_df.sort_values("Rank (Mean Rank)")  # Sort by the first method's rank
    st.dataframe(combined_df)

    results_path = PROJECT_ROOT / f"results/{title.lower()}_aggregated_rankings.csv"
    if st.button(f"Download {title} aggregated results"):
        results_path.parent.mkdir(parents=True, exist_ok=True)
        combined_df.to_csv(results_path, index=False)
        st.success(f"Results saved to {results_path}")

def aggregation_page():
    st.title("Aggregation Methods for SP500 Rankings")

    create_mcdm_ranking_wrapper()

    rankings_file = "results/normal_mcdm_rankings.csv"
    forecasted_rankings_file = "results/forecasted_mcdm_rankings.csv"

    display_aggregation_results(rankings_file, "Normal")
    display_aggregation_results(forecasted_rankings_file, "Forecasted")
