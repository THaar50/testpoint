from datetime import timedelta
from secrets import token_urlsafe
from flask import Flask
from .storage import db
from .loginManager import login_manager
from .views import views
from .auth import auth
from .routes import routes
from .config import DB_USER, DB_PW, DB_ADDRESS, DB_PORT, DB_NAME


def create_app() -> Flask:
    """
    Creates a Flask application setting, its secret and linking it with the database.
    :return: Flask application.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_urlsafe(nbytes=256)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PW}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    db.init_app(app=app)
    login_manager.init_app(app=app)

    app.register_blueprint(views,  url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')

    return app
