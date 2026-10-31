import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    predictions = db.relationship('PredictionHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    portfolios = db.relationship('PortfolioPlan', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class DatasetMeta(db.Model):
    __tablename__ = 'datasets_meta'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    row_count = db.Column(db.Integer, default=0)
    features = db.Column(db.Text, default='[]')
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    is_system = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'symbol': self.symbol,
            'row_count': self.row_count,
            'features': json.loads(self.features) if self.features else [],
            'is_system': self.is_system,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    symbol = db.Column(db.String(50), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(20), default='regression')  # regression or classification
    metrics = db.Column(db.Text, default='{}')
    target_date = db.Column(db.String(50), nullable=True)
    predicted_value = db.Column(db.String(100), nullable=True)
    signal = db.Column(db.String(20), default='HOLD')  # BUY, HOLD, SELL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.username if self.user else 'Guest',
            'symbol': self.symbol,
            'model_name': self.model_name,
            'task_type': self.task_type,
            'metrics': json.loads(self.metrics) if self.metrics else {},
            'target_date': self.target_date,
            'predicted_value': self.predicted_value,
            'signal': self.signal,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class PortfolioPlan(db.Model):
    __tablename__ = 'portfolio_plans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    investment_amount = db.Column(db.Float, nullable=False)
    risk_tolerance = db.Column(db.String(20), default='Medium')  # Low, Medium, High
    allocations = db.Column(db.Text, nullable=False)  # JSON {ticker: {weight: float, amount: float}}
    expected_return = db.Column(db.Float, default=0.0)
    volatility = db.Column(db.Float, default=0.0)
    sharpe_ratio = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'investment_amount': self.investment_amount,
            'risk_tolerance': self.risk_tolerance,
            'allocations': json.loads(self.allocations) if self.allocations else {},
            'expected_return': self.expected_return,
            'volatility': self.volatility,
            'sharpe_ratio': self.sharpe_ratio,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(80), default='System')
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, default='')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }
