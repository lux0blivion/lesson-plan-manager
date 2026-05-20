import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .logger import setup_logger

load_dotenv()

db = SQLAlchemy()
logger = setup_logger(__name__)


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///lesson_plans.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    from .routes.lesson_plans import lesson_plans_bp
    from .routes.health import health_bp

    app.register_blueprint(lesson_plans_bp, url_prefix="/api/lesson-plans")
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()
        logger.info("database_initialized", message="All tables created")

    return app
