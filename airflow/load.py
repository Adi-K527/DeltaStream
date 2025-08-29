import os
import boto3
import pandas as pd
from io import BytesIO

def load_data_powerbi():
    s3 = boto3.client('s3')
    
    bucket_name = "databricks-mount-1703"
    os.makedirs("data", exist_ok=True)
    tables = ["speed_table", "changes_over_time", "airplane_counts"]

    for table in tables:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{table}/")
        if "Contents" not in response:
            continue

        csv_keys = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith(".csv")]

        combined_df = pd.concat([
            pd.read_csv(BytesIO(s3.get_object(Bucket=bucket_name, Key=key)['Body'].read()))
            for key in csv_keys
        ])

        combined_df.to_csv(f"data/{table}.csv", index=False)