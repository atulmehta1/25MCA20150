import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.svm import SVR, SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

# Supported ML models dictionary
REGRESSION_MODELS = {
    'linear_regression': {'name': 'Linear Regression', 'cls': LinearRegression},
    'polynomial_regression': {'name': 'Polynomial Regression (Deg 2)', 'cls': None},
    'decision_tree': {'name': 'Decision Tree Regressor', 'cls': DecisionTreeRegressor, 'kwargs': {'max_depth': 6, 'random_state': 42}},
    'random_forest': {'name': 'Random Forest Regressor', 'cls': RandomForestRegressor, 'kwargs': {'n_estimators': 100, 'max_depth': 8, 'random_state': 42}},
    'svm': {'name': 'Support Vector Regressor (SVR)', 'cls': SVR, 'kwargs': {'C': 100, 'gamma': 'scale'}},
    'knn': {'name': 'K-Nearest Neighbors (KNN)', 'cls': KNeighborsRegressor, 'kwargs': {'n_neighbors': 5}},
    'mlp': {'name': 'Multi-Layer Perceptron (Neural Net)', 'cls': MLPRegressor, 'kwargs': {'hidden_layer_sizes': (64, 32), 'max_iter': 500, 'random_state': 42}}
}

CLASSIFICATION_MODELS = {
    'logistic_regression': {'name': 'Logistic Regression', 'cls': LogisticRegression, 'kwargs': {'max_iter': 500, 'random_state': 42}},
    'decision_tree': {'name': 'Decision Tree Classifier', 'cls': DecisionTreeClassifier, 'kwargs': {'max_depth': 5, 'random_state': 42}},
    'random_forest': {'name': 'Random Forest Classifier', 'cls': RandomForestClassifier, 'kwargs': {'n_estimators': 100, 'max_depth': 6, 'random_state': 42}},
    'knn': {'name': 'K-Nearest Neighbors (KNN)', 'cls': KNeighborsClassifier, 'kwargs': {'n_neighbors': 5}},
    'svm': {'name': 'Support Vector Machine (SVC)', 'cls': SVC, 'kwargs': {'probability': True, 'random_state': 42}},
    'naive_bayes': {'name': 'Gaussian Naive Bayes', 'cls': GaussianNB, 'kwargs': {}},
    'mlp': {'name': 'Multi-Layer Perceptron Classifier', 'cls': MLPClassifier, 'kwargs': {'hidden_layer_sizes': (64, 32), 'max_iter': 500, 'random_state': 42}}
}

def prepare_features(df, lag_days=5):
    """
    Generate lag features, rolling technical metrics, and targets.
    Input df should have ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'].
    """
    df = df.copy()
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
    
    # Target 1: Next Day Close Price (Regression)
    df['Target_Close'] = df['Close'].shift(-1)
    
    # Target 2: Price Direction (Classification: 1 for UP, 0 for DOWN/FLAT)
    df['Target_Direction'] = (df['Target_Close'] > df['Close']).astype(int)
    
    # Technical & Lag features
    for lag in range(1, lag_days + 1):
        df[f'Close_Lag_{lag}'] = df['Close'].shift(lag)
        df[f'Volume_Lag_{lag}'] = df['Volume'].shift(lag)
        df[f'Return_Lag_{lag}'] = df['Close'].pct_change(lag)

    # Rolling averages & volatility
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_15'] = df['Close'].rolling(window=15).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['Volatility_10'] = df['Close'].pct_change().rolling(window=10).std()
    df['High_Low_Pct'] = (df['High'] - df['Low']) / df['Low']
    df['Close_Open_Pct'] = (df['Close'] - df['Open']) / df['Open']
    
    # Drop rows with NaN from lags and targets
    df = df.dropna().reset_index(drop=True)
    return df

def get_feature_columns(df):
    excluded = ['Date', 'Target_Close', 'Target_Direction', 'Adj Close']
    return [col for col in df.columns if col not in excluded and np.issubdtype(df[col].dtype, np.number)]

def train_regression_model(df, model_key='random_forest', test_size=0.2, scaler_type='standard', cv_folds=5):
    """
    Train a regression model for stock price prediction.
    Returns metrics, predictions array, cv scores, feature importances.
    """
    df_prep = prepare_features(df)
    feature_cols = get_feature_columns(df_prep)
    
    X = df_prep[feature_cols].values
    y = df_prep['Target_Close'].values
    dates = df_prep['Date'].dt.strftime('%Y-%m-%d').values
    
    # Split train/test (chronological order preserve or shuffle=False for time-series)
    split_idx = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    dates_train, dates_test = dates[:split_idx], dates[split_idx:]
    
    # Scaling
    scaler = StandardScaler() if scaler_type == 'standard' else MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize Model
    if model_key == 'polynomial_regression':
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_train_poly = poly.fit_transform(X_train_scaled)
        X_test_poly = poly.transform(X_test_scaled)
        model = LinearRegression()
        model.fit(X_train_poly, y_train)
        y_pred = model.predict(X_test_poly)
        y_train_pred = model.predict(X_train_poly)
    else:
        model_info = REGRESSION_MODELS.get(model_key, REGRESSION_MODELS['random_forest'])
        cls = model_info['cls']
        kwargs = model_info.get('kwargs', {})
        model = cls(**kwargs)
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_train_pred = model.predict(X_train_scaled)
        
    # Evaluation Metrics
    mae = float(mean_absolute_error(y_test, y_pred))
    mse = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_test, y_pred))
    mape = float(np.mean(np.abs((y_test - y_pred) / y_test)) * 100)
    
    # Cross Validation
    cv = KFold(n_splits=cv_folds, shuffle=False)
    if model_key == 'polynomial_regression':
        cv_pipe = Pipeline([('poly', PolynomialFeatures(degree=2, include_bias=False)), ('model', LinearRegression())])
        cv_scores = cross_val_score(cv_pipe, scaler.transform(X), y, cv=cv, scoring='r2')
    else:
        cv_scores = cross_val_score(model, scaler.transform(X), y, cv=cv, scoring='r2')
    
    # Feature Importance
    importances = {}
    if hasattr(model, 'feature_importances_'):
        for col, imp in zip(feature_cols, model.feature_importances_):
            importances[col] = round(float(imp), 4)
    elif hasattr(model, 'coef_') and model_key != 'polynomial_regression':
        for col, coef in zip(feature_cols, model.coef_):
            importances[col] = round(float(abs(coef)), 4)
            
    # Sort top features
    importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True)[:8])

    # Future Forecasting (Recursive multi-step forecast for next 7 days)
    future_dates = pd.bdate_range(start=pd.to_datetime(dates[-1]) + pd.Timedelta(days=1), periods=7).strftime('%Y-%m-%d').tolist()
    last_row_scaled = X_test_scaled[-1:].copy()
    future_forecasts = []
    
    current_feat = last_row_scaled
    curr_price = float(y_pred[-1])
    for _ in range(7):
        if model_key == 'polynomial_regression':
            next_p = float(model.predict(poly.transform(current_feat))[0])
        else:
            next_p = float(model.predict(current_feat)[0])
        future_forecasts.append(round(next_p, 2))
        # slight dynamic shift for recursive steps
        current_feat = current_feat * (1 + (next_p - curr_price)/curr_price * 0.1)
        curr_price = next_p

    return {
        'model_name': REGRESSION_MODELS.get(model_key, {}).get('name', model_key),
        'metrics': {
            'mae': round(mae, 4),
            'mse': round(mse, 4),
            'rmse': round(rmse, 4),
            'r2': round(r2, 4),
            'mape': round(mape, 2)
        },
        'cv_scores': [round(float(s), 4) for s in cv_scores],
        'cv_mean': round(float(np.mean(cv_scores)), 4),
        'feature_importance': importances,
        'dates_test': list(dates_test),
        'actual': [round(float(a), 2) for a in y_test],
        'predicted': [round(float(p), 2) for p in y_pred],
        'future_dates': future_dates,
        'future_predictions': future_forecasts,
        'last_actual_price': round(float(y_test[-1]), 2),
        'next_day_prediction': round(float(future_forecasts[0]), 2)
    }

def train_classification_model(df, model_key='random_forest', test_size=0.2, scaler_type='standard'):
    """
    Train classification model to predict price movement (Up vs Down).
    Returns accuracy, precision, recall, f1, and confusion matrix.
    """
    df_prep = prepare_features(df)
    feature_cols = get_feature_columns(df_prep)
    
    X = df_prep[feature_cols].values
    y = df_prep['Target_Direction'].values
    dates = df_prep['Date'].dt.strftime('%Y-%m-%d').values
    
    split_idx = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    dates_test = dates[split_idx:]
    
    scaler = StandardScaler() if scaler_type == 'standard' else MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model_info = CLASSIFICATION_MODELS.get(model_key, CLASSIFICATION_MODELS['random_forest'])
    cls = model_info['cls']
    kwargs = model_info.get('kwargs', {})
    model = cls(**kwargs)
    
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = [int(val) for val in cm.ravel()]
    
    probs = None
    if hasattr(model, 'predict_proba'):
        probs = [round(float(p[1]), 3) for p in model.predict_proba(X_test_scaled)]
        
    next_day_prob = probs[-1] if probs else (1.0 if y_pred[-1] == 1 else 0.0)
    recommendation = "BUY" if next_day_prob > 0.60 else ("SELL" if next_day_prob < 0.40 else "HOLD")
    
    return {
        'model_name': model_info['name'],
        'task': 'classification',
        'metrics': {
            'accuracy': round(accuracy * 100, 2),
            'precision': round(precision * 100, 2),
            'recall': round(recall * 100, 2),
            'f1_score': round(f1 * 100, 2)
        },
        'confusion_matrix': {
            'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn
        },
        'dates_test': list(dates_test),
        'actual': [int(a) for a in y_test],
        'predicted': [int(p) for p in y_pred],
        'probabilities': probs,
        'next_day_direction': 'UP' if y_pred[-1] == 1 else 'DOWN',
        'next_day_confidence': round(next_day_prob * 100 if y_pred[-1] == 1 else (1 - next_day_prob) * 100, 1),
        'signal': recommendation
    }

def compare_all_models(df):
    """
    Run and compare all regression and classification models side by side.
    """
    results_reg = []
    for key in REGRESSION_MODELS:
        try:
            res = train_regression_model(df, model_key=key, test_size=0.2)
            results_reg.append({
                'key': key,
                'name': res['model_name'],
                'rmse': res['metrics']['rmse'],
                'mae': res['metrics']['mae'],
                'r2': res['metrics']['r2'],
                'mape': res['metrics']['mape'],
                'cv_mean': res['cv_mean']
            })
        except Exception as e:
            continue

    # Sort best regression model by lowest RMSE and highest R2
    results_reg = sorted(results_reg, key=lambda x: (-x['r2'], x['rmse']))

    results_clf = []
    for key in CLASSIFICATION_MODELS:
        try:
            res = train_classification_model(df, model_key=key, test_size=0.2)
            results_clf.append({
                'key': key,
                'name': res['model_name'],
                'accuracy': res['metrics']['accuracy'],
                'precision': res['metrics']['precision'],
                'recall': res['metrics']['recall'],
                'f1': res['metrics']['f1_score'],
                'signal': res['signal']
            })
        except Exception as e:
            continue

    # Sort best classification model by F1 / Accuracy
    results_clf = sorted(results_clf, key=lambda x: -x['f1'])

    return {
        'regression_comparison': results_reg,
        'classification_comparison': results_clf
    }
