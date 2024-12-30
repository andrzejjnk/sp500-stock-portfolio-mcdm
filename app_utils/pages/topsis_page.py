import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.mcdm.topsis import topsis

def topsis_page():
    st.title("TOPSIS Analysis for SP500 Stocks")

    with st.expander("What is the TOPSIS method?"):
        st.write("""
        The Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision-making method.  
        It identifies the best alternative by measuring the relative closeness to an ideal solution.  

        **Steps in TOPSIS**:
        1. Normalize the decision matrix to make criteria comparable.
        2. Weight the normalized matrix based on the importance of each criterion.
        3. Identify the ideal (best) and anti-ideal (worst) solutions:
           - Ideal: Maximum for benefit criteria, minimum for cost criteria.
           - Anti-ideal: Minimum for benefit criteria, maximum for cost criteria.
        4. Calculate the distances of each alternative from the ideal and anti-ideal solutions.
        5. Compute the relative closeness to the ideal solution and rank alternatives accordingly.  

        **Interpretation**:  
        - A higher TOPSIS score indicates a better alternative closer to the ideal solution.  
        """)

    # Path to the decision matrix file
    decision_matrix_path = PROJECT_ROOT / "data/preprocessed/sp500_complete_decision_matrix.csv"
    results_path = PROJECT_ROOT / "results/sp500_topsis_results.csv"

    if not decision_matrix_path.exists():
        st.error(f"Decision matrix file not found at {decision_matrix_path}")
        return
    
    data = pd.read_csv(decision_matrix_path)
    st.write("### Decision Matrix")
    st.dataframe(data)

    # Default weights and criteria types
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

    # Run TOPSIS
    rankings, scores = topsis(decision_matrix, weights, criteria_types)

    data['TOPSIS Score'] = scores
    data['Rank'] = rankings + 1  # 1-based indexing

    sorted_data = data.sort_values(by='Rank')

    st.markdown("---")
    st.write("## 🏆 TOPSIS Results")
    st.dataframe(sorted_data[['Symbol', 'Shortname', 'TOPSIS Score', 'Rank']])

    if st.button("Download TOPSIS results"):
        results_path.parent.mkdir(parents=True, exist_ok=True)
        sorted_data.to_csv(results_path, index=False)
        st.success(f"Results saved to {results_path}")
