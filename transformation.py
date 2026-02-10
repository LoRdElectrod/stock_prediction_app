import pandas as pd

def transform_stock_data(input_file="AAPL_raw.csv"):
    """
    Reads raw stock data, calculates technical indicators, and prepares target variable.
    """
    print(f"Transforming data from {input_file}...")
    
    # 1. Load Data
    df = pd.read_csv(input_file)
    
    # Convert Date to datetime object for proper sorting
    # utc=True handles timezone aware strings if present
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df = df.sort_values('Date')
    
    # 2. Feature Engineering 
    
    # Moving Average (50 days): Shows the long-term trend
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    # Daily Return: Percentage change from previous day
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Volatility (High - Low)
    df['Volatility'] = df['High'] - df['Low']
    
    # 3. Create the "Target" (What we want to predict)
    # We want to know: Will the price be HIGHER tomorrow?
    # Shift(-1) allows us to see "tomorrow's" price on "today's" row
    df['Next_Day_Close'] = df['Close'].shift(-1)
    
    # Target = 1 if Tomorrow > Today, else 0
    df['Target'] = (df['Next_Day_Close'] > df['Close']).astype(int)
    
    # 4. Clean Data
    # Rolling averages create NaNs at the start (first 50 rows)
    # Shift(-1) creates a NaN at the very end (can't see the future)
    df_clean = df.dropna()
    
    print(f"Data transformed. Rows after cleaning: {len(df_clean)}")
    return df_clean

if __name__ == "__main__":
    df = transform_stock_data()
    
    # Save to a new CSV 
    output_file = "AAPL_transformed.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved transformed data to {output_file}")