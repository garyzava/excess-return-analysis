import pandas as pd
import numpy as np

def compute_rsi_corrected(data, window):
    """
    Compute the Relative Strength Index (RSI) for a given data series.
    """
    diff = data.diff()
    
    # If the difference is positive, set gain to the difference and loss to 0; otherwise, do the opposite.
    gain = diff.where(diff > 0, 0)
    loss = -diff.where(diff < 0, 0)
    
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    
    # Handle division by zero and NaN values
    rs = rs.fillna(0).replace([np.inf, -np.inf], 0)
    
    rsi = 100 - (100 / (1 + rs))
    return rsi

def transform_hourly(df):
    # Resample the data to hourly intervals
    hourly_df = df.resample('H').agg({
        'Price': ['first', 'max', 'min', 'last'],
        'Quantity': 'sum',
        'Was the buyer the maker?': lambda x: (x == True).sum(),
        'Was the trade the best price match?': lambda x: (x == True).sum()
    })
    # Flatten the MultiIndex columns
    hourly_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Taker_buy_base', 'Taker_buy_quote']
    # Calculate the Quote asset volume
    hourly_df['Quote_asset_volume'] = hourly_df['Volume'] * hourly_df['Close']
    # Calculate the Number of trades
    hourly_df['Number_of_trades'] = df.resample('H').size()
    # Compute RSI for the specified timeframes
    hourly_df['RSI_14H'] = compute_rsi_corrected(hourly_df['Close'], window=14) # 14 hours
    hourly_df['RSI_1D'] = compute_rsi_corrected(hourly_df['Close'], window=24) # 24 hours
    hourly_df['RSI_7D'] = compute_rsi_corrected(hourly_df['Close'], window=24*7) # 24*7 hours
    
    return hourly_df

def transform_daily(df):
    # Resample the data to daily intervals
    daily_df = df.resample('D').agg({
        'Price': ['first', 'max', 'min', 'last'],
        'Quantity': 'sum',
        'Was the buyer the maker?': lambda x: (x == True).sum(),
        'Was the trade the best price match?': lambda x: (x == True).sum()
    })
    daily_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Taker_buy_base', 'Taker_buy_quote']
    daily_df['Quote_asset_volume'] = daily_df['Volume'] * daily_df['Close']
    daily_df['Number_of_trades'] = df.resample('D').size()
    daily_df['RSI_7D'] = compute_rsi_corrected(daily_df['Close'], window=7)  # 7 days
    daily_df['RSI_14D'] = compute_rsi_corrected(daily_df['Close'], window=14)  # 14 days
    
    return daily_df

def main():
    df = pd.read_csv('binance_data.csv')
    # Convert the Timestamp column to a datetime format
    df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    # Set the Datetime column as the index
    df.set_index('Datetime', inplace=True)
    
    hourly_data = transform_hourly(df)
    daily_data = transform_daily(df)

    hourly_data.to_csv('hourly_data.csv')
    daily_data.to_csv('daily_data.csv')

if __name__ == "__main__":
    main()
