import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.mcdm.taxonomy import taxonomy

def taxonomy_page():
    st.title("TAXONOMY Analysis for SP500 Stocks")

    with st.expander("What is the TAXONOMY method?"):
        st.write("""
        TAXONOMY is a multi-criteria decision-making method that evaluates alternatives based on their distances
        from an ideal point in a multi-dimensional criteria space.

        **Steps in TAXONOMY**:
        1. Normalize the decision matrix:
           - Benefit criteria: Divide each value by the column maximum.
           - Cost criteria: Divide the column minimum by each value.
        2. Apply weights to the normalized decision matrix.
        3. Compute the ideal point (Z*) as the maximum value for each criterion.
        4. Calculate the Euclidean distance of each alternative from the ideal point.
        5. Rank alternatives based on their distances (lower distances are better).
        """)

    # Paths to the decision matrix files
    decision_matrix_path = PROJECT_ROOT / "data/preprocessed/sp500_complete_decision_matrix.csv"
    forecasted_decision_matrix_path = PROJECT_ROOT / "data/forecasted_preprocessed/sp500_forecasted_complete_decision_matrix.csv"
    results_path = PROJECT_ROOT / "results/sp500_taxonomy_results.csv"
    forecasted_results_path = PROJECT_ROOT / "results/sp500_forecasted_taxonomy_results.csv"

    # Function to display TAXONOMY results
    def display_taxonomy_results(decision_matrix_path, results_path, title):
        if not decision_matrix_path.exists():
            st.error(f"Decision matrix file not found at {decision_matrix_path}")
            return

        data = pd.read_csv(decision_matrix_path)
        st.write(f"### {title} Decision Matrix")
        st.dataframe(data)

        # Default weights and criteria types
        default_weights = [0.2, 0.15, 0.2, 0.1, 0.15, 0.1, 0.05, 0.05]
        default_criteria_types = ['benefit', 'benefit', 'benefit', 'benefit', 'cost', 'benefit', 'benefit', 'benefit']

        with st.expander(f"Edit Criteria Weights and Types for {title}"):
            st.write("You can adjust the weights (importance) and types (benefit/cost) of each criterion below.")

            weights = []
            st.write("#### Set Criteria Weights")
            for i, weight in enumerate(default_weights):
                weights.append(st.number_input(f"Criterion {i + 1} Weight", min_value=0.0, max_value=1.0, value=weight, key=f"weight_{i}_{title}"))

            total_weight = sum(weights)
            if total_weight > 0:
                weights = [w / total_weight for w in weights]  # Normalize weights
            else:
                st.error("Total weight cannot be zero. Please adjust the weights.")

            st.write("Normalized Weights (sum = 1):")
            st.write(weights)

            st.write("#### Set Criteria Types")
            criteria_types = []
            for i, criterion in enumerate(default_criteria_types):
                criteria_types.append(
                    st.selectbox(
                        f"Criterion {i + 1} Type",
                        options=["benefit", "cost"],
                        index=0 if criterion == "benefit" else 1,
                        key=f"criterion_{i}_{title}"
                    )
                )

        decision_matrix = data.iloc[:, 2:].values

        # Run TAXONOMY
        rankings, distances, norm_matrix, ideal_point = taxonomy(decision_matrix, weights, criteria_types)

        data['Distance'] = distances
        data['Rank'] = rankings + 1

        sorted_data = data.sort_values(by='Distance', ascending=True)
        sorted_data['Rank'] = range(1, len(rankings) + 1)

        st.markdown("---")
        st.write(f"## 🏆 {title} TAXONOMY Results")
        st.dataframe(sorted_data[['Symbol', 'Shortname', 'Distance', 'Rank']])

        if st.button(f"Download {title} TAXONOMY results", key=f"download_{title}"):
            results_path.parent.mkdir(parents=True, exist_ok=True)
            sorted_data.to_csv(results_path, index=False)
            st.success(f"Results saved to {results_path}")

    # Display TAXONOMY results for normal data
    display_taxonomy_results(decision_matrix_path, results_path, "Normal")

    # Display TAXONOMY results for forecasted data
    display_taxonomy_results(forecasted_decision_matrix_path, forecasted_results_path, "Forecasted")
