"""
S3 helper functions for data lake operations
"""
import boto3
from io import BytesIO
import pandas as pd
from typing import Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class S3DataLake:
    """Helper class for S3 data lake operations"""
    
    def __init__(self, bucket_name: str, aws_conn_id: str = 'aws_s3'):
        self.bucket_name = bucket_name
        self.aws_conn_id = aws_conn_id
        self.s3_client = boto3.client('s3')
    
    def upload_dataframe_as_parquet(
        self,
        df: pd.DataFrame,
        s3_key: str,
        partition_cols: list = None
    ) -> bool:
        """
        Upload DataFrame to S3 as Parquet
        
        Args:
            df: DataFrame to upload
            s3_key: S3 key (path) for the file
            partition_cols: Columns to partition by
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to parquet in memory
            parquet_buffer = BytesIO()
            df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
            parquet_buffer.seek(0)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=parquet_buffer.getvalue(),
                ContentType='application/octet-stream'
            )
            
            logger.info(f"Uploaded {s3_key} to s3://{self.bucket_name}/{s3_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload {s3_key}: {str(e)}")
            return False
    
    def create_success_marker(self, s3_prefix: str) -> bool:
        """
        Create _SUCCESS marker file to indicate complete write
        
        Args:
            s3_prefix: S3 prefix (directory path)
        
        Returns:
            True if successful
        """
        try:
            success_key = f"{s3_prefix}/_SUCCESS"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=success_key,
                Body=b'',
            )
            logger.info(f"Created success marker: {success_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to create success marker: {str(e)}")
            return False