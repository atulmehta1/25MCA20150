import json
from flask import (
    Blueprint, render_template, request, jsonify, send_file, flash, redirect, url_for, session, g
)
from database import db, PredictionHistory, PortfolioPlan, DatasetMeta, AuditLog
from backend.auth import login_required
from backend.data_loader import (
    get_stock_data, get_dataset_inspection, preprocess_dataset, sanitize_symbol
)
from backend.ml_engine import (
    train_regression_model, train_classification_model, compare_all_models,
    REGRESSION_MODELS, CLASSIFICATION_MODELS
)
from backend.technical_analysis import (
    generate_signals_and_recommendation, get_chart_series
)
from backend.portfolio_ai import (
    get_market_overview, perform_clustering_and_pca, get_correlation_matrix,
    recommend_portfolio, calculate_stock_stats
)
from backend.nlp_sentiment import nlp_engine
from backend.report_generator import generate_pdf_report, generate_csv_report
from config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main_bp.route('/dashboard')
def dashboard():
    market_stocks = get_market_overview()
    sample_headlines = nlp_engine.get_sample_sentiment()[:4]
    return render_template(
        'dashboard.html',
        stocks=market_stocks,
        supported_stocks=Config.SUPPORTED_STOCKS,
        headlines=sample_headlines
    )

@main_bp.route('/analysis')
def analysis():
    symbol = request.args.get('symbol', 'AAPL').upper()
    if symbol not in Config.SUPPORTED_STOCKS:
        # Check if local dataset exists or fallback
        if not get_stock_data(symbol) is not None:
            symbol = 'AAPL'
            
    stats = calculate_stock_stats(symbol) or {}
    return render_template(
        'analysis.html',
        symbol=symbol,
        stats=stats,
        supported_stocks=Config.SUPPORTED_STOCKS
    )

@main_bp.route('/prediction')
def prediction():
    symbol = request.args.get('symbol', 'AAPL').upper()
    return render_template(
        'prediction.html',
        symbol=symbol,
        supported_stocks=Config.SUPPORTED_STOCKS,
        regression_models=REGRESSION_MODELS,
        classification_models=CLASSIFICATION_MODELS
    )

@main_bp.route('/model-arena')
def model_arena():
    symbol = request.args.get('symbol', 'AAPL').upper()
    return render_template(
        'model_arena.html',
        symbol=symbol,
        supported_stocks=Config.SUPPORTED_STOCKS
    )

@main_bp.route('/portfolio')
def portfolio():
    return render_template(
        'portfolio.html',
        supported_stocks=Config.SUPPORTED_STOCKS
    )

@main_bp.route('/clustering-pca')
def clustering_pca():
    return render_template(
        'clustering_pca.html',
        supported_stocks=Config.SUPPORTED_STOCKS
    )

@main_bp.route('/sentiment')
def sentiment():
    sample_news = nlp_engine.get_sample_sentiment()
    return render_template(
        'sentiment.html',
        news=sample_news,
        supported_stocks=Config.SUPPORTED_STOCKS
    )

@main_bp.route('/datasets', methods=['GET', 'POST'])
def datasets():
    system_datasets = DatasetMeta.query.filter_by(is_system=True).all()
    user_datasets = DatasetMeta.query.filter_by(is_system=False).all()
    selected_ds = request.args.get('file', 'AAPL.csv')
    inspection = get_dataset_inspection(selected_ds)
    
    return render_template(
        'datasets.html',
        system_datasets=system_datasets,
        user_datasets=user_datasets,
        selected_file=selected_ds,
        inspection=inspection,
        supported_stocks=Config.SUPPORTED_STOCKS
    )

# ---------------- API ENDPOINTS ----------------

@main_bp.route('/api/chart-data/<symbol>')
def api_chart_data(symbol):
    symbol = sanitize_symbol(symbol)
    df = get_stock_data(symbol)
    if df is None:
        return jsonify({'error': 'Stock data not found'}), 404
        
    series = get_chart_series(df, limit=140)
    return jsonify(series)

@main_bp.route('/api/technical-signals/<symbol>')
def api_technical_signals(symbol):
    symbol = sanitize_symbol(symbol)
    df = get_stock_data(symbol)
    if df is None:
        return jsonify({'error': 'Stock data not found'}), 404
        
    signals = generate_signals_and_recommendation(df)
    return jsonify(signals)

@main_bp.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json() or {}
    symbol = sanitize_symbol(data.get('symbol', 'AAPL'))
    model_key = data.get('model_key', 'random_forest')
    task_type = data.get('task_type', 'regression')
    test_size = float(data.get('test_size', 0.2))
    scaler_type = data.get('scaler_type', 'standard')
    
    df = get_stock_data(symbol)
    if df is None or len(df) < 40:
        return jsonify({'error': f"Insufficient historical data for {symbol}"}), 400
        
    if task_type == 'classification':
        result = train_classification_model(
            df, model_key=model_key, test_size=test_size, scaler_type=scaler_type
        )
    else:
        result = train_regression_model(
            df, model_key=model_key, test_size=test_size, scaler_type=scaler_type
        )
        
    # Save to history if user is logged in
    user_id = session.get('user_id')
    if user_id:
        target_val = str(result.get('next_day_prediction', '')) if task_type == 'regression' else result.get('next_day_direction', '')
        pred_entry = PredictionHistory(
            user_id=user_id,
            symbol=symbol,
            model_name=result.get('model_name', model_key),
            task_type=task_type,
            metrics=json.dumps(result.get('metrics', {})),
            target_date=result.get('future_dates', [''])[0] if task_type == 'regression' else result.get('dates_test', [''])[-1],
            predicted_value=target_val,
            signal=result.get('signal', 'HOLD')
        )
        db.session.add(pred_entry)
        db.session.commit()
        
    return jsonify(result)

@main_bp.route('/api/compare-models/<symbol>')
def api_compare_models(symbol):
    symbol = sanitize_symbol(symbol)
    df = get_stock_data(symbol)
    if df is None:
        return jsonify({'error': 'Stock data not found'}), 404
        
    comparison = compare_all_models(df)
    return jsonify(comparison)

@main_bp.route('/api/portfolio/recommend', methods=['POST'])
def api_portfolio_recommend():
    data = request.get_json() or {}
    amount = float(data.get('amount', 10000.0))
    risk = data.get('risk_tolerance', 'Medium')
    stocks = data.get('stocks', list(Config.SUPPORTED_STOCKS.keys()))
    
    plan = recommend_portfolio(amount, risk_tolerance=risk, selected_stocks=stocks)
    if not plan:
        return jsonify({'error': 'Failed to compute portfolio allocation'}), 400
        
    # Save plan to user account if logged in
    user_id = session.get('user_id')
    if user_id:
        plan_entry = PortfolioPlan(
            user_id=user_id,
            investment_amount=amount,
            risk_tolerance=risk,
            allocations=json.dumps(plan['allocations']),
            expected_return=plan['expected_annual_return'],
            volatility=plan['expected_volatility'],
            sharpe_ratio=plan['sharpe_ratio']
        )
        db.session.add(plan_entry)
        db.session.commit()
        
    return jsonify(plan)

@main_bp.route('/api/clustering')
def api_clustering():
    k = int(request.args.get('k', 3))
    cluster_res = perform_clustering_and_pca(n_clusters=k)
    corr_res = get_correlation_matrix()
    return jsonify({
        'clustering': cluster_res,
        'correlation': corr_res
    })

@main_bp.route('/api/sentiment/analyze', methods=['POST'])
def api_sentiment_analyze():
    data = request.get_json() or {}
    text = data.get('text', '')
    model = data.get('model', 'logistic_regression')
    result = nlp_engine.analyze_text(text, model_choice=model)
    return jsonify(result)

# ---------------- DOWNLOAD REPORTS ----------------

@main_bp.route('/api/download/report/pdf')
def download_pdf_report():
    symbol = sanitize_symbol(request.args.get('symbol', 'AAPL'))
    model_key = request.args.get('model', 'random_forest')
    
    df = get_stock_data(symbol)
    if df is None:
        flash("Stock data unavailable for PDF generation.", "danger")
        return redirect(url_for('main.prediction', symbol=symbol))
        
    reg_res = train_regression_model(df, model_key=model_key)
    tech_res = generate_signals_and_recommendation(df)
    risk_info = calculate_stock_stats(symbol) or {}
    
    pdf_buffer = generate_pdf_report(
        stock_symbol=symbol,
        model_name=reg_res['model_name'],
        metrics=reg_res['metrics'],
        forecast_data=reg_res,
        tech_signals=tech_res,
        risk_info=risk_info
    )
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{symbol}_AI_Prediction_Report.pdf",
        mimetype='application/pdf'
    )

@main_bp.route('/api/download/report/csv')
def download_csv_report():
    symbol = sanitize_symbol(request.args.get('symbol', 'AAPL'))
    model_key = request.args.get('model', 'random_forest')
    
    df = get_stock_data(symbol)
    if df is None:
        return "Stock data unavailable", 404
        
    reg_res = train_regression_model(df, model_key=model_key)
    csv_str = generate_csv_report(
        stock_symbol=symbol,
        model_name=reg_res['model_name'],
        metrics=reg_res['metrics'],
        forecast_data=reg_res
    )
    
    return (
        csv_str,
        200,
        {
            'Content-Disposition': f'attachment; filename="{symbol}_forecast.csv"',
            'Content-Type': 'text/csv'
        }
    )
