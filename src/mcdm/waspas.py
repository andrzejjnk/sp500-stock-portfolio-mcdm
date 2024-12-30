import numpy as np

def waspas(decision_matrix, weights, criteria_types, lambda_param=0.5):
    """
    Implements the WASPAS method for multi-criteria decision-making.

    Parameters:
    - decision_matrix (numpy array): Decision matrix (rows = alternatives, cols = criteria).
    - weights (numpy array): Weights for each criterion.
    - criteria_types (list of str): 'benefit' or 'cost' for each criterion.
    - lambda_param (float): Weighting coefficient for WASPAS, typically 0.5.

    Returns:
    - rankings (numpy array): Indices of alternatives sorted by their scores (descending).
    - W (numpy array): Combined WASPAS scores for each alternative.
    - Q1 (numpy array): Scores from the weighted sum model.
    - Q2 (numpy array): Scores from the weighted product model.
    """
    # Step 1: Normalize the decision matrix
    norm_matrix = decision_matrix / np.max(decision_matrix, axis=0)  # Benefit normalization
    for i, criterion in enumerate(criteria_types):
        if criterion == "cost":
            norm_matrix[:, i] = np.min(decision_matrix[:, i]) / decision_matrix[:, i]  # Cost normalization

    # Step 2: Calculate the Weighted Sum Model (WSM) scores (Q1)
    Q1 = np.sum(norm_matrix * weights, axis=1)

    # Step 3: Calculate the Weighted Product Model (WPM) scores (Q2)
    Q2 = np.prod(np.power(norm_matrix, weights), axis=1)

    # Step 4: Calculate the combined WASPAS score (W)
    W = lambda_param * Q1 + (1 - lambda_param) * Q2

    # Step 5: Rank alternatives (higher W is better)
    rankings = W.argsort()[::-1]

    return rankings, W, Q1, Q2
