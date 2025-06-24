from flask import Flask
from .config import Config
from .extensions import db, mail, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.api.auth_routes import auth_bp
    from app.api.admin_routes import admin_bp
    from app.api.post_routes import post_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(post_bp, url_prefix='/api/post')

    return app
