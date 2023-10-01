## Installation

To use these scripts, follow these steps:

1. Clone the repository.
2. Create a python virtual environment `python3 -m venv venv` and activate it `venv/bin/activate`
3. Install the necessary dependencies using `pip install -r requirements.txt`.

## Dependencies

These scripts require the following dependencies:

- Python 3.7 or higher
- Pandas
- NumPy
- Requests
- Datatime

## Usage

To use these scripts, follow these steps:

1. The script `binance_api_fetcher.py`: gets binance data in chunks per epoch.
2. The script `alphavantage_api_fetcher.py`: gets news data in chunks per 10 days. Verify the rate limits per day on the alphavantage website
3. The script `trade_stats_prep.py`: transforms the trade stats data from Binance into hourly and daily timeframes, additionally adds RSI technical analysis metrics.

Run any script using `python -m <script_name.py>`