"""Module providingFunction printing python version."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()


def something():
    "where the app starts to load"
    app.config.from_object("application.config.Config")
    app.logger.info(f'ENV is set to: {app.config["ENV"]}')
    app.logger.info(app.config)
    with app.app_context():
        db.init_app(app)
    login_manager.init_app(app)
    from application.main.main_controller import main
    app.register_blueprint(main, url_prefix="/")
    from application.portal.portal_controller import dash
    app.register_blueprint(dash, url_prefix="/portal/dash")
    from application.admin.admin_controller import admin
    app.register_blueprint(admin, url_prefix="/portal/admin")
    return app
