import yfinance as yf
import pandas as pd
from datetime import datetime

def extract_stock_data(symbol="AAPL", period="2y"):
    """
    Downloading historical stock data from Yahoo Finance.
    period: '1mo', '1y', '2y', '5y', 'max'
    """
    print(f"Extracting data for {symbol}...")
    
    # Fetch data
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    
    # Reset index so 'Date' becomes a column (easier for databases)
    df.reset_index(inplace=True)
    
    # We only need the core columns for now
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Add a column to track when we extracted this
    df['extraction_date'] = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Extracted {len(df)} rows.")
    return df

if __name__ == "__main__":
    # AAPL is Apple
    symbol = "AAPL"
    df = extract_stock_data(symbol)
    
    # Save locally to inspect
    filename = f"{symbol}_raw.csv"
    df.to_csv(filename, index=False)
    print(f"Saved raw data to {filename}")