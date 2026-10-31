import os
import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from config import Config

def load_stock_df(symbol):
    """Load dataframe for a stock from local datasets."""
    csv_path = os.path.join(Config.DATASET_FOLDER, f"{symbol}.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df.sort_values('Date').reset_index(drop=True)
    return None

def calculate_stock_stats(symbol):
    """Compute financial summary statistics for a stock symbol."""
    df = load_stock_df(symbol)
    if df is None or len(df) < 30:
        return None
        
    prices = df['Close']
    returns = prices.pct_change().dropna()
    
    ann_return = float((prices.iloc[-1] / prices.iloc[0]) ** (252 / len(prices)) - 1)
    ann_volatility = float(returns.std() * np.sqrt(252))
    
    # Sharpe ratio (risk-free rate = 4.0%)
    rf = 0.04
    sharpe = float((ann_return - rf) / (ann_volatility + 1e-6))
    
    # Maximum Drawdown
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    max_dd = float(drawdown.min())
    
    # Risk Classification
    if ann_volatility > 0.35 or max_dd < -0.40:
        risk_class = 'High'
    elif ann_volatility < 0.22 and max_dd > -0.25:
        risk_class = 'Low'
    else:
        risk_class = 'Medium'
        
    latest_price = float(prices.iloc[-1])
    day_change = float(returns.iloc[-1] * 100)
    
    meta = Config.SUPPORTED_STOCKS.get(symbol, {'name': symbol, 'sector': 'Equities'})
    
    return {
        'symbol': symbol,
        'name': meta.get('name', symbol),
        'sector': meta.get('sector', 'Equities'),
        'latest_price': round(latest_price, 2),
        'day_change_pct': round(day_change, 2),
        'ann_return': round(ann_return * 100, 2),
        'ann_volatility': round(ann_volatility * 100, 2),
        'sharpe_ratio': round(sharpe, 2),
        'max_drawdown': round(max_dd * 100, 2),
        'risk_level': risk_class
    }

def get_market_overview():
    """Returns overview list of all supported stocks with stats."""
    stocks = []
    for sym in Config.SUPPORTED_STOCKS:
        stats = calculate_stock_stats(sym)
        if stats:
            stocks.append(stats)
    return stocks

def perform_clustering_and_pca(n_clusters=3):
    """
    Performs K-Means clustering and PCA 2D dimensionality reduction on available stocks.
    """
    data_list = []
    symbols = []
    
    for sym in Config.SUPPORTED_STOCKS:
        stats = calculate_stock_stats(sym)
        if stats:
            symbols.append(sym)
            data_list.append([
                stats['ann_return'],
                stats['ann_volatility'],
                stats['sharpe_ratio'],
                abs(stats['max_drawdown'])
            ])
            
    if len(symbols) < 3:
        return {'clusters': [], 'pca_points': []}
        
    X = np.array(data_list)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. K-Means
    k = min(n_clusters, len(symbols))
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # 2. PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    var_explained = [round(float(v) * 100, 1) for v in pca.explained_variance_ratio_]
    
    cluster_names = {
        0: 'Aggressive High-Growth',
        1: 'Consistent Compounders',
        2: 'Defensive & Value'
    }
    
    results = []
    for i, sym in enumerate(symbols):
        c_id = int(cluster_labels[i])
        results.append({
            'symbol': sym,
            'name': Config.SUPPORTED_STOCKS.get(sym, {}).get('name', sym),
            'sector': Config.SUPPORTED_STOCKS.get(sym, {}).get('sector', 'General'),
            'cluster_id': c_id,
            'cluster_label': cluster_names.get(c_id, f"Cluster {c_id+1}"),
            'ann_return': data_list[i][0],
            'ann_volatility': data_list[i][1],
            'sharpe_ratio': data_list[i][2],
            'pca_x': round(float(X_pca[i, 0]), 3),
            'pca_y': round(float(X_pca[i, 1]), 3)
        })
        
    return {
        'items': results,
        'var_explained': var_explained,
        'k': k
    }

def get_correlation_matrix():
    """Computes cross-asset return correlation matrix."""
    return_series = {}
    for sym in Config.SUPPORTED_STOCKS:
        df = load_stock_df(sym)
        if df is not None:
            return_series[sym] = df.set_index('Date')['Close'].pct_change()
            
    comb_df = pd.DataFrame(return_series).dropna()
    corr = comb_df.corr().round(3)
    
    labels = list(corr.columns)
    matrix = []
    for r in labels:
        row = [float(corr.loc[r, c]) for c in labels]
        matrix.append(row)
        
    return {
        'labels': labels,
        'matrix': matrix
    }

def recommend_portfolio(investment_amount, risk_tolerance='Medium', selected_stocks=None):
    """
    AI Portfolio Allocation Engine based on Markowitz Modern Portfolio Theory & Risk profiling.
    Distributes user capital with target allocations, expected returns, and Sharpe ratio.
    """
    if not selected_stocks:
        selected_stocks = list(Config.SUPPORTED_STOCKS.keys())
        
    # Gather price series
    prices_dict = {}
    for sym in selected_stocks:
        df = load_stock_df(sym)
        if df is not None:
            prices_dict[sym] = df.set_index('Date')['Close']
            
    df_prices = pd.DataFrame(prices_dict).dropna()
    if df_prices.empty:
        return None
        
    returns = df_prices.pct_change().dropna()
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    
    num_assets = len(selected_stocks)
    
    # Weight strategy based on risk tolerance
    # Low: Inverse-volatility weighting with cap (conservative)
    # Medium: Sharpe-ratio weighted (balanced growth)
    # High: Momentum / Return weighted (aggressive)
    
    vols = np.sqrt(np.diag(cov_matrix))
    rf = 0.04
    
    if risk_tolerance.lower() == 'low':
        # Inverse volatility
        inv_vol = 1.0 / (vols + 1e-6)
        raw_weights = inv_vol / np.sum(inv_vol)
    elif risk_tolerance.lower() == 'high':
        # Return / upside focused
        pos_returns = np.maximum(mean_returns.values, 0.05)
        raw_weights = (pos_returns ** 1.5) / np.sum(pos_returns ** 1.5)
    else:  # Medium
        # Sharpe ratio weighted
        sharpes = np.maximum((mean_returns.values - rf) / (vols + 1e-6), 0.1)
        raw_weights = sharpes / np.sum(sharpes)
        
    # Normalize weights to sum to 100%
    weights = raw_weights / np.sum(raw_weights)
    
    portfolio_return = float(np.sum(mean_returns.values * weights))
    portfolio_volatility = float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights))))
    portfolio_sharpe = float((portfolio_return - rf) / (portfolio_volatility + 1e-6))
    
    allocations = []
    for i, sym in enumerate(selected_stocks):
        w = float(weights[i])
        allocated_amount = round(investment_amount * w, 2)
        stock_stats = calculate_stock_stats(sym) or {}
        
        allocations.append({
            'symbol': sym,
            'name': Config.SUPPORTED_STOCKS.get(sym, {}).get('name', sym),
            'sector': Config.SUPPORTED_STOCKS.get(sym, {}).get('sector', 'General'),
            'weight_pct': round(w * 100, 1),
            'amount': allocated_amount,
            'shares_approx': int(allocated_amount / stock_stats.get('latest_price', 150)) if stock_stats.get('latest_price') else 0,
            'risk_level': stock_stats.get('risk_level', 'Medium')
        })
        
    # Sort by largest allocation
    allocations = sorted(allocations, key=lambda x: -x['weight_pct'])
    
    return {
        'investment_amount': float(investment_amount),
        'risk_tolerance': risk_tolerance.capitalize(),
        'expected_annual_return': round(portfolio_return * 100, 2),
        'expected_volatility': round(portfolio_volatility * 100, 2),
        'sharpe_ratio': round(portfolio_sharpe, 2),
        'allocations': allocations
    }
