"""
Alpha Vantage Data Fetcher

This script allows users to fetch news sentiment data related to specific topics and tickers 
from the Alpha Vantage API. The data fetched includes details like title, URL, time published, 
authors, summary, banner image, source, category within the source, source domain, topics, 
overall sentiment score, and overall sentiment label. The fetched data is saved as a CSV file.

Requirements:
    - Python3
    - `requests` library
    - Free API key from Alpha Vantage

Usage:
    1. Ensure you have the required Python libraries installed.
       You can install them using pip:
       ```
       pip install requests
       ```

    2. Set the `ALPHA_API_KEY` constant variable in the script to your Alpha Vantage API key.

    3. To fetch data for a specific timeframe, run the script and provide the start and end dates as arguments:
       ```
       python script_name.py YYYY-MM-DD YYYY-MM-DD
       ```

       Alternatively, if you run the script without arguments, it will prompt you to manually enter the start and end dates.

Output:
    The script will save the fetched data in a CSV file named "alpha_data_STARTDATE_to_ENDDATE.csv" 
    and will also log messages to a log file named "alpha_data_log_STARTDATE_to_ENDDATE.txt".

Rate Limit:
    The script respects Alpha Vantage's rate limit of 5 requests per minute. 
    If the rate limit is reached, the script will automatically pause until it can make the next request.

Author:
    Gary Zavaleta

Version: 1.0
"""

import requests
import time
import csv
import sys
from datetime import datetime, timedelta

ALPHA_API_KEY = "" #add your free API key here
BASE_URL = "https://www.alphavantage.co/query"
FUNCTION = "NEWS_SENTIMENT",
TOPICS = "blockchain",
TICKERS = "CRYPTO:BTC"
TIME_INTERVAL = 10 #Time interval for pulling data from the API

#Rate Limit constants
REQUESTS_COUNT = 0
LAST_REQUEST_TIME = None

def add_one_hour_to_alpha_format(alpha_date_str):
    """Add one hour to a date string in Alpha Vantage's format YYYYMMDDTHHMM."""
    dt = datetime.strptime(alpha_date_str, '%Y%m%dT%H%M')
    dt += timedelta(hours=1)
    return dt.strftime('%Y%m%dT%H%M')

def add_one_minute_to_alpha_format(alpha_date_str):
    """Add one hour to a date string in Alpha Vantage's format YYYYMMDDTHHMM."""
    dt = datetime.strptime(alpha_date_str, '%Y%m%dT%H%M')
    dt += timedelta(minutes=1)
    return dt.strftime('%Y%m%dT%H%M')    

def log_message(message, log_file):
    """Write a message to the log file and print it to the console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as log:
        log.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")

# def date_to_alpha_format(date_str):
#     """Convert a date string (YYYY-MM-DD) to Alpha Vantage's format YYYYMMDDTHHMM."""
#     return date_str.replace("-", "") + "T0000"

def date_to_alpha_format(date_str):
   dt = datetime.strptime(date_str, '%Y-%m-%d')
   return dt.strftime('%Y%m%dT%H%M')


def fetch_alpha_data(api_key, start_date, end_date, log_file_name, limit=1000):
    global REQUESTS_COUNT
    global LAST_REQUEST_TIME

    all_articles = []
    last_article_date = start_date

    waited_once = False  # Flag to check if we've already waited once

    while True:
        if REQUESTS_COUNT >= 5:
            # Calculate time to wait for the next minute
            wait_time = 60 - (time.time() - LAST_REQUEST_TIME)
            log_message(f"Rate limit reached. Sleeping for {wait_time:.2f} seconds.", log_file_name)
            time.sleep(wait_time)
            REQUESTS_COUNT = 0            

        #print("start_date:- ", start_date)
        #print("MAX:- ",max(start_date,add_one_minute_to_alpha_format(last_article_date)))
        #print("end_date:- ", end_date)
        params = {
            "function": FUNCTION,
            "topics": TOPICS,
            "tickers": TICKERS,
            "time_from": max(start_date,add_one_minute_to_alpha_format(last_article_date)),
            "time_to": end_date,
            #"time_from": start_date,
            #"time_to": end_date,           
            "limit": limit,
            "sort": "EARLIEST",            
            "apikey": api_key
        }

        params2 = {
            "function": FUNCTION,
            "topics": TOPICS,
            "tickers": TICKERS,
            "time_from": "20220101T0000",
            "time_to": "20220115T0000",
            "limit": 1000,
            "sort": "EARLIEST",
            "apikey": api_key
        }

        # response = requests.get(BASE_URL, params=params2)
        # if response.status_code == 200:
        #     data = response.json()
        #     if "Error Message" in data:
        #         print(f"Error fetching data: {data['Error Message']}")
        #         #return []
        #     articles = data.get('feed', [])
        #     print("response2:- ",response.json())
        #     print("articles2:- ", articles)
        #     for article in articles[:5]:
        #          print(article)
        # else:
        #     print(f"Error {response.status_code}: {response.text}")
        #     #return []


        response = requests.get(BASE_URL, params=params)
        #print("response:- ",response.json())

        # Update request count and time after making the request
        REQUESTS_COUNT += 1
        LAST_REQUEST_TIME = time.time()
        
        if response.status_code == 200:
            data = response.json()
            if "Error Message" in data:
                log_message(f"Error fetching data: {data['Error Message']}", log_file_name)
                return all_articles
            #articles = [article for article in data.get('feed', []) if article.get('title') and article.get('url')]
            # if waited_once:
            #     log_message(f"No articles fetched again after waiting. Aborting the script.", log_file_name)
            #     sys.exit(1)
            # else:
            #     log_message(f"No articles fetched. Waiting for one minute before the next request...", log_file_name)
            #     time.sleep(60)
            #     waited_once = True
            #     continue

            articles = data.get('feed', [])
            log_message(f"Fetched {len(articles)} articles from {last_article_date} to {end_date}.", log_file_name)
            all_articles.extend(articles)

            if len(articles) < limit:
                break
            else:
                print("BREAK Warning limit")
                # Increment the last_article_date by one day for the next iteration
                last_article_date = (datetime.strptime(last_article_date, '%Y-%m-%d') + timedelta(minutes=1)).strftime('%Y-%m-%d')
                print("last_article_date:- ", last_article_date)
        else:
            log_message(f"Error {response.status_code}: {response.text}", log_file_name)
            return all_articles

    return all_articles

def fetch_data_for_timeframe(api_key, start_date, end_date, output_file, log_file_name):
    current_start = date_to_alpha_format(start_date)
    #end_timestamp = date_to_alpha_format(end_date) + (24 * 60 * 60 * 1000) - 1 # TODO
    end_timestamp = date_to_alpha_format(end_date)

    # Write the CSV header only once at the beginning
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["title", "url", "time_published", "authors", "summary", "banner_image", "source", "category_within_source", "source_domain", "topics", "overall_sentiment_score", "overall_sentiment_label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    while current_start < end_timestamp:
        print("current_start:- ", current_start)
        #current_end = current_start + (24 * 60 * 60 * 1000) #TODO
        #current_end = (datetime.strptime(current_start, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        current_end = (datetime.strptime(current_start, '%Y%m%dT%H%M') + timedelta(days=TIME_INTERVAL)).strftime('%Y%m%dT%H%M')
        print("current_end:- ", current_end)
        if current_end > end_timestamp:
            current_end = end_timestamp

        data = fetch_alpha_data(api_key, current_start, current_end, log_file_name)

        # Save the fetched data for the current day to the CSV
        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = ["title", "url", "time_published", "authors", "summary", "banner_image", "source", "category_within_source", "source_domain", "topics", "overall_sentiment_score", "overall_sentiment_label"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for row in data:
                writer.writerow({
                    "title": row["title"],
                    "url": row["url"],
                    "time_published": row["time_published"],
                    "authors": ", ".join(row["authors"]),
                    "summary": row["summary"],
                    "banner_image": row["banner_image"],
                    "source": row["source"],
                    "category_within_source": row["category_within_source"],
                    "source_domain": row["source_domain"],
                    "topics": ", ".join([topic["topic"] for topic in row["topics"]]),
                    "overall_sentiment_score": row["overall_sentiment_score"],
                    "overall_sentiment_label": row["overall_sentiment_label"]
                })

        log_message(f"Data for interval {current_start} to {current_end} written to {output_file}", log_file_name)
        current_start = current_end
        #time.sleep(1.1)

    log_message(f"Data fetching and saving completed for {start_date} to {end_date}.", log_file_name)


def fetch_alpha_data2(api_key, start_date, end_date):
    params = {
        "function": FUNCTION,
        "topics": TOPICS,
        "tickers": TICKERS,
        "time_from": start_date,
        "time_to": end_date,
        "limit": 1000,
        "sort": "EARLIEST",
        "apikey": api_key
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "Error Message" in data:
            print(f"Error fetching data: {data['Error Message']}")
            return []
        return data.get('feed', [])
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# def main():
#     api_key = ALPHA_API_KEY
#     start_date = input("Enter the start date (YYYY-MM-DD): ")
#     end_date = input("Enter the end date (YYYY-MM-DD): ")
#     start_date = date_to_alpha_format(start_date)
#     end_date = date_to_alpha_format(end_date)
    
#     data = fetch_alpha_data2(api_key, start_date, end_date)
#     for article in data[:5]:
#         print(article)


def main():
    start_time = time.time()

    api_key = ALPHA_API_KEY
    
    # Check for command-line arguments for start_date and end_date
    if len(sys.argv) == 3:
        start_date = sys.argv[1]
        end_date = sys.argv[2]
    else:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

    output_file = f"alpha_data_{start_date}_to_{end_date}.csv"
    log_file_name = f"alpha_data_log_{start_date}_to_{end_date}.txt"
    
    fetch_data_for_timeframe(api_key, start_date, end_date, output_file, log_file_name)

    end_time = time.time()
    elapsed_time = end_time - start_time
    log_message(f"Script completed in {elapsed_time:.2f} seconds.", log_file_name)

if __name__ == "__main__":
    main()
