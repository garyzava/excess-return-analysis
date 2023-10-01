import requests
import time
import csv
import sys
from datetime import datetime

BASE_URL = "https://api.binance.com/api/v3/aggTrades"

def log_message(message, log_file):
    """Write a message to the log file and print it to the console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as log:
        log.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")

def date_to_epoch(date_str):
    """Convert a date string (YYYY-MM-DD) to epoch timestamp in milliseconds."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return int(dt.timestamp() * 1000)

def fetch_binance_data(symbol, startTime, endTime, log_file_name, limit=1000):
    all_trades = []
    last_trade_timestamp = 0

    while True:
        params = {
            "symbol": symbol,
            "startTime": max(startTime, last_trade_timestamp + 1),
            "endTime": endTime,
            "limit": limit
        }

        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            trades = response.json()
            if isinstance(trades, dict) and "code" in trades and "msg" in trades:
                log_message(f"Error fetching data: {trades['msg']}", log_file_name)
                return all_trades
            valid_trades = [trade for trade in trades if not (trade["p"] == '0' and trade["q"] == '0' and trade["f"] == -1 and trade["l"] == -1)]
            log_message(f"Fetched {len(valid_trades)} records for the interval {params['startTime']} to {params['endTime']}.", log_file_name)
            all_trades.extend(valid_trades)

            if len(valid_trades) < limit:
                break
            else:
                last_trade_timestamp = valid_trades[-1]["T"]
        else:
            log_message(f"Error {response.status_code}: {response.text}", log_file_name)
            return all_trades

    return all_trades

def fetch_data_for_timeframe(symbol, start_date, end_date, output_file, log_file_name):
    current_start = date_to_epoch(start_date)
    end_timestamp = date_to_epoch(end_date) + (24 * 60 * 60 * 1000) - 1

    # Write the CSV header only once at the beginning
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Aggregate tradeId", "Price", "Quantity", "First tradeId", "Last tradeId", "Timestamp", "Was the buyer the maker?", "Was the trade the best price match?"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    while current_start < end_timestamp:
        current_end = current_start + (24 * 60 * 60 * 1000)
        if current_end > end_timestamp:
            current_end = end_timestamp

        data = fetch_binance_data(symbol, current_start, current_end, log_file_name)

        # Save the fetched data for the current day to the CSV
        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = ["Aggregate tradeId", "Price", "Quantity", "First tradeId", "Last tradeId", "Timestamp", "Was the buyer the maker?", "Was the trade the best price match?"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for row in data:
                writer.writerow({
                    "Aggregate tradeId": row["a"],
                    "Price": row["p"],
                    "Quantity": row["q"],
                    "First tradeId": row["f"],
                    "Last tradeId": row["l"],
                    "Timestamp": row["T"],
                    "Was the buyer the maker?": row["m"],
                    "Was the trade the best price match?": row["M"]
                })

        log_message(f"Data for interval {current_start} to {current_end} written to {output_file}", log_file_name)
        current_start = current_end
        time.sleep(1.1)

    log_message(f"Data fetching and saving completed for {start_date} to {end_date}.", log_file_name)


def main():
    start_time = time.time()

    symbol = "BTCUSDT"
    
    # Check for command-line arguments for start_date and end_date
    if len(sys.argv) == 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    else:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

    output_file = f"binance_data_{start_date}_to_{end_date}.csv"
    log_file_name = f"binance_data_log_{start_date}_to_{end_date}.txt"
    
    fetch_data_for_timeframe(symbol, start_date, end_date, output_file, log_file_name)

    end_time = time.time()
    elapsed_time = end_time - start_time
    log_message(f"Script completed in {elapsed_time:.2f} seconds.", log_file_name)

if __name__ == "__main__":
    main()
