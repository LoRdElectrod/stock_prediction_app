import boto3
import os
import streamlit as st
from botocore.exceptions import NoCredentialsError

# CHANGE THIS to your actual bucket name
BUCKET_NAME = "stock-prediction-lake-lord"

def get_s3_client():
    # Check if running on Streamlit Cloud with secrets
    if hasattr(st, "secrets") and "aws" in st.secrets:
        return boto3.client(
            's3',
            aws_access_key_id=st.secrets["aws"]["aws_access_key_id"],
            aws_secret_access_key=st.secrets["aws"]["aws_secret_access_key"],
            region_name="us-east-1"
        )
    else:
        # Fallback to local computer credentials
        return boto3.client('s3')

def upload_to_s3(file_name, s3_folder="raw"):
    s3 = get_s3_client()
    object_name = f"{s3_folder}/{os.path.basename(file_name)}"
    
    try:
        s3.upload_file(file_name, BUCKET_NAME, object_name)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False