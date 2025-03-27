from flask import Flask

from .config import Config
from .extensions import db, login_manager, migrate
from .ranks.routes import ranks
from .auth.routes import auth
from .scheduler import scheduler, save_xp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(ranks)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Сначала нужно авторизоваться"
    login_manager.login_message_category = "error"

    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        db.create_all()

    return app
