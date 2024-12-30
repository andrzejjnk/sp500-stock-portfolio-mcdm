import numpy as np

def calculate_ranks(values, reverse=False):
    """
    Calculate ranks for a given array of values. Handles ties by assigning the same rank to equal values.

    Parameters:
    - values (numpy array): Array of values to rank.
    - reverse (bool): Whether higher values should have lower ranks (for scores like Borda or Copeland).

    Returns:
    - ranks (numpy array): Array of ranks (starting from 1).
    """
    sorted_indices = np.argsort(values)
    if reverse:
        sorted_indices = sorted_indices[::-1]

    ranks = np.empty_like(sorted_indices)
    ranks[sorted_indices] = range(1, len(values) + 1)
    return ranks



def mean_rank_method(rankings):
    """
    Implements the Mean Rank Method for aggregating rankings.

    Parameters:
    - rankings (numpy array): Matrix of rankings, where rows represent alternatives 
      and columns represent rankings from different MCDM methods.

    Returns:
    - aggregated_ranking (numpy array): Final aggregated ranking based on mean ranks.
    - mean_ranks (numpy array): Mean ranks for each alternative.
    """
    mean_ranks = np.mean(rankings, axis=1)
    aggregated_ranking = calculate_ranks(mean_ranks)  # Lower mean rank is better
    return aggregated_ranking, mean_ranks


def borda_count_method(rankings):
    """
    Implements the Borda Count Method for aggregating rankings.

    Parameters:
    - rankings (numpy array): Matrix of rankings, where rows represent alternatives 
      and columns represent rankings from different MCDM methods.

    Returns:
    - aggregated_ranking (numpy array): Final aggregated ranking based on Borda scores.
    - borda_scores (numpy array): Borda scores for each alternative.
    """
    n_alternatives, n_methods = rankings.shape
    borda_scores = np.zeros(n_alternatives)

    for i in range(n_alternatives):
        for j in range(n_alternatives):
            if i != j:
                # Count the number of methods where alternative i is ranked better than j
                borda_scores[i] += np.sum(rankings[i, :] < rankings[j, :])

    aggregated_ranking = calculate_ranks(borda_scores, reverse=True)  # Higher Borda score is better
    return aggregated_ranking, borda_scores


def copeland_method(rankings):
    """
    Implements the Copeland Method for aggregating rankings.

    Parameters:
    - rankings (numpy array): Matrix of rankings, where rows represent alternatives 
      and columns represent rankings from different MCDM methods.

    Returns:
    - aggregated_ranking (numpy array): Final aggregated ranking based on Copeland scores.
    - copeland_scores (numpy array): Copeland scores for each alternative.
    """
    n_alternatives, n_methods = rankings.shape
    copeland_scores = np.zeros(n_alternatives)

    for i in range(n_alternatives):
        wins = 0
        losses = 0
        for j in range(n_alternatives):
            if i != j:
                wins += np.sum(rankings[i, :] < rankings[j, :])
                losses += np.sum(rankings[i, :] > rankings[j, :])
        copeland_scores[i] = wins - losses

    aggregated_ranking = calculate_ranks(copeland_scores, reverse=True)  # Higher Copeland score is better
    return aggregated_ranking, copeland_scores
