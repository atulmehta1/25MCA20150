# 📈 Stock Market Prediction & AI Investment Intelligence Platform

A modern, production-grade, full-stack web application for stock market forecasting, quantitative technical analysis, and AI-powered investment intelligence built with **Python (Flask), HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, and SQLite/MySQL**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Engine-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🌟 Key Features

### 1. 🤖 9 Machine Learning Algorithms (Regression & Classification)
- **Linear Regression**: Baseline multivariate price prediction.
- **Polynomial Regression (Degree 2)**: Non-linear price curve fitting.
- **Logistic Regression**: Price movement direction (UP / DOWN) with class probabilities.
- **Decision Tree**: Regressor & Classifier with depth tuning.
- **Random Forest**: Ensemble learning for robust non-linear trend capture.
- **Support Vector Machine (SVR & SVC)**: High-dimensional hyperplane modeling.
- **K-Nearest Neighbors (KNN)**: Non-parametric distance-weighted modeling.
- **Gaussian Naive Bayes**: Probabilistic movement and risk prediction.
- **Multi-Layer Perceptron (MLP)**: Deep neural network for price trajectory prediction.

### 2. 📊 Machine Learning Features & Metrics
- **Dynamic Train/Test Split** (70/30, 80/20, 85/15)
- **K-Fold Cross Validation** (5-Fold CV Mean R² score)
- **Standardization & Normalization** (`StandardScaler` and `MinMaxScaler`)
- **Regression Evaluation Metrics**: MAE, MSE, RMSE, R² Score, MAPE
- **Classification Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- **Feature Importance**: Visualized top predictive signal weights (Lags, Moving Averages, Volatility)
- **Recursive Multi-Day Forecast**: Forward projection for the next 7 business days

### 3. 📉 Interactive Technical Charts & Quantitative Matrix
- Candlestick and Line price chart toggle
- Overlays: **SMA 20, SMA 50, EMA 12, Bollinger Bands** (Upper, Middle, Lower)
- Sub-charts: **Volume bars, RSI 14** (Overbought 70 / Oversold 30), **MACD (12, 26, 9)** with Signal Line & Histogram
- **Automated Buy / Hold / Sell Recommendation Matrix**: Multi-model consensus with confidence scoring.

### 4. 🧠 AI Investment Intelligence & Portfolio Optimizer
- **Markowitz Modern Portfolio Theory (MPT)**: Mean-Variance Optimization
- Tailored to user's capital amount ($ or ₹) and **Risk Tolerance** (Conservative, Moderate, Aggressive)
- Target allocation breakdown: Percentage weights, dollar amount, and estimated shares
- Portfolio Expected Annual Compound Return, Volatility, and Sharpe Ratio

### 5. 🔮 Unsupervised Clustering & PCA Dimensionality Reduction
- **K-Means Clustering**: Groups assets into High-Growth, Balanced, and Defensive cohorts
- **PCA 2D Projection**: Principal Component coordinate scatter plot showing explained variance
- **Cross-Asset Return Correlation Heatmap**: Matrix for diversification analysis

### 6. 📰 Financial News NLP Sentiment Engine
- TF-IDF Vectorization with N-Grams
- Supervised Classification via Logistic Regression and Multinomial Naive Bayes
- Custom headline analyzer with Bullish / Bearish / Neutral gauge and keyword feature weights
- Live stream of recent financial headlines with automated sentiment scoring

### 7. 📁 Dataset Preprocessing & CSV Studio
- Inspect pre-bundled datasets (**AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA**)
- Upload custom stock CSV datasets with automatic OHLCV column detection
- Missing value imputation (Forward Fill, Drop, Mean, Median)
- Feature scaling and Pandas descriptive summary statistics table

### 8. 🛡️ User Authentication & Admin Portal
- Secure User Registration, Login, Logout with hashed passwords (`werkzeug.security`)
- Role-based Access Control (`user` and `admin`)
- **Admin Portal**: User management, dataset repository, prediction audit logs, and batch model retraining pipeline
- Pre-seeded accounts:
  - **Admin**: `admin` / `admin123`
  - **Demo User**: `demo` / `demo123`

### 9. 📄 Export & Reporting
- **Executive PDF Report**: Professional PDF report generated with ReportLab (metrics, signals, forecast table, disclaimers).
- **CSV Data Export**: Download raw forecast and metrics in CSV format.

---

## 🗂️ Project Directory Structure

```text
Stock Market Prediction and Analysis System/
├── app.py                     # Flask application factory & database seeding
├── config.py                  # App configuration & stock parameters
├── database.py                # SQLAlchemy models (User, Predictions, Portfolios, Datasets)
├── requirements.txt           # Project Python dependencies
├── .gitignore                 # GitHub-optimized exclusion rules
├── README.md                  # Comprehensive documentation
├── backend/
│   ├── auth.py                # Authentication blueprint (Login, Register, Profile)
│   ├── routes.py              # Main routes (Dashboard, Prediction, Portfolio, Reports)
│   ├── admin.py               # Admin portal (User & dataset management, retraining)
│   ├── ml_engine.py           # 9 Machine Learning models, CV, and forecasting
│   ├── technical_analysis.py  # SMA, EMA, RSI, MACD, Bollinger Bands, Buy/Sell
│   ├── portfolio_ai.py        # Markowitz MPT, K-Means clustering, PCA 2D
│   ├── nlp_sentiment.py       # TF-IDF + Logistic Regression/Naive Bayes NLP
│   ├── data_loader.py         # CSV handler, preprocessing, yfinance fetcher
│   └── report_generator.py    # ReportLab PDF & CSV export engine
├── datasets/
│   ├── AAPL.csv               # Historical daily data for Apple Inc.
│   ├── MSFT.csv               # Historical daily data for Microsoft
│   ├── GOOGL.csv              # Historical daily data for Google
│   ├── TSLA.csv               # Historical daily data for Tesla
│   ├── AMZN.csv               # Historical daily data for Amazon
│   ├── NVDA.csv               # Historical daily data for NVIDIA
│   └── uploads/               # User-uploaded custom CSVs
├── static/
│   ├── css/
│   │   └── style.css          # Glassmorphism design system & Dark/Light mode tokens
│   └── js/
│       └── main.js            # Theme switcher, search routing, mobile drawer, toasts
└── templates/
    ├── base.html              # Base layout with sidebar, search, and CDN scripts
    ├── dashboard.html         # Main overview dashboard
    ├── analysis.html          # Interactive candlestick & technical chart suite
    ├── prediction.html        # ML forecasting studio with 9 models & metrics
    ├── model_arena.html       # Tournament leaderboard comparing all models
    ├── portfolio.html         # AI investment portfolio optimizer
    ├── clustering_pca.html    # K-Means clustering & PCA 2D projection
    ├── sentiment.html         # Financial news NLP sentiment engine
    ├── datasets.html          # CSV inspector & preprocessing studio
    ├── admin.html             # Admin portal (users, datasets, audit logs)
    ├── profile.html           # User profile & saved prediction history
    └── auth/
        ├── login.html         # User sign-in
        └── register.html      # Account registration
```

---

## 🚀 Quick Start Guide

### 1. Clone or Download Repository
```bash
git clone https://github.com/your-username/stock-market-prediction-ai.git
cd "Stock Market Prediction and Analysis System"
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows (Command Prompt / PowerShell):
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
Open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🔑 Default Credentials

| Role | Username | Password | Access Level |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full access (Admin Portal, User Management, Datasets, Retraining) |
| **Demo User** | `demo` | `demo123` | Regular User access (Forecasting, Portfolios, Profile) |

*(You can also register a new account anytime via the Sign In / Register pages!)*

---

## 📦 Uploading to GitHub

This repository is optimized for GitHub:
1. All large temporary caches, virtual environments, and database files are excluded in `.gitignore`.
2. Compact pre-bundled datasets ensure repository size remains under **1 MB**!
3. Fast CDNs are utilized for frontend dependencies (Bootstrap, FontAwesome, ApexCharts, Chart.js).

To push to your GitHub account:
```bash
git init
git add .
git commit -m "Initial commit: Stock Market Prediction and AI Investment Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

---

## 📄 License
This project is open-source under the **MIT License**.
