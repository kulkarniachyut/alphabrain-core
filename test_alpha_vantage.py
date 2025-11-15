#!/usr/bin/env python3
"""
Test Alpha Vantage data fetching locally
"""
import sys
sys.path.insert(0, 'dags')

from utils.data_fetcher import fetch_stock_prices
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fetch():
    """Test fetching stock data"""
    
    # Your API key
    api_key = input("Enter Alpha Vantage API Key: ")
    
    # Test parameters
    symbols = ['AAPL']  # Start with just 1 symbol
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    logger.info(f"Testing fetch for {symbols} on {yesterday}")
    
    # Fetch
    data = fetch_stock_prices(
        symbols=symbols,
        start_date=yesterday,
        end_date=yesterday,
        api_key=api_key
    )
    
    # Results
    if data:
        for symbol, df in data.items():
            print(f"\n✅ {symbol}: {len(df)} rows")
            print(df.head())
            print(f"\nColumns: {df.columns.tolist()}")
    else:
        print("❌ No data returned")

if __name__ == "__main__":
    test_fetch()