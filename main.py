from extraction import extract_stock_data
from transformation import transform_stock_data
from aws_manager import upload_to_s3
import pandas as pd

def run_pipeline(ticker="AAPL"):
    print(f"--- STARTING PIPELINE FOR {ticker} ---")
    
    # 1. EXTRACT
    print("\n[STEP 1] Extracting...")
    df_raw = extract_stock_data(ticker)
    raw_file = f"{ticker}_raw.csv"
    df_raw.to_csv(raw_file, index=False)
    
    # 2. LOAD RAW TO S3 (Data Lake)
    print("\n[STEP 2] Uploading Raw Data to AWS S3...")
    upload_to_s3(raw_file, s3_folder="raw")
    
    # 3. TRANSFORM
    print("\n[STEP 3] Transforming...")
    # (We could read from S3 here to be pure, but for now let's use local for speed)
    df_clean = transform_stock_data(raw_file)
    clean_file = f"{ticker}_processed.csv"
    df_clean.to_csv(clean_file, index=False)
    
    # 4. LOAD PROCESSED TO S3
    print("\n[STEP 4] Uploading Processed Data to AWS S3...")
    upload_to_s3(clean_file, s3_folder="processed")
    
    print("\n--- PIPELINE FINISHED ---")
    print(f"Check your S3 Bucket: https://s3.console.aws.amazon.com/s3/buckets/")

if __name__ == "__main__":
    run_pipeline("AAPL")