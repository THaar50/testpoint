from secrets import token_urlsafe
from flask import Flask
from .storage import db
from .views import views
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
    db.init_app(app=app)

    app.register_blueprint(views,  url_prefix='/')

    return app
