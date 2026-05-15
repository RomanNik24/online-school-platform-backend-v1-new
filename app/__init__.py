from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_all(app)
    migrate.init_app(app, db)

    # Register Blueprints (Mock for now)
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Example routes
    from flask_login import login_required, current_user

    # 4. Обработка ролей (логика входа)
    @app.route('/')
    @login_required
    def index():
        # Перенаправление пользователя в зависимости от его роли
        if current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('auth.logout'))

    # Маршрут для проверки работоспособности системы
    @app.route('/ping')
    def ping():
        return "Pong! Система в порядке."

    return app
