import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()  

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    db_url = (os.getenv("DATABASE_URL") or "").strip()
    if not db_url:
        db_url = "sqlite:///eventfinder.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # register models and create tables
    from . import models  
    with app.app_context():
        db.create_all()

    # routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
 