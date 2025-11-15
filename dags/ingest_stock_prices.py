"""
DAG: Ingest Stock Prices
Fetches daily stock prices and stores in S3 data lake
"""
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import logging

from utils.data_fetcher import fetch_stock_prices
from utils.s3_helper import S3DataLake
from airflow.models import Variable

logger = logging.getLogger(__name__)

# DAG configuration
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


@dag(
    dag_id='ingest_stock_prices',
    default_args=default_args,
    description='Fetch stock prices from Alpha Vantage and save to S3',
    schedule='0 14 * * 1-5',  # Mon-Fri only at 2 PM UTC
    start_date=datetime(2025, 11, 11),  # Start on a Monday
    catchup=False,
    tags=['ingestion', 'stocks', 'daily'],
)


def stock_price_ingestion():
    
    @task()
    def fetch_prices(**context):
        """Fetch stock prices for configured symbols"""
        
        # Get API key from Airflow Variables
        api_key = Variable.get("ALPHA_VANTAGE_API_KEY")
        
        # Get execution date
        exec_date = datetime.fromisoformat(context['ds'])
        
        # Find last trading day (skip weekends, get previous day's close data)
        fetch_date = exec_date - timedelta(days=1)
        
        # Skip weekends - if Saturday/Sunday, go back to Friday
        while fetch_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
            fetch_date = fetch_date - timedelta(days=1)
        
        fetch_date_str = fetch_date.strftime('%Y-%m-%d')
        
        # Configuration
        symbols = ['AAPL']
        
        logger.info(f"Execution date: {context['ds']}, Fetching data for: {fetch_date_str}")
        
        # Fetch data
        data = fetch_stock_prices(
            symbols=symbols,
            start_date=fetch_date_str,
            end_date=fetch_date_str,
            api_key=api_key
        )
        
        if not data:
            raise ValueError(f"No data fetched for any symbol on {fetch_date_str}")
        
        return {
            'symbols': list(data.keys()),
            'date': fetch_date_str,
            'record_counts': {sym: len(df) for sym, df in data.items()},
            'api_key': api_key
        }
    
    @task()
    def save_to_s3(fetch_result: dict):
        """Save fetched data to S3 data lake"""
        
        s3_lake = S3DataLake(bucket_name='alphabrain-core-dev-data')
        date = fetch_result['date']
        api_key = fetch_result['api_key']
        
        # Re-fetch data (in production, pass via XCom or persistent storage)
        symbols = fetch_result['symbols']
        data = fetch_stock_prices(
            symbols=symbols,
            start_date=date,
            end_date=date,
            api_key=api_key
        )
        
        # Upload each symbol
        uploaded_files = []
        for symbol, df in data.items():
            s3_key = f"raw/market/prices/date={date}/{symbol}.parquet"
            success = s3_lake.upload_dataframe_as_parquet(df, s3_key)
            
            if success:
                uploaded_files.append(s3_key)
        
        # Create success marker
        s3_prefix = f"raw/market/prices/date={date}"
        s3_lake.create_success_marker(s3_prefix)
        
        return {
            'uploaded_files': uploaded_files,
            'date': date
        }
    
    @task()
    def log_metadata(save_result: dict):
        """Log ingestion metadata to Postgres"""
        
        postgres_hook = PostgresHook(postgres_conn_id='airflow_db')
        
        for file_path in save_result['uploaded_files']:
            symbol = file_path.split('/')[-1].replace('.parquet', '')
            
            insert_sql = """
            INSERT INTO data_lineage (
                dataset_name, source, ingestion_ts, 
                s3_path, schema_version
            ) VALUES (
                %s, %s, NOW(), %s, %s
            )
            """
            
            postgres_hook.run(
                insert_sql,
                parameters=(
                    f"stock_prices_{symbol}",
                    "alpha_vantage", 
                    f"s3://alphabrain-core-dev-data/{file_path}",
                    1  # schema version
                )
            )
        
        logger.info(f"Logged {len(save_result['uploaded_files'])} files to metadata")
        return True
    
    # Define task dependencies
    fetch_result = fetch_prices()
    save_result = save_to_s3(fetch_result)
    log_metadata(save_result)


# Instantiate the DAG
stock_price_dag = stock_price_ingestion()