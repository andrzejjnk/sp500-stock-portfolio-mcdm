import pandas as pd
import streamlit as st
from src.data_preprocessing.preprocess_data import preprocess_sp500_data


def get_min_max_dates(stocks_file):
    stocks = pd.read_csv(stocks_file)
    stocks['Date'] = pd.to_datetime(stocks['Date'])
    min_date = stocks['Date'].min().strftime('%Y-%m-%d')
    max_date = stocks['Date'].max().strftime('%Y-%m-%d')
    return min_date, max_date


def main_page():
    st.title("📊 Optimal Selection of SP500 Stock Portfolio using MCDM methods")
    st.write("""
    Welcome to the Optimal Selection of SP500 Stock Portfolio application!  
    Several MCDM methods are being used to help identify the best companies based on multi-criteria decision-making analyses.  
    Use the sidebar menu to navigate to the analysis results.
    """)
    default_start_date = '2024-01-01'
    default_end_date = '2024-12-20'

    default_min_date, default_max_date = get_min_max_dates('data/raw/sp500_stocks.csv')

    st.write("""
    **Date Range Selection**:  
    You can choose the start and end dates for the period you want to analyze the SP500 stock data.  
    The available date range is constrained by the data in the stock files. The default start and end dates are pre-set to the range from `2024-01-01` to `2024-12-20`, but you can adjust them as needed. 
    """)
    start_date = st.date_input(
        "Start Date", 
        value=pd.to_datetime(default_start_date), 
        min_value=pd.to_datetime(default_min_date),
        max_value=pd.to_datetime(default_max_date)
    )
    
    end_date = st.date_input(
        "End Date", 
        value=pd.to_datetime(default_end_date), 
        min_value=pd.to_datetime(default_min_date),
        max_value=pd.to_datetime(default_max_date)
    )

    st.write(f"Selected date range: {start_date} to {end_date}")

    if st.button('Run Preprocessing'):
        with st.spinner('Processing data...'):
            preprocess_sp500_data(
                start_date=str(start_date),
                end_date=str(end_date),
                stocks_file='data/raw/sp500_stocks.csv',
                companies_file='data/raw/sp500_companies.csv',
                output_stocks_file='data/preprocessed/sp500_stocks_clean.csv',
                output_indicators_file='data/preprocessed/sp500_stock_indicators.csv',
                output_decision_matrix_file='data/preprocessed/sp500_complete_decision_matrix.csv'
            )
            st.success("Data preprocessing complete!")

