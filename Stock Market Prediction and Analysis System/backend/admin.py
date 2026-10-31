import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, g
from werkzeug.utils import secure_filename
from database import db, User, DatasetMeta, PredictionHistory, AuditLog
from backend.auth import admin_required
from backend.data_loader import get_stock_data, normalize_columns
from backend.ml_engine import train_regression_model
from config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    users = User.query.order_by(User.created_at.desc()).all()
    datasets = DatasetMeta.query.order_by(DatasetMeta.created_at.desc()).all()
    predictions = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(50).all()
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(50).all()
    
    total_users = User.query.count()
    total_predictions = PredictionHistory.query.count()
    total_datasets = DatasetMeta.query.count()
    
    return render_template(
        'admin.html',
        users=users,
        datasets=datasets,
        predictions=predictions,
        logs=logs,
        total_users=total_users,
        total_predictions=total_predictions,
        total_datasets=total_datasets
    )

@admin_bp.route('/user/<int:user_id>/toggle-role', methods=['POST'])
@admin_required
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == session.get('user_id'):
        flash("You cannot change your own admin role.", "warning")
        return redirect(url_for('admin.admin_dashboard'))
        
    user.role = 'admin' if user.role == 'user' else 'user'
    log = AuditLog(
        user_id=session.get('user_id'),
        username=session.get('username'),
        action='ROLE_CHANGE',
        details=f"Changed user {user.username} role to {user.role}"
    )
    db.session.add(log)
    db.session.commit()
    flash(f"Updated role for {user.username} to {user.role}.", "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == session.get('user_id'):
        flash("You cannot delete your own account from admin panel.", "danger")
        return redirect(url_for('admin.admin_dashboard'))
        
    username = user.username
    db.session.delete(user)
    log = AuditLog(
        user_id=session.get('user_id'),
        username=session.get('username'),
        action='DELETE_USER',
        details=f"Deleted user {username} (ID: {user_id})"
    )
    db.session.add(log)
    db.session.commit()
    flash(f"User {username} deleted successfully.", "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/dataset/upload', methods=['POST'])
@admin_required
def upload_dataset():
    if 'file' not in request.files:
        flash('No file part selected.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
        
    file = request.files['file']
    symbol = request.form.get('symbol', '').strip().upper()
    
    if file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
        
    if file and file.filename.endswith(('.csv', '.txt')):
        filename = secure_filename(file.filename)
        if not symbol:
            symbol = filename.split('.')[0].upper()
            
        save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(save_path)
        
        # Read and inspect
        try:
            import pandas as pd
            df = pd.read_csv(save_path)
            df = normalize_columns(df)
            row_count = len(df)
            features = json.dumps(list(df.columns))
            
            meta = DatasetMeta(
                filename=filename,
                symbol=symbol,
                row_count=row_count,
                features=features,
                uploaded_by=session.get('user_id'),
                is_system=False
            )
            db.session.add(meta)
            
            log = AuditLog(
                user_id=session.get('user_id'),
                username=session.get('username'),
                action='DATASET_UPLOAD',
                details=f"Uploaded custom dataset {filename} for {symbol} with {row_count} rows."
            )
            db.session.add(log)
            db.session.commit()
            
            flash(f"Dataset {filename} uploaded successfully ({row_count} rows).", "success")
        except Exception as e:
            flash(f"Failed to process CSV: {str(e)}", "danger")
    else:
        flash("Invalid file format. Please upload a CSV file.", "danger")
        
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/dataset/<int:dataset_id>/delete', methods=['POST'])
@admin_required
def delete_dataset(dataset_id):
    ds = DatasetMeta.query.get_or_404(dataset_id)
    if ds.is_system:
        flash("System datasets cannot be removed.", "warning")
        return redirect(url_for('admin.admin_dashboard'))
        
    filepath = os.path.join(Config.UPLOAD_FOLDER, ds.filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception:
            pass
            
    db.session.delete(ds)
    db.session.commit()
    flash(f"Dataset {ds.filename} removed.", "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/models/retrain', methods=['POST'])
@admin_required
def retrain_models():
    """Batch retrains models for all base stocks."""
    trained_count = 0
    errors = []
    
    for symbol in Config.SUPPORTED_STOCKS:
        try:
            df = get_stock_data(symbol)
            if df is not None and len(df) > 50:
                train_regression_model(df, model_key='random_forest')
                trained_count += 1
        except Exception as e:
            errors.append(f"{symbol}: {str(e)}")
            
    log = AuditLog(
        user_id=session.get('user_id'),
        username=session.get('username'),
        action='MODELS_RETRAINED',
        details=f"Batch retraining completed for {trained_count} stock models."
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': f"Successfully retrained models for {trained_count} stocks.",
        'errors': errors
    })
