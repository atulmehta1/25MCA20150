import os
import re
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from config import Config

def sanitize_symbol(symbol):
    return re.sub(r'[^A-Za-z0-9\.\-]', '', symbol).upper()

def normalize_columns(df):
    """Normalize common variations of OHLCV column names."""
    mapping = {}
    for col in df.columns:
        c_lower = col.strip().lower()
        if c_lower in ['date', 'timestamp', 'time', 'datetime']:
            mapping[col] = 'Date'
        elif c_lower in ['open', 'open_price', 'openprice']:
            mapping[col] = 'Open'
        elif c_lower in ['high', 'high_price', 'highprice']:
            mapping[col] = 'High'
        elif c_lower in ['low', 'low_price', 'lowprice']:
            mapping[col] = 'Low'
        elif c_lower in ['close', 'close_price', 'closeprice']:
            mapping[col] = 'Close'
        elif c_lower in ['adj close', 'adjclose', 'adjusted_close', 'adj_close']:
            mapping[col] = 'Adj Close'
        elif c_lower in ['volume', 'vol', 'total_volume']:
            mapping[col] = 'Volume'
            
    df = df.rename(columns=mapping)
    return df

def get_stock_data(symbol_or_filename):
    """
    Retrieve dataset dataframe by symbol (AAPL) or filename (uploads/custom.csv).
    If not local, attempts to download via yfinance.
    """
    symbol_or_filename = str(symbol_or_filename).strip()
    
    # 1. Check custom uploaded file
    upload_path = os.path.join(Config.UPLOAD_FOLDER, symbol_or_filename)
    if os.path.exists(upload_path):
        df = pd.read_csv(upload_path)
        return normalize_columns(df)
        
    # 2. Check pre-bundled dataset
    sym = sanitize_symbol(symbol_or_filename.replace('.csv', ''))
    base_path = os.path.join(Config.DATASET_FOLDER, f"{sym}.csv")
    if os.path.exists(base_path):
        df = pd.read_csv(base_path)
        return normalize_columns(df)
        
    # 3. Fetch from Yahoo Finance if network available
    try:
        yf_df = yf.download(sym, period="2y", interval="1d", auto_adjust=False)
        if yf_df is not None and len(yf_df) > 30:
            if isinstance(yf_df.columns, pd.MultiIndex):
                yf_df.columns = yf_df.columns.get_level_values(0)
            yf_df = yf_df.reset_index()
            yf_df = normalize_columns(yf_df)
            yf_df['Date'] = pd.to_datetime(yf_df['Date']).dt.strftime('%Y-%m-%d')
            # Cache locally
            yf_df.to_csv(base_path, index=False)
            return yf_df
    except Exception as e:
        print(f"Error fetching {sym} from yfinance: {e}")
        
    # Fallback to AAPL if completely unfound
    fallback_path = os.path.join(Config.DATASET_FOLDER, "AAPL.csv")
    if os.path.exists(fallback_path):
        df = pd.read_csv(fallback_path)
        return normalize_columns(df)
        
    return None

def preprocess_dataset(df, missing_strategy='ffill', scaling_method='none'):
    """
    Performs data cleaning, missing value imputation, and feature scaling.
    """
    df_clean = df.copy()
    
    # 1. Ensure Date is sorted
    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'])
        df_clean = df_clean.sort_values('Date').reset_index(drop=True)
        
    # 2. Handle Missing Values
    numeric_cols = [c for c in df_clean.columns if np.issubdtype(df_clean[c].dtype, np.number)]
    
    initial_nulls = int(df_clean.isnull().sum().sum())
    
    if missing_strategy == 'drop':
        df_clean = df_clean.dropna().reset_index(drop=True)
    elif missing_strategy == 'ffill':
        df_clean[numeric_cols] = df_clean[numeric_cols].ffill().bfill()
    elif missing_strategy == 'mean':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    elif missing_strategy == 'median':
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
        
    post_nulls = int(df_clean.isnull().sum().sum())
    
    # 3. Optional Scaling
    scaled_df = df_clean.copy()
    if scaling_method in ['standard', 'minmax'] and numeric_cols:
        scaler = StandardScaler() if scaling_method == 'standard' else MinMaxScaler()
        scaled_df[numeric_cols] = scaler.fit_transform(scaled_df[numeric_cols])
        
    # Summary Statistics
    summary_stats = df_clean[numeric_cols].describe().round(2).to_dict()
    
    # Correlation Matrix
    corr_matrix = df_clean[numeric_cols].corr().round(3).to_dict()
    
    return {
        'cleaned_df': df_clean,
        'scaled_df': scaled_df,
        'rows_total': len(df_clean),
        'columns': list(df_clean.columns),
        'numeric_columns': numeric_cols,
        'nulls_handled': initial_nulls - post_nulls,
        'summary_stats': summary_stats,
        'correlation_matrix': corr_matrix
    }

def get_dataset_inspection(symbol_or_filename):
    """
    Generates preview, null counts, stats, and head/tail for the UI.
    """
    df = get_stock_data(symbol_or_filename)
    if df is None:
        return None
        
    pre = preprocess_dataset(df)
    
    preview_rows = df.head(10).copy()
    if 'Date' in preview_rows.columns:
        preview_rows['Date'] = preview_rows['Date'].astype(str)
        
    # Convert numeric values to standard floats for JSON
    preview_dict = preview_rows.to_dict(orient='records')
    
    null_counts = {col: int(df[col].isnull().sum()) for col in df.columns}
    dtypes = {col: str(df[col].dtype) for col in df.columns}
    
    return {
        'total_rows': len(df),
        'columns': list(df.columns),
        'preview': preview_dict,
        'null_counts': null_counts,
        'dtypes': dtypes,
        'summary_stats': pre['summary_stats'],
        'correlation': pre['correlation_matrix']
    }
