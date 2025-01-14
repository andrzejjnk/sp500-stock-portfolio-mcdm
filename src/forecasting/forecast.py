import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def filter_invalid_data(data):
    """
    Removes rows where all financial columns are NaN for a given symbol.

    Parameters:
    - data (pd.DataFrame): Input stock data.

    Returns:
    - pd.DataFrame: Cleaned data with invalid rows removed.
    """
    columns_to_check = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']

    data_cleaned = data.dropna(subset=columns_to_check, how='all')
    return data_cleaned

def forecast_all_columns(data, forecast_period, output_file):
    """
    Forecasts all columns for each stock using ARIMA.

    Parameters:
    - data (pd.DataFrame): DataFrame containing stock data with 'Symbol', 'Date', and numeric columns to forecast.
    - forecast_period (int): Number of days to forecast.
    - output_file (str): Path to save the forecasted data as a CSV file.
    """
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = filter_invalid_data(data)

    forecast_results = []

    data['Date'] = pd.to_datetime(data['Date'])

    columns_to_forecast = data.select_dtypes(include=[np.number]).columns.tolist()

    for symbol in data['Symbol'].unique():
        stock_data = data[data['Symbol'] == symbol].sort_values('Date')

        # Ensure there are enough data points for ARIMA
        if len(stock_data) < 10:
            print(f"Skipping {symbol}: Not enough data points for ARIMA.")
            continue

        forecasted_values = {'Symbol': [], 'Date': [], 'Column': [], 'Forecasted Value': []}
        for column in columns_to_forecast:
            try:
                series = stock_data[column].values

                # Fit ARIMA model
                model = ARIMA(series, order=(1, 1, 1))  # ARIMA(1,1,1) configuration
                fitted_model = model.fit()
                forecast = fitted_model.forecast(steps=forecast_period)

                last_date = stock_data['Date'].iloc[-1]
                forecast_dates = [last_date + pd.Timedelta(days=i) for i in range(1, forecast_period + 1)]

                for date, value in zip(forecast_dates, forecast):
                    forecasted_values['Symbol'].append(symbol)
                    forecasted_values['Date'].append(date)
                    forecasted_values['Column'].append(column)
                    forecasted_values['Forecasted Value'].append(value)

            except Exception as e:
                print(f"Error forecasting {symbol}, column {column}: {e}")
                continue

        forecast_df = pd.DataFrame(forecasted_values)
        forecast_results.append(forecast_df)

    # Combine all forecasted data into one DataFrame and save
    all_forecasts = pd.concat(forecast_results, ignore_index=True)
    all_forecasts.to_csv(output_file, index=False)
    print(f"Forecast saved to {output_file}")


def transform_forecast_data(forecast_file, output_file):
    """
    Transforms the forecast data from the format 'Symbol, Date, Column, Forecasted Value'
    to the format 'Date, Symbol, Adj Close, Close, High, Low, Open, Volume'.

    Parameters:
    - forecast_file (str): Path to the input forecast CSV file.
    - output_file (str): Path to save the transformed data as a CSV file.
    """
    # Read the forecast data
    forecast_data = pd.read_csv(forecast_file)

    # Pivot the data to get the desired format
    pivot_data = forecast_data.pivot_table(index=['Date', 'Symbol'], columns='Column', values='Forecasted Value').reset_index()

    # Rename columns to match the desired format
    pivot_data.columns.name = None
    pivot_data = pivot_data.rename_axis(None, axis=1)

    # Reorder columns to match the desired format
    desired_columns = ['Date', 'Symbol', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    pivot_data = pivot_data.reindex(columns=desired_columns)

    # Save the transformed data to a CSV file
    pivot_data.to_csv(output_file, index=False)
    print(f"Transformed forecast saved to {output_file}")
