import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.mcdm.vikor import vikor

def vikor_page():
    st.title("VIKOR Analysis for SP500 Stocks")

    with st.expander("What is the VIKOR method?"):
        st.write("""
        VIKOR is a multi-criteria decision-making method that identifies a compromise solution based on closeness to the ideal solution.  
        It ranks alternatives by balancing the group utility (S) and individual regret (R).  

        **Steps in VIKOR**:
        1. Normalize the decision matrix to make criteria comparable:
           - Benefit criteria: Divide by the maximum value.
           - Cost criteria: Divide the minimum value by each value.
        2. Apply weights to the normalized matrix.
        3. Calculate:
           - \( S_i \): Sum of weighted normalized values for each alternative.
           - \( R_i \): Maximum weighted normalized value for each alternative.
        4. Calculate the \( Q_i \) compromise solution score for each alternative.
        5. Rank alternatives based on \( Q_i \) (higher values are better).
        """)

    decision_matrix_path = PROJECT_ROOT / "data/preprocessed/sp500_complete_decision_matrix.csv"
    results_path = PROJECT_ROOT / "results/sp500_vikor_results.csv"

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

        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
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

    rankings, Q, S, R = vikor(decision_matrix, weights, criteria_types)

    data['VIKOR Score (Q)'] = Q
    data['Group Utility (S)'] = S
    data['Individual Regret (R)'] = R

    # needs to be checked
    sorted_data = data.sort_values(by='VIKOR Score (Q)', ascending=False)
    sorted_data['Rank'] = range(1, len(rankings) + 1)

    # data['Rank'] = rankings + 1
    # sorted_data = data.sort_values(by='Rank', ascending=True)

    st.markdown("---")
    st.write("## 🏆 VIKOR Results")
    st.dataframe(sorted_data[['Symbol', 'Shortname', 'VIKOR Score (Q)', 'Group Utility (S)', 'Individual Regret (R)', 'Rank']])

    if st.button("Download VIKOR results"):
        results_path.parent.mkdir(parents=True, exist_ok=True)
        sorted_data.to_csv(results_path, index=False)
        st.success(f"Results saved to {results_path}")
