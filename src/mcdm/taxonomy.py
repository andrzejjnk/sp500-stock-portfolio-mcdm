import numpy as np

def taxonomy(decision_matrix, weights, criteria_types):
    """
    Implements the TAXONOMY method for multi-criteria decision-making.
    
    Parameters:
    - decision_matrix (numpy array): Decision matrix (rows = alternatives, cols = criteria).
    - weights (numpy array): Weights for each criterion.
    - criteria_types (list of str): 'benefit' or 'cost' for each criterion.
    
    Returns:
    - rankings (numpy array): Indices of alternatives sorted by their distances (ascending).
    - distances (numpy array): Distance scores for each alternative (lower is better).
    - normalized_matrix (numpy array): Normalized decision matrix.
    - ideal_point (numpy array): Ideal point in the criteria space.
    """
    # Step 1: Normalize the decision matrix
    norm_matrix = decision_matrix / (np.max(decision_matrix, axis=0) + 1e-10)  # Prevent division by zero in benefit criteria
    for i, criterion in enumerate(criteria_types):
        if criterion == "cost":
            min_value = np.min(decision_matrix[:, i])
            max_value = np.max(decision_matrix[:, i])
            # Prevent division by zero
            if max_value - min_value > 0:  # Range > 0
                norm_matrix[:, i] = min_value / (decision_matrix[:, i] + 1e-10)
            else:
                norm_matrix[:, i] = 1  # If range is zero (all values are the same), set norm to 1

    # Step 2: Calculate the weighted normalized matrix
    weighted_matrix = norm_matrix * weights

    # Step 3: Compute the ideal point (Z*) for all criteria
    ideal_point = np.max(weighted_matrix, axis=0)  # Ideal point (maximum values)

    # Step 4: Calculate the Euclidean distance from the ideal point for each alternative
    distances = np.sqrt(np.sum((weighted_matrix - ideal_point) ** 2, axis=1))

    # Step 5: Rank alternatives (lower distance is better)
    rankings = distances.argsort()

    return rankings, distances, norm_matrix, ideal_point
