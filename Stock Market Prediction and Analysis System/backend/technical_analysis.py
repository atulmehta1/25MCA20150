import numpy as np
import pandas as pd

def compute_technical_indicators(df):
    """
    Computes SMA, EMA, RSI, MACD, Bollinger Bands, and Volatility.
    Input df should have ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'].
    """
    df = df.copy()
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        
    close = df['Close']
    
    # 1. Simple Moving Averages
    df['SMA_20'] = close.rolling(window=20).mean()
    df['SMA_50'] = close.rolling(window=50).mean()
    df['SMA_200'] = close.rolling(window=200).mean() if len(df) >= 200 else close.rolling(window=len(df)//2).mean()
    
    # 2. Exponential Moving Averages
    df['EMA_12'] = close.ewm(span=12, adjust=False).mean()
    df['EMA_26'] = close.ewm(span=26, adjust=False).mean()
    
    # 3. MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    # 4. RSI (14-day)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 5. Bollinger Bands (20-day, 2 std dev)
    rolling_std = close.rolling(window=20).std()
    df['BB_Middle'] = df['SMA_20']
    df['BB_Upper'] = df['BB_Middle'] + (rolling_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (rolling_std * 2)
    
    # 6. Daily Returns & Annualized Volatility
    df['Daily_Return'] = close.pct_change()
    df['Rolling_Volatility'] = df['Daily_Return'].rolling(window=30).std() * np.sqrt(252) * 100
    
    return df

def generate_signals_and_recommendation(df):
    """
    Evaluates latest technical indicators and generates BUY / HOLD / SELL recommendations.
    """
    df_calc = compute_technical_indicators(df)
    latest = df_calc.iloc[-1]
    prev = df_calc.iloc[-2] if len(df_calc) > 1 else latest
    
    signals = []
    bullish_points = 0
    bearish_points = 0
    total_checks = 0
    
    # 1. RSI Indicator
    rsi_val = float(latest['RSI']) if pd.notnull(latest['RSI']) else 50.0
    if rsi_val < 30:
        bullish_points += 2
        signals.append({'indicator': 'RSI (14)', 'value': round(rsi_val, 1), 'status': 'Oversold (Bullish Reversal Potential)', 'action': 'BUY'})
    elif rsi_val > 70:
        bearish_points += 2
        signals.append({'indicator': 'RSI (14)', 'value': round(rsi_val, 1), 'status': 'Overbought (Correction Risk)', 'action': 'SELL'})
    else:
        signals.append({'indicator': 'RSI (14)', 'value': round(rsi_val, 1), 'status': 'Neutral Range', 'action': 'HOLD'})
    total_checks += 2

    # 2. MACD Crossover
    macd_val = float(latest['MACD']) if pd.notnull(latest['MACD']) else 0.0
    macd_sig = float(latest['MACD_Signal']) if pd.notnull(latest['MACD_Signal']) else 0.0
    if macd_val > macd_sig:
        bullish_points += 2
        signals.append({'indicator': 'MACD (12,26,9)', 'value': f"{macd_val:.2f} > {macd_sig:.2f}", 'status': 'Bullish Crossover', 'action': 'BUY'})
    else:
        bearish_points += 2
        signals.append({'indicator': 'MACD (12,26,9)', 'value': f"{macd_val:.2f} < {macd_sig:.2f}", 'status': 'Bearish Crossover', 'action': 'SELL'})
    total_checks += 2

    # 3. Moving Average Trend (SMA 20 vs SMA 50)
    sma20 = float(latest['SMA_20']) if pd.notnull(latest['SMA_20']) else float(latest['Close'])
    sma50 = float(latest['SMA_50']) if pd.notnull(latest['SMA_50']) else float(latest['Close'])
    curr_close = float(latest['Close'])
    
    if curr_close > sma20 and sma20 > sma50:
        bullish_points += 2
        signals.append({'indicator': 'SMA Trend', 'value': f"${curr_close:.2f} > SMA20 (${sma20:.2f})", 'status': 'Strong Bullish Trend', 'action': 'BUY'})
    elif curr_close < sma20 and sma20 < sma50:
        bearish_points += 2
        signals.append({'indicator': 'SMA Trend', 'value': f"${curr_close:.2f} < SMA20 (${sma20:.2f})", 'status': 'Strong Bearish Trend', 'action': 'SELL'})
    else:
        signals.append({'indicator': 'SMA Trend', 'value': f"${curr_close:.2f}", 'status': 'Consolidation / Mixed', 'action': 'HOLD'})
    total_checks += 2

    # 4. Bollinger Bands Positioning
    bb_upper = float(latest['BB_Upper']) if pd.notnull(latest['BB_Upper']) else curr_close * 1.05
    bb_lower = float(latest['BB_Lower']) if pd.notnull(latest['BB_Lower']) else curr_close * 0.95
    if curr_close <= bb_lower * 1.01:
        bullish_points += 1
        signals.append({'indicator': 'Bollinger Bands', 'value': f"Near Lower Band (${bb_lower:.2f})", 'status': 'Oversold / Bounce Zone', 'action': 'BUY'})
    elif curr_close >= bb_upper * 0.99:
        bearish_points += 1
        signals.append({'indicator': 'Bollinger Bands', 'value': f"Near Upper Band (${bb_upper:.2f})", 'status': 'Resistance Zone', 'action': 'SELL'})
    else:
        signals.append({'indicator': 'Bollinger Bands', 'value': f"Within Bands (${bb_lower:.2f} - ${bb_upper:.2f})", 'status': 'Normal Band Range', 'action': 'HOLD'})
    total_checks += 1

    # Final Decision
    net_score = bullish_points - bearish_points
    if net_score >= 3:
        overall_recommendation = 'STRONG BUY'
        confidence = min(95, 65 + net_score * 7)
    elif net_score >= 1:
        overall_recommendation = 'BUY'
        confidence = min(85, 55 + net_score * 8)
    elif net_score <= -3:
        overall_recommendation = 'STRONG SELL'
        confidence = min(95, 65 + abs(net_score) * 7)
    elif net_score <= -1:
        overall_recommendation = 'SELL'
        confidence = min(85, 55 + abs(net_score) * 8)
    else:
        overall_recommendation = 'HOLD'
        confidence = 60

    ann_volatility = float(latest['Rolling_Volatility']) if pd.notnull(latest['Rolling_Volatility']) else 22.5
    risk_level = 'High' if ann_volatility > 35 else ('Low' if ann_volatility < 20 else 'Medium')

    return {
        'recommendation': overall_recommendation,
        'confidence': confidence,
        'risk_level': risk_level,
        'annualized_volatility': round(ann_volatility, 2),
        'signals': signals,
        'latest_price': round(curr_close, 2),
        'rsi': round(rsi_val, 2),
        'macd': round(macd_val, 2),
        'macd_signal': round(macd_sig, 2),
        'sma_20': round(sma20, 2),
        'sma_50': round(sma50, 2),
        'bb_upper': round(bb_upper, 2),
        'bb_lower': round(bb_lower, 2)
    }

def get_chart_series(df, limit=120):
    """
    Format data for frontend charting (Candlestick + Technical Overlays).
    Limits to last `limit` points for swift client rendering.
    """
    df_calc = compute_technical_indicators(df)
    subset = df_calc.tail(limit).copy()
    
    dates = subset['Date'].dt.strftime('%Y-%m-%d').tolist()
    candlesticks = []
    for _, row in subset.iterrows():
        candlesticks.append({
            'x': row['Date'].strftime('%Y-%m-%d'),
            'y': [round(float(row['Open']), 2), round(float(row['High']), 2), round(float(row['Low']), 2), round(float(row['Close']), 2)]
        })
        
    return {
        'dates': dates,
        'candlesticks': candlesticks,
        'close': [round(float(x), 2) for x in subset['Close']],
        'volume': [int(x) for x in subset['Volume']],
        'sma_20': [round(float(x), 2) if pd.notnull(x) else None for x in subset['SMA_20']],
        'sma_50': [round(float(x), 2) if pd.notnull(x) else None for x in subset['SMA_50']],
        'ema_12': [round(float(x), 2) if pd.notnull(x) else None for x in subset['EMA_12']],
        'bb_upper': [round(float(x), 2) if pd.notnull(x) else None for x in subset['BB_Upper']],
        'bb_middle': [round(float(x), 2) if pd.notnull(x) else None for x in subset['BB_Middle']],
        'bb_lower': [round(float(x), 2) if pd.notnull(x) else None for x in subset['BB_Lower']],
        'rsi': [round(float(x), 2) if pd.notnull(x) else None for x in subset['RSI']],
        'macd': [round(float(x), 2) if pd.notnull(x) else None for x in subset['MACD']],
        'macd_signal': [round(float(x), 2) if pd.notnull(x) else None for x in subset['MACD_Signal']],
        'macd_hist': [round(float(x), 2) if pd.notnull(x) else None for x in subset['MACD_Hist']]
    }
