# app/__init__.py

from flask import Flask
from .movies import movies_bp
from .comments import comments_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(movies_bp)
    app.register_blueprint(comments_bp)
    return app
