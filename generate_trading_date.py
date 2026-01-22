import os
import pandas as pd
import argparse

# Generate Trading Date List
def generate_trading_date_list(dataset):
    price_dir = f"dataset/{dataset}/price/"
    # Get the first CSV file in the directory
    ticker_csv = os.listdir(price_dir)[0]
    price_path = os.path.join(price_dir, ticker_csv)
    df = pd.read_csv(price_path)

    ticker_csv_list = df['Date'].tolist()

    df = pd.DataFrame(ticker_csv_list, columns=['Date'])
    df.to_csv("dataset/trading_date_list.csv", index=False)
    print(f"Generated trading_date_list.csv with {len(ticker_csv_list)} dates")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="CSMD50")
    args = parser.parse_args()
    
    generate_trading_date_list(dataset = args.dataset)
