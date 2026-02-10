import boto3
import os
from botocore.exceptions import NoCredentialsError


BUCKET_NAME = "stock-prediction-lake-lord"

def upload_to_s3(file_name, s3_folder="raw"):
    """
    Uploads a local file to an S3 bucket.
    
    :param file_name: The path to the local file (e.g., 'AAPL_raw.csv')
    :param s3_folder: The 'folder' in S3 to store it in (e.g., 'raw' or 'processed')
    """
    s3 = boto3.client('s3')
    
    # If the file is 'AAPL_raw.csv', we want it to be 'raw/AAPL_raw.csv' in S3
    object_name = f"{s3_folder}/{os.path.basename(file_name)}"
    
    try:
        print(f"Uploading {file_name} to s3://{BUCKET_NAME}/{object_name}...")
        s3.upload_file(file_name, BUCKET_NAME, object_name)
        print("Upload Successful!")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test the function with the file we just created
    # Make sure you have 'AAPL_raw.csv' in the same folder
    upload_to_s3("AAPL_raw.csv", s3_folder="raw")