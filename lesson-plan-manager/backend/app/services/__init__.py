from .ai_service import get_ai_recommendations
from .schemas import (
    lesson_plan_schema,
    lesson_plans_schema,
    lesson_plan_update_schema,
    smart_assist_schema,
)

__all__ = [
    "get_ai_recommendations",
    "lesson_plan_schema",
    "lesson_plans_schema",
    "lesson_plan_update_schema",
    "smart_assist_schema",
]
