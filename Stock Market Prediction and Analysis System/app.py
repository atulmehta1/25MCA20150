import os
import json
from datetime import datetime
from flask import Flask, render_template
from config import Config
from database import db, User, DatasetMeta, AuditLog
from backend.auth import auth_bp
from backend.routes import main_bp
from backend.admin import admin_bp
from backend.data_loader import get_stock_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Context processors for all Jinja templates
    @app.context_processor
    def inject_globals():
        return {
            'supported_stocks': Config.SUPPORTED_STOCKS,
            'current_year': datetime.now().year,
            'app_name': 'StockAI Intelligence'
        }

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_code=404, error_message="Page Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_code=500, error_message="Internal Server Error"), 500

    # Auto-seed database tables and default admin/demo accounts
    with app.app_context():
        db.create_all()

        # Seed default Admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@stockai.local', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)

        # Seed default Demo User
        demo_user = User.query.filter_by(username='demo').first()
        if not demo_user:
            demo_user = User(username='demo', email='demo@stockai.local', role='user')
            demo_user.set_password('demo123')
            db.session.add(demo_user)

        # Seed pre-bundled dataset metadata
        for symbol, info in Config.SUPPORTED_STOCKS.items():
            existing = DatasetMeta.query.filter_by(symbol=symbol).first()
            if not existing:
                filename = f"{symbol}.csv"
                df = get_stock_data(symbol)
                row_cnt = len(df) if df is not None else 0
                cols = list(df.columns) if df is not None else []
                meta = DatasetMeta(
                    filename=filename,
                    symbol=symbol,
                    row_count=row_cnt,
                    features=json.dumps(cols),
                    is_system=True
                )
                db.session.add(meta)

        db.session.commit()

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
