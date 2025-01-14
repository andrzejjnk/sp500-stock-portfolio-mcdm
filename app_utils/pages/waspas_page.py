import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.mcdm.waspas import waspas

def waspas_page():
    st.title("WASPAS Analysis for SP500 Stocks")

    with st.expander("What is the WASPAS method?"):
        st.write("""
        WASPAS (Weighted Aggregated Sum Product Assessment) is a multi-criteria decision-making method that combines
        the Weighted Sum Model (WSM) and Weighted Product Model (WPM) into a single aggregated method.

        **Steps in WASPAS**:
        1. Normalize the decision matrix:
           - Benefit criteria: Divide each value by the column maximum.
           - Cost criteria: Divide the column minimum by each value.
        2. Calculate:
           - \( Q_1 \): Weighted sum of the normalized decision matrix (WSM).
           - \( Q_2 \): Weighted product of the normalized decision matrix (WPM).
        3. Combine \( Q_1 \) and \( Q_2 \) using a weighting coefficient \( \lambda \) to compute the final score \( W \):
           - \( W = \lambda Q_1 + (1 - \lambda) Q_2 \)
        4. Rank alternatives based on \( W \) (higher values are better).
        """)

    # Paths to the decision matrix files
    decision_matrix_path = PROJECT_ROOT / "data/preprocessed/sp500_complete_decision_matrix.csv"
    forecasted_decision_matrix_path = PROJECT_ROOT / "data/forecasted_preprocessed/sp500_forecasted_complete_decision_matrix.csv"
    results_path = PROJECT_ROOT / "results/sp500_waspas_results.csv"
    forecasted_results_path = PROJECT_ROOT / "results/sp500_forecasted_waspas_results.csv"

    # Function to display WASPAS results
    def display_waspas_results(decision_matrix_path, results_path, title):
        if not decision_matrix_path.exists():
            st.error(f"Decision matrix file not found at {decision_matrix_path}")
            return

        data = pd.read_csv(decision_matrix_path)
        st.write(f"### {title} Decision Matrix")
        st.dataframe(data)

        # Default weights, criteria types, and lambda
        default_weights = [0.2, 0.15, 0.2, 0.1, 0.15, 0.1, 0.05, 0.05]
        default_criteria_types = ['benefit', 'benefit', 'benefit', 'benefit', 'cost', 'benefit', 'benefit', 'benefit']
        default_lambda = 0.5

        with st.expander(f"Edit Criteria Weights, Types, and Lambda for {title}"):
            st.write("You can adjust the weights (importance), types (benefit/cost), and the lambda parameter below.")

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

            lambda_param = st.slider("Set Lambda (Weighting Coefficient)", min_value=0.0, max_value=1.0, value=default_lambda, key=f"lambda_{title}")

        decision_matrix = data.iloc[:, 2:].values

        # Run WASPAS
        rankings, W, Q1, Q2 = waspas(decision_matrix, weights, criteria_types, lambda_param)

        data['WASPAS Score (W)'] = W
        data['WSM Score (Q1)'] = Q1
        data['WPM Score (Q2)'] = Q2

        sorted_data = data.sort_values(by='WASPAS Score (W)', ascending=False)
        sorted_data['Rank'] = range(1, len(rankings) + 1)

        st.markdown("---")
        st.write(f"## 🏆 {title} WASPAS Results")
        st.dataframe(sorted_data[['Symbol', 'Shortname', 'WASPAS Score (W)', 'WSM Score (Q1)', 'WPM Score (Q2)', 'Rank']])

        if st.button(f"Download {title} WASPAS results", key=f"download_{title}"):
            results_path.parent.mkdir(parents=True, exist_ok=True)
            sorted_data.to_csv(results_path, index=False)
            st.success(f"Results saved to {results_path}")

    # Display WASPAS results for normal data
    display_waspas_results(decision_matrix_path, results_path, "Normal")

    # Display WASPAS results for forecasted data
    display_waspas_results(forecasted_decision_matrix_path, forecasted_results_path, "Forecasted")
