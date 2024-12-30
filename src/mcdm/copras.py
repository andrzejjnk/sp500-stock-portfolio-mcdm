import numpy as np

def copras(decision_matrix, weights, criteria_types):
    """
    Implements the COPRAS method for multi-criteria decision-making.
    
    Parameters:
    - decision_matrix (numpy array): Decision matrix (rows = alternatives, cols = criteria).
    - weights (numpy array): Weights for each criterion.
    - criteria_types (list of str): 'benefit' or 'cost' for each criterion.
    
    Returns:
    - rankings (numpy array): Indices of alternatives sorted by their scores (descending).
    - utility_scores (numpy array): Utility degree scores for each alternative.
    """
    # Step 1: Normalize the decision matrix
    norm_matrix = decision_matrix / np.sum(decision_matrix, axis=0)

    # Step 2: Apply weights to the normalized matrix
    weighted_matrix = norm_matrix * weights

    # Step 3: Separate benefit and cost criteria
    benefit_scores = np.sum(weighted_matrix[:, [i for i, c in enumerate(criteria_types) if c == "benefit"]], axis=1)
    cost_scores = np.sum(weighted_matrix[:, [i for i, c in enumerate(criteria_types) if c == "cost"]], axis=1)

    # Step 4: Calculate the relative significance (Ri)
    relative_significance = benefit_scores - cost_scores

    # Step 5: Calculate the utility degree (Qi) for each alternative
    Q = relative_significance / np.max(relative_significance) * 100  # Normalize to percentage scale

    # Step 6: Rank alternatives (higher Q is better)
    rankings = Q.argsort()[::-1]

    return rankings, Q
