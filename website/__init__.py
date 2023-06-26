from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "posers"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'youmayremembermefromsuchselfhelpvideosassmokeyourselfthinandgetconfidencestupid'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres@localhost:5432/{DB_NAME}'
    db.init_app(app)

    from .auth import auth
    from .messages import messages
    from .posts import posts
    from .profiles import profiles
    from .search import search, SearchForm
    from .groups import groups

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(messages, url_prefix='/')
    app.register_blueprint(posts, url_prefix='/')
    app.register_blueprint(profiles, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')
    app.register_blueprint(groups, url_prefix='/')
    from .models import Users
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.context_processor
    def base():
        form = SearchForm()
        return dict(form=form)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):

        with app.app_context():
            db.create_all()
        print('Created Database!')
