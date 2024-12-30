import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

# Import VIKOR method
from src.mcdm.vikor import vikor

# Main function for the VIKOR page
def vikor_page():
    st.title("VIKOR Analysis for SP500 Stocks")

    # Collapsible section with a description of the VIKOR method
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
        5. Rank alternatives based on \( Q_i \) (smaller values are better).
        """)

    # Path to the decision matrix file
    decision_matrix_path = PROJECT_ROOT / "data/preprocessed/sp500_complete_decision_matrix.csv"
    results_path = PROJECT_ROOT / "results/sp500_vikor_results.csv"

    # Check if the file exists
    if not decision_matrix_path.exists():
        st.error(f"Decision matrix file not found at {decision_matrix_path}")
        return

    # Load the decision matrix
    data = pd.read_csv(decision_matrix_path)
    st.write("### Decision Matrix")
    st.dataframe(data.head())

    # Default weights and criteria types
    default_weights = [0.2, 0.15, 0.2, 0.1, 0.15, 0.1, 0.05, 0.05]
    default_criteria_types = ['benefit', 'benefit', 'benefit', 'benefit', 'cost', 'benefit', 'benefit', 'benefit']

    # Editable weights and criteria types in a collapsible expander
    with st.expander("Edit Criteria Weights and Types"):
        st.write("You can adjust the weights (importance) and types (benefit/cost) of each criterion below.")

        # Editable weights
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

        # Display normalized weights
        st.write("Normalized Weights (sum = 1):")
        st.write(weights)

        # Editable criteria types
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

    # Prepare the decision matrix (excluding Symbol and Shortname columns)
    decision_matrix = data.iloc[:, 2:].values

    # Run VIKOR
    rankings, Q, S, R = vikor(decision_matrix, weights, criteria_types)

    # Add results to the DataFrame
    data['VIKOR Score (Q)'] = Q
    data['Group Utility (S)'] = S
    data['Individual Regret (R)'] = R

    # Sort results
    sorted_data = data.sort_values(by='VIKOR Score (Q)', ascending=False)
    sorted_data['Rank'] = range(1, len(rankings) + 1)

    st.markdown("---")
    st.write("## 🏆 VIKOR Results")
    st.dataframe(sorted_data[['Symbol', 'Shortname', 'VIKOR Score (Q)', 'Group Utility (S)', 'Individual Regret (R)', 'Rank']])

    if st.button("Download VIKOR results"):
        results_path.parent.mkdir(parents=True, exist_ok=True)
        sorted_data.to_csv(results_path, index=False)
        st.success(f"Results saved to {results_path}")
