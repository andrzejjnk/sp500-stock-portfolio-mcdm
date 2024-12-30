import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.mcdm.copras import copras

def copras_page():
    st.title("COPRAS Analysis for SP500 Stocks")

    with st.expander("What is the COPRAS method?"):
        st.write("""
        COPRAS (Complex Proportional Assessment) is a multi-criteria decision-making method that evaluates alternatives based on their relative significance.  

        **Steps in COPRAS**:
        1. Normalize the decision matrix by dividing each value by the column sum.
        2. Apply weights to the normalized matrix.
        3. Separate benefit and cost criteria:
           - Benefit: Criteria where higher values are better.
           - Cost: Criteria where lower values are better.
        4. Calculate the relative significance (\( R_i \)) for each alternative.
        5. Calculate the utility degree (\( Q_i \)) for each alternative as a percentage of the maximum \( R_i \).
        6. Rank alternatives based on \( Q_i \) (higher values are better).
        """)

    decision_matrix_path = PROJECT_ROOT / "data/preprocessed/sp500_complete_decision_matrix.csv"
    results_path = PROJECT_ROOT / "results/sp500_copras_results.csv"

    if not decision_matrix_path.exists():
        st.error(f"Decision matrix file not found at {decision_matrix_path}")
        return

    data = pd.read_csv(decision_matrix_path)
    st.write("### Decision Matrix")
    st.dataframe(data)

    default_weights = [0.2, 0.15, 0.2, 0.1, 0.15, 0.1, 0.05, 0.05]
    default_criteria_types = ['benefit', 'benefit', 'benefit', 'benefit', 'cost', 'benefit', 'benefit', 'benefit']

    with st.expander("Edit Criteria Weights and Types"):
        st.write("You can adjust the weights (importance) and types (benefit/cost) of each criterion below.")

        weights = []
        st.write("#### Set Criteria Weights")
        for i, weight in enumerate(default_weights):
            weights.append(st.number_input(f"Criterion {i + 1} Weight", min_value=0.0, max_value=1.0, value=weight))

        # Automatically normalize weights to sum to 1
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
                )
            )

    decision_matrix = data.iloc[:, 2:].values

    # Run COPRAS
    rankings, utility_scores = copras(decision_matrix, weights, criteria_types)

    data['Utility Score (Q)'] = utility_scores

    sorted_data = data.sort_values(by='Utility Score (Q)', ascending=False)
    sorted_data['Rank'] = range(1, len(rankings) + 1)

    st.markdown("---")
    st.write("## 🏆 COPRAS Results")
    st.dataframe(sorted_data[['Symbol', 'Shortname', 'Utility Score (Q)', 'Rank']])

    if st.button("Download COPRAS results"):
        results_path.parent.mkdir(parents=True, exist_ok=True)
        sorted_data.to_csv(results_path, index=False)
        st.success(f"Results saved to {results_path}")

