import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATASET_DIR = os.path.join(os.path.dirname(__file__), 'datasets')
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(os.path.join(DATASET_DIR, 'uploads'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'models_saved'), exist_ok=True)

TICKERS = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc. (Google)',
    'TSLA': 'Tesla Inc.',
    'AMZN': 'Amazon.com Inc.',
    'NVDA': 'NVIDIA Corporation'
}

def generate_synthetic_stock(symbol, days=730, start_price=150.0):
    """Generate realistic OHLCV stock data if network download fails."""
    np.random.seed(abs(hash(symbol)) % (2**32))
    end_date = datetime.now()
    dates = pd.date_range(end=end_date, periods=days, freq='B')
    
    # Geometric Brownian Motion
    mu = 0.0006
    sigma = 0.018
    returns = np.random.normal(mu, sigma, size=len(dates))
    price = start_price * np.exp(np.cumsum(returns))
    
    high = price * (1 + np.abs(np.random.normal(0, 0.008, size=len(dates))))
    low = price * (1 - np.abs(np.random.normal(0, 0.008, size=len(dates))))
    open_p = low + np.random.uniform(0.2, 0.8, size=len(dates)) * (high - low)
    close_p = low + np.random.uniform(0.2, 0.8, size=len(dates)) * (high - low)
    volume = np.random.randint(15000000, 85000000, size=len(dates))
    
    df = pd.DataFrame({
        'Date': dates.strftime('%Y-%m-%d'),
        'Open': np.round(open_p, 2),
        'High': np.round(high, 2),
        'Low': np.round(low, 2),
        'Close': np.round(close_p, 2),
        'Adj Close': np.round(close_p, 2),
        'Volume': volume
    })
    return df

def fetch_or_cache():
    for ticker in TICKERS:
        file_path = os.path.join(DATASET_DIR, f"{ticker}.csv")
        try:
            print(f"Downloading historical data for {ticker}...")
            df = yf.download(ticker, period="3y", interval="1d", auto_adjust=False)
            if df is not None and len(df) > 50:
                # Flatten multi-level columns if present in newer yfinance versions
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df = df.reset_index()
                # Ensure date format is YYYY-MM-DD
                df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
                cols_to_keep = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
                available_cols = [c for c in cols_to_keep if c in df.columns]
                df = df[available_cols]
                df.to_csv(file_path, index=False)
                print(f"Saved {ticker}.csv with {len(df)} rows.")
                continue
        except Exception as e:
            print(f"yfinance failed for {ticker}: {e}. Generating synthetic fallback.")
        
        # Fallback if download failed
        start_prices = {'AAPL': 175.0, 'MSFT': 320.0, 'GOOGL': 135.0, 'TSLA': 210.0, 'AMZN': 140.0, 'NVDA': 480.0}
        df = generate_synthetic_stock(ticker, days=730, start_price=start_prices.get(ticker, 150.0))
        df.to_csv(file_path, index=False)
        print(f"Generated synthetic {ticker}.csv with {len(df)} rows.")

if __name__ == '__main__':
    fetch_or_cache()
