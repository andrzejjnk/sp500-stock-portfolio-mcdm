import pandas as pd
import numpy as np

def process_csv_files(file_paths):
    """
    Reads multiple CSV files containing rankings and creates a ranking matrix.

    Parameters:
    - file_paths (list of str): List of file paths to the CSV files.

    Returns:
    - ranking_matrix (numpy array): Matrix where rows are alternatives (stocks)
      and columns are rankings from different methods.
    - alternatives (list): List of stock symbols (alternatives).
    - shortnames (list): List of company shortnames (names corresponding to symbols).
    """
    rankings = []
    alternatives = None
    shortnames = None

    for file_path in file_paths:
        df = pd.read_csv(file_path)

        df = df.sort_values('Symbol')

        if alternatives is None:
            alternatives = df['Symbol'].tolist()
            shortnames = df['Shortname'].tolist()
        elif alternatives != df['Symbol'].tolist():
            raise ValueError("Mismatch in alternatives between files. Ensure all files have the same rows.")

        rankings.append(df['Rank'].values)

    # Combine rankings into a matrix (rows = alternatives, cols = methods)
    ranking_matrix = np.array(rankings).T
    return ranking_matrix, alternatives, shortnames

def create_mcdm_rankings_file(file_paths, output_file, method_names):
    """
    Creates a combined rankings CSV file from multiple MCDM results.

    Parameters:
    - file_paths (list of str): List of file paths to the CSV files.
    - output_file (str): Path to save the combined rankings file.
    - method_names (list of str): Names of the MCDM methods corresponding to the file paths.
    """
    ranking_matrix, alternatives, shortnames = process_csv_files(file_paths)

    rankings_df = pd.DataFrame(ranking_matrix, columns=method_names)
    rankings_df.insert(0, "Shortname", shortnames)
    rankings_df.insert(0, "Symbol", alternatives)

    rankings_df.to_csv(output_file, index=False)
    print(f"Combined rankings saved to {output_file}")

file_paths = [
    "results/sp500_topsis_results.csv",
    "results/sp500_aras_results.csv",
    "results/sp500_vikor_results.csv",
    "results/sp500_copras_results.csv",
    "results/sp500_waspas_results.csv",
    "results/sp500_taxonomy_results.csv"
]

forecasted_file_paths = [
    "results/sp500_forecasted_topsis_results.csv",
    "results/sp500_forecasted_aras_results.csv",
    "results/sp500_forecasted_vikor_results.csv",
    "results/sp500_forecasted_copras_results.csv",
    "results/sp500_forecasted_waspas_results.csv",
    "results/sp500_forecasted_taxonomy_results.csv"
]

method_names = ["TOPSIS", "ARAS", "VIKOR", "COPRAS", "WASPAS", "TAXONOMY"]
output_file = "results/normal_mcdm_rankings.csv"
forecasted_output_file = "results/forecasted_mcdm_rankings.csv"

def create_mcdm_ranking_wrapper():
    create_mcdm_rankings_file(file_paths, output_file, method_names)
    create_mcdm_rankings_file(forecasted_file_paths, forecasted_output_file, method_names)
