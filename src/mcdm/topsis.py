import numpy as np
import pandas as pd

def topsis(decision_matrix, weights, criteria_types):
    """
    Implements the TOPSIS method for multi-criteria decision-making.
    
    Parameters:
    - decision_matrix (numpy array): The decision matrix (rows = alternatives, cols = criteria).
    - weights (numpy array): Weights for each criterion.
    - criteria_types (list of str): 'benefit' or 'cost' for each criterion.
    
    Returns:
    - rankings (numpy array): Indices of alternatives sorted by their scores (descending).
    - scores (numpy array): Closeness scores for each alternative.
    """
    # Step 1: Normalize the decision matrix
    norm_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))
    
    # Step 2: Apply weights to the normalized matrix
    weighted_matrix = norm_matrix * weights
    
    # Step 3: Determine the ideal (best) and anti-ideal (worst) solutions
    ideal_best = np.array([
        weighted_matrix[:, i].max() if criteria_types[i] == 'benefit' else weighted_matrix[:, i].min()
        for i in range(weighted_matrix.shape[1])
    ])
    ideal_worst = np.array([
        weighted_matrix[:, i].min() if criteria_types[i] == 'benefit' else weighted_matrix[:, i].max()
        for i in range(weighted_matrix.shape[1])
    ])
    
    # Step 4: Calculate distances to the ideal and anti-ideal solutions
    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    
    # Step 5: Calculate the relative closeness to the ideal solution
    scores = dist_worst / (dist_best + dist_worst)
    
    # Step 6: Rank alternatives based on scores (higher is better)
    rankings = scores.argsort()[::-1]
    
    return rankings, scores
