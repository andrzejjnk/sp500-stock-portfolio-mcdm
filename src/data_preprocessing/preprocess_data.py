import pandas as pd

def preprocess_sp500_data(start_date: str, end_date: str, stocks_file: str, companies_file: str, 
                          output_stocks_file: str, output_indicators_file: str, output_decision_matrix_file: str):
    """
    Preprocesses the SP500 stock data, calculates financial indicators, and generates a decision matrix.

    This function performs the following steps:
    1. Loads and cleans SP500 stock data by removing rows with NaN values.
    2. Filters stock data based on the provided date range.
    3. Computes financial indicators for each stock symbol (Volatility, Average Close Price, Return, Average Volume).
    4. Normalizes the calculated indicators.
    5. Loads additional company data and merges it with the calculated stock indicators.
    6. Normalizes the columns of the decision matrix (including fundamental data).
    7. Saves the cleaned stock data, stock indicators, and the complete decision matrix to CSV files.

    Parameters:
    start_date (str): The start date of the period to filter the data (format: 'YYYY-MM-DD').
    end_date (str): The end date of the period to filter the data (format: 'YYYY-MM-DD').
    stocks_file (str): Path to the raw SP500 stock data CSV file.
    companies_file (str): Path to the SP500 companies data CSV file.
    output_stocks_file (str): Path to save the cleaned stock data CSV file.
    output_indicators_file (str): Path to save the stock indicators CSV file.
    output_decision_matrix_file (str): Path to save the complete decision matrix CSV file.
    """
    
    # Step 1: Load and clean SP500 stock data
    stocks = pd.read_csv(stocks_file)
    stocks = stocks.dropna()  # Remove rows with NaN values
    stocks.to_csv(output_stocks_file, index=False)  # Save cleaned stock data

    # Step 2: Filter stock data based on the date range
    stocks['Date'] = pd.to_datetime(stocks['Date'])  # Convert 'Date' column to datetime format
    filtered_stocks = stocks[(stocks['Date'] >= start_date) & (stocks['Date'] <= end_date)]  # Filter by date range

    # Step 3: Calculate financial indicators for each stock symbol
    stock_indicators = filtered_stocks.groupby('Symbol').agg({
        'High': lambda x: (x - filtered_stocks['Low']).mean(),  # Daily volatility (mean difference between High and Low)
        'Adj Close': 'mean',  # Average adjusted close price
        'Close': lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0],  # Percentage return (last close / first close)
        'Volume': 'mean'  # Average trading volume
    }).rename(columns={
        'High': 'Volatility',
        'Adj Close': 'Average Close Price',
        'Close': 'Return',
        'Volume': 'Average Volume'
    })

    # Step 4: Normalize the calculated financial indicators
    def normalize_column(column):
        """Normalize a column using min-max normalization."""
        return (column - column.min()) / (column.max() - column.min())
    
    columns_to_normalize = ['Volatility', 'Average Close Price', 'Return', 'Average Volume']
    for col in columns_to_normalize:
        stock_indicators[col] = normalize_column(stock_indicators[col])  # Normalize selected columns

    # Step 5: Save the stock indicators to a CSV file
    stock_indicators.to_csv(output_indicators_file)  # Save stock indicators

    # Step 6: Load company data and merge with stock indicators
    companies = pd.read_csv(companies_file)
    decision_matrix = pd.merge(companies, stock_indicators, on='Symbol')  # Merge companies with stock indicators

    # Step 7: Select relevant columns for the decision matrix
    decision_matrix = decision_matrix[['Symbol', 'Shortname', 'Revenuegrowth', 'Ebitda', 'Marketcap', 'Weight',
                                       'Volatility', 'Average Close Price', 'Return', 'Average Volume']]

    # Step 8: Normalize the columns of the decision matrix
    columns_to_normalize = ['Revenuegrowth', 'Ebitda', 'Marketcap', 'Weight', 
                            'Volatility', 'Average Close Price', 'Return', 'Average Volume']
    for col in columns_to_normalize:
        decision_matrix[col] = normalize_column(decision_matrix[col])  # Normalize the decision matrix columns

    # Step 9: Save the complete decision matrix to a CSV file
    decision_matrix = decision_matrix.dropna()
    decision_matrix.to_csv(output_decision_matrix_file, index=False)  # Save the complete decision matrix

    print(decision_matrix.head())
    print(decision_matrix.columns)

preprocess_sp500_data(
    start_date='2024-01-01', 
    end_date='2024-12-20', 
    stocks_file='data/raw/sp500_stocks.csv', 
    companies_file='data/raw/sp500_companies.csv', 
    output_stocks_file='data/preprocessed/sp500_stocks_clean.csv', 
    output_indicators_file='data/preprocessed/sp500_stock_indicators.csv', 
    output_decision_matrix_file='data/preprocessed/sp500_complete_decision_matrix.csv'
)
