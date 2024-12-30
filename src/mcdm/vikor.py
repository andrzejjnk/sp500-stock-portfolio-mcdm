import numpy as np

def vikor(decision_matrix, weights, criteria_types):
    """
    Implements the VIKOR method for multi-criteria decision-making.

    Parameters:
    - decision_matrix (numpy array): Decision matrix (rows = alternatives, cols = criteria).
    - weights (numpy array): Weights for each criterion.
    - criteria_types (list of str): 'benefit' or 'cost' for each criterion.

    Returns:
    - rankings (numpy array): Indices of alternatives sorted by their scores (ascending).
    - Q (numpy array): Compromise solution scores for each alternative.
    - S (numpy array): Group utility scores for each alternative.
    - R (numpy array): Individual regret scores for each alternative.
    """
    # Step 1: Normalize the decision matrix
    norm_matrix = np.zeros_like(decision_matrix, dtype=float)

    for i, criterion in enumerate(criteria_types):
        column = decision_matrix[:, i]
        if criterion == "benefit":
            norm_matrix[:, i] = column / np.max(column)  # Benefit normalization
        elif criterion == "cost":
            epsilon = 1e-10  # Small value to avoid division by zero
            min_val = max(np.min(column), epsilon)
            norm_matrix[:, i] = np.where(column <= epsilon, 1, min_val / column)  # Avoid division by zero

    # Step 2: Compute the weighted normalized matrix
    weighted_matrix = norm_matrix * weights

    # Step 3: Calculate S (group utility) and R (individual regret)
    S = np.sum(weighted_matrix, axis=1)  # Sum of weighted normalized values
    R = np.max(weighted_matrix, axis=1)  # Maximum weighted normalized value

    # Step 4: Identify S_min, S_max, R_min, R_max
    S_min, S_max = np.min(S), np.max(S)
    R_min, R_max = np.min(R), np.max(R)

    # Step 5: Calculate the Q compromise solution for each alternative
    v = 0.5  # Weight of the strategy of majority rule (S)
    Q = v * (S - S_min) / (S_max - S_min) + (1 - v) * (R - R_min) / (R_max - R_min)

    # Step 6: Rank alternatives by Q (ascending order, higher is better)
    rankings = Q.argsort()

    return rankings, Q, S, R
