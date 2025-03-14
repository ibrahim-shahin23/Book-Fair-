from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(environment='development'):

    app = Flask(__name__)
    app.config.from_object(config.get(environment, config['development']))
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from . import models
    register_blueprints(app)
    migrate.init_app(app, db)
    return app

def register_blueprints(app):
    from app.main.routes import main_blueprint
    from app.auth.routes import auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    return app