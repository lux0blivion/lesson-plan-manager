from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import asc, desc
from datetime import date

from .. import db
from ..models.lesson_plan import LessonPlan
from ..services import (
    get_ai_recommendations,
    lesson_plan_schema,
    lesson_plans_schema,
    lesson_plan_update_schema,
    smart_assist_schema,
)
from ..logger import setup_logger

lesson_plans_bp = Blueprint("lesson_plans", __name__)
logger = setup_logger(__name__)


@lesson_plans_bp.route("", methods=["GET"])
def list_lesson_plans():
    """List lesson plans with filtering, search, sorting and pagination."""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = min(per_page, 50)

    discipline = request.args.get("discipline", "").strip()
    tag = request.args.get("tag", "").strip()
    scheduled_date = request.args.get("scheduled_date", "").strip()
    search = request.args.get("search", "").strip()
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")

    query = LessonPlan.query

    if discipline:
        query = query.filter(LessonPlan.discipline.ilike(f"%{discipline}%"))

    if tag:
        query = query.filter(LessonPlan.tags.ilike(f"%{tag}%"))

    if scheduled_date:
        try:
            parsed_date = date.fromisoformat(scheduled_date)
            query = query.filter(LessonPlan.scheduled_date == parsed_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if search:
        query = query.filter(LessonPlan.title.ilike(f"%{search}%"))

    sort_column_map = {
        "title": LessonPlan.title,
        "created_at": LessonPlan.created_at,
        "scheduled_date": LessonPlan.scheduled_date,
    }
    sort_col = sort_column_map.get(sort_by, LessonPlan.created_at)
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = lesson_plans_schema.dump(pagination.items)

    logger.info(
        "lesson_plans_listed",
        page=page,
        total=pagination.total,
        filters={"discipline": discipline, "tag": tag, "search": search},
    )

    return jsonify(
        {
            "items": items,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }
    )


@lesson_plans_bp.route("/<int:plan_id>", methods=["GET"])
def get_lesson_plan(plan_id):
    """Get a single lesson plan."""
    plan = LessonPlan.query.get_or_404(plan_id, description="Lesson plan not found")
    return jsonify(lesson_plan_schema.dump(plan))


@lesson_plans_bp.route("", methods=["POST"])
def create_lesson_plan():
    """Create a new lesson plan."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        data = lesson_plan_schema.load(json_data)
    except ValidationError as err:
        logger.warning("validation_error_create", errors=err.messages)
        return jsonify({"errors": err.messages}), 422

    tags_str = ",".join(data.get("tags", [])) if data.get("tags") else ""

    plan = LessonPlan(
        title=data["title"],
        objective=data["objective"],
        summary=data["summary"],
        scheduled_date=data.get("scheduled_date"),
        discipline=data["discipline"],
        contents=data.get("contents"),
        support_resources=data.get("support_resources"),
        tags=tags_str,
    )

    db.session.add(plan)
    db.session.commit()

    logger.info("lesson_plan_created", plan_id=plan.id, title=plan.title)
    return jsonify(lesson_plan_schema.dump(plan)), 201


@lesson_plans_bp.route("/<int:plan_id>", methods=["PUT"])
def update_lesson_plan(plan_id):
    """Update an existing lesson plan."""
    plan = LessonPlan.query.get_or_404(plan_id, description="Lesson plan not found")

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        data = lesson_plan_update_schema.load(json_data)
    except ValidationError as err:
        logger.warning("validation_error_update", plan_id=plan_id, errors=err.messages)
        return jsonify({"errors": err.messages}), 422

    for field in [
        "title",
        "objective",
        "summary",
        "scheduled_date",
        "discipline",
        "contents",
        "support_resources",
    ]:
        if field in data:
            setattr(plan, field, data[field])

    if "tags" in data:
        plan.tags = ",".join(data["tags"])

    db.session.commit()

    logger.info("lesson_plan_updated", plan_id=plan.id)
    return jsonify(lesson_plan_schema.dump(plan))


@lesson_plans_bp.route("/<int:plan_id>", methods=["DELETE"])
def delete_lesson_plan(plan_id):
    """Delete a lesson plan."""
    plan = LessonPlan.query.get_or_404(plan_id, description="Lesson plan not found")
    db.session.delete(plan)
    db.session.commit()

    logger.info("lesson_plan_deleted", plan_id=plan_id)
    return jsonify({"message": "Lesson plan deleted successfully"}), 200


@lesson_plans_bp.route("/smart-assist", methods=["POST"])
def smart_assist():
    """Generate AI-powered recommendations for a lesson plan."""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        data = smart_assist_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    logger.info(
        "smart_assist_requested",
        title=data["title"],
        discipline=data["discipline"],
    )

    try:
        recommendations = get_ai_recommendations(
            title=data["title"],
            discipline=data["discipline"],
            summary=data["summary"],
        )
        return jsonify(recommendations)
    except Exception as e:
        logger.error(
            "smart_assist_failed",
            error=str(e),
            title=data["title"],
        )
        return jsonify({"error": "AI service temporarily unavailable. Please try again."}), 503


@lesson_plans_bp.route("/disciplines", methods=["GET"])
def list_disciplines():
    """List all unique disciplines."""
    results = db.session.query(LessonPlan.discipline).distinct().all()
    disciplines = sorted([r[0] for r in results if r[0]])
    return jsonify(disciplines)


@lesson_plans_bp.route("/tags", methods=["GET"])
def list_tags():
    """List all unique tags."""
    results = db.session.query(LessonPlan.tags).all()
    all_tags = set()
    for row in results:
        if row[0]:
            for tag in row[0].split(","):
                t = tag.strip()
                if t:
                    all_tags.add(t)
    return jsonify(sorted(list(all_tags)))
