from io import StringIO
import boto3
import pandas as pd


class Aws():
    def __init__(self) -> None:
        self.s3 = boto3.resource('s3')

    def load_df_s3(self, df: pd.DataFrame, bucket: str, file_name: str) -> None:
        """Function to export df to file in S3."""
        csv_buffer = StringIO()
        self.s3.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())