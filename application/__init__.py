"""Module providingFunction printing python version."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os.path import join, dirname
import os


app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()


def something():
    "where the app starts to load"
    app.config.from_object("application.config.Config")
    app.logger.info(f'ENV is set to: {app.config["ENV"]}')
    app.logger.info(app.config)
    dotenv_path = join(dirname(__file__), '.flaskenv')
    load_dotenv(dotenv_path)
    YOCO_PUBLIC_KEY = os.environ.get("YOCO_PUBLIC_KEY")
    YOCO_TEST_KEY = os.environ.get("YOCO_TEST_KEY")
    print(YOCO_PUBLIC_KEY)
    print(YOCO_TEST_KEY)
    with app.app_context():
        db.init_app(app)
    login_manager.init_app(app)
    from application.main.main_controller import main
    app.register_blueprint(main, url_prefix="/")
    from application.portal.portal_controller import dash
    app.register_blueprint(dash, url_prefix="/portal/dash")
    from application.admin.admin_controller import admin
    app.register_blueprint(admin, url_prefix="/portal/admin")
    from application.webhook.hook_controller import hook
    app.register_blueprint(hook, url_prefix="/hook")
    return app
