from flask import Blueprint, jsonify
from .. import db
from ..logger import setup_logger

health_bp = Blueprint("health", __name__)
logger = setup_logger(__name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error("health_check_db_error", error=str(e))
        db_status = "unhealthy"

    status = "healthy" if db_status == "healthy" else "degraded"

    logger.info("health_check", status=status, db=db_status)

    return jsonify(
        {
            "status": status,
            "services": {
                "database": db_status,
                "api": "healthy",
            },
        }
    ), (200 if status == "healthy" else 503)
