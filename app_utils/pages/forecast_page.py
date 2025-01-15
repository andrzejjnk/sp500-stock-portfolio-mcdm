import streamlit as st
import os
import pandas as pd
import sys
from pathlib import Path

# Adding the project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # structure: project_root -> src/
sys.path.append(str(PROJECT_ROOT))

from src.forecasting.forecast import forecast_all_columns, transform_forecast_data
from src.data_preprocessing.preprocess_data import preprocess_sp500_data

def get_min_max_dates(stocks_file):
    stocks = pd.read_csv(stocks_file)
    stocks['Date'] = pd.to_datetime(stocks['Date'])
    min_date = stocks['Date'].min().strftime('%Y-%m-%d')
    max_date = stocks['Date'].max().strftime('%Y-%m-%d')
    return min_date, max_date

def ensure_directory_exists(directory):
    """Ensure that the directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        st.success(f"Created directory: {directory}")
    else:
        st.success(f"Directory already exists: {directory}")

def forecast_page():
    st.title("📈 Forecasting Stock Data with ARIMA")

    default_min_date, default_max_date = get_min_max_dates('data/raw/sp500_stocks.csv')
    st.write(f"""
    ARIMA model predicts from data in the range from {default_min_date} to {default_max_date}.
    """)

    # Load raw stock data
    stocks_file = 'data/raw/sp500_stocks.csv'
    try:
        stocks_data = pd.read_csv(stocks_file)
    except FileNotFoundError:
        st.error("Stock data file not found. Please ensure the file exists.")
        return

    # Forecasting parameters
    st.write("### Select Forecasting Parameters")
    forecast_period = st.slider("Select number of days to forecast:", min_value=1, max_value=365, value=90)

    # Generate forecast
    if st.button("Generate Forecast"):
        with st.spinner("Forecasting all columns..."):
            forecast_output_file = 'data/forecasted/forecasted_stock.csv'
            forecast_all_columns(stocks_data, forecast_period, forecast_output_file)
            transform_forecast_data(forecast_output_file, forecast_output_file)
            st.success(f"Forecast complete! Results saved to {forecast_output_file}")

            # Extract start and end dates from the forecasted data
            forecasted_data = pd.read_csv(forecast_output_file)
            forecasted_data['Date'] = pd.to_datetime(forecasted_data['Date'])
            start_date = forecasted_data['Date'].min().strftime('%Y-%m-%d')
            end_date = forecasted_data['Date'].max().strftime('%Y-%m-%d')

            # Ensure the forecasted_preprocessed directory exists
            forecasted_preprocessed_dir = 'data/forecasted_preprocessed'
            ensure_directory_exists(forecasted_preprocessed_dir)

            # Preprocess the data with the extracted dates
            preprocess_sp500_data(
                start_date=start_date,
                end_date=end_date,
                stocks_file='data/forecasted/forecasted_stock.csv',
                companies_file='data/raw/sp500_companies.csv',
                output_stocks_file=f'{forecasted_preprocessed_dir}/sp500_forecasted_stocks_clean.csv',
                output_indicators_file=f'{forecasted_preprocessed_dir}/sp500_forecasted_stock_indicators.csv',
                output_decision_matrix_file=f'{forecasted_preprocessed_dir}/sp500_forecasted_complete_decision_matrix.csv'
            )
            st.success("Data preprocessing complete!")

    # Check if the forecasted data file exists
    forecast_output_file = 'data/forecasted/forecasted_stock.csv'
    if os.path.exists(forecast_output_file):
        # Display a sample of the forecasted data
        forecasted_data = pd.read_csv(forecast_output_file)
        forecasted_data['Date'] = pd.to_datetime(forecasted_data['Date'])
        st.write(f"### Forecasted Data ({forecasted_data['Date'].min().strftime('%Y-%m-%d')} - {forecasted_data['Date'].max().strftime('%Y-%m-%d')})")
        st.dataframe(forecasted_data)
    else:
        st.warning("Forecasted data file not found. Please generate the forecast first.")
