import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def aras(decision_matrix, weights, criteria_types):
    """
    Implements the ARAS (Additive Ratio Assessment) method for multi-criteria decision-making.
    
    Parameters:
    - decision_matrix (numpy array): The decision matrix (rows = alternatives, cols = criteria).
    - weights (numpy array): Weights for each criterion.
    - criteria_types (list of str): 'benefit' or 'cost' for each criterion.
    
    Returns:
    - rankings (numpy array): Indices of alternatives sorted by their scores (descending).
    - scores (numpy array): Utility scores for each alternative.
    """
    # Step 1: Standardize the decision matrix (using StandardScaler)
    scaler = StandardScaler()
    norm_matrix = scaler.fit_transform(decision_matrix)
    
    # Step 2: Apply weights to the standardized matrix
    weighted_matrix = norm_matrix * weights
    
    # Step 3: Determine the ideal (best) solutions for each criterion
    ideal_best = np.array([
        weighted_matrix[:, i].max() if criteria_types[i] == 'benefit' else weighted_matrix[:, i].min()
        for i in range(weighted_matrix.shape[1])
    ])
    
    # Step 4: Ensure no zero division errors (avoid divide by zero)
    ideal_best = np.where(ideal_best == 0, 1e-10, ideal_best)
    
    # Step 5: Calculate the utility degree for each alternative
    utility_scores = np.sum(weighted_matrix / ideal_best, axis=1)  # sum of ratios
    
    # Step 6: Rank alternatives based on their utility scores (higher is better)
    rankings = utility_scores.argsort()[::-1]  # Sort in descending order
    
    return rankings, utility_scores