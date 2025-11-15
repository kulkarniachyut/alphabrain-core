"""
Data fetching utilities for financial data using Alpha Vantage
"""
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict
import logging
import time

logger = logging.getLogger(__name__)


def fetch_stock_prices_alpha_vantage(
    symbols: List[str],
    api_key: str,
    outputsize: str = 'compact'
) -> Dict[str, pd.DataFrame]:
    """
    Fetch stock price data using Alpha Vantage API
    
    Args:
        symbols: List of stock symbols (e.g., ['AAPL', 'TSLA'])
        api_key: Alpha Vantage API key
        outputsize: 'compact' (100 days) or 'full' (20+ years)
    
    Returns:
        Dictionary mapping symbol to DataFrame
    """
    results = {}
    base_url = "https://www.alphavantage.co/query"
    
    for symbol in symbols:
        try:
            logger.info(f"Fetching data for {symbol} from Alpha Vantage")
            
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': api_key,
                'outputsize': outputsize,
                'datatype': 'json'
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                logger.error(f"API error for {symbol}: {data['Error Message']}")
                continue
            
            if 'Note' in data:
                logger.warning(f"API rate limit hit: {data['Note']}")
                time.sleep(60)  # Wait 1 min if rate limited
                continue
            
            if 'Time Series (Daily)' not in data:
                logger.error(f"Unexpected response for {symbol}: {data.keys()}")
                continue
            
            # Convert to DataFrame
            time_series = data['Time Series (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            
            # Rename columns
            df.columns = ['open', 'high', 'low', 'close', 'volume']
            df.index.name = 'date'
            df.reset_index(inplace=True)
            
            # Convert types
            df['date'] = pd.to_datetime(df['date'])
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
            
            # Add metadata
            df['symbol'] = symbol
            df['fetch_timestamp'] = datetime.utcnow()
            
            # Sort by date descending
            df = df.sort_values('date', ascending=False)
            
            results[symbol] = df
            logger.info(f"Successfully fetched {len(df)} rows for {symbol}")
            
            # Rate limit: 5 calls/min for free tier
            time.sleep(12)  # 12s between calls = 5/min
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching {symbol}: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Error fetching {symbol}: {str(e)}")
            continue
    
    return results


# Backward compatibility - keep old function name
def fetch_stock_prices(symbols: List[str], start_date: str, end_date: str, api_key: str = None) -> Dict[str, pd.DataFrame]:
    """Wrapper for backward compatibility"""
    if api_key is None:
        raise ValueError("API key required for Alpha Vantage")
    
    # Fetch full data, then filter by date
    all_data = fetch_stock_prices_alpha_vantage(symbols, api_key)
    
    # Filter to date range
    filtered_data = {}
    for symbol, df in all_data.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df[mask].copy()
        if not filtered_df.empty:
            filtered_data[symbol] = filtered_df
    
    return filtered_data