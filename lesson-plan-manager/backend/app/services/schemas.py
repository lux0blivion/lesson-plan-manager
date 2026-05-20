from marshmallow import Schema, fields, validate


class CsvTagsField(fields.Field):
    """Serializes DB CSV string → list; deserializes list → kept as list for route to join."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return []
        if isinstance(value, str):
            return [t.strip() for t in value.split(",") if t.strip()]
        if isinstance(value, list):
            return value
        return []

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [t.strip() for t in value.split(",") if t.strip()]
        return []


class LessonPlanSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    objective = fields.Str(required=True, validate=validate.Length(min=5))
    summary = fields.Str(required=True, validate=validate.Length(min=5))
    scheduled_date = fields.Date(allow_none=True, load_default=None)
    discipline = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    contents = fields.Str(allow_none=True, load_default=None)
    support_resources = fields.Str(allow_none=True, load_default=None)
    tags = CsvTagsField(load_default=[])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LessonPlanUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=3, max=255))
    objective = fields.Str(validate=validate.Length(min=5))
    summary = fields.Str(validate=validate.Length(min=5))
    scheduled_date = fields.Date(allow_none=True)
    discipline = fields.Str(validate=validate.Length(min=2, max=100))
    contents = fields.Str(allow_none=True)
    support_resources = fields.Str(allow_none=True)
    tags = fields.List(fields.Str())


class SmartAssistSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3))
    discipline = fields.Str(required=True, validate=validate.Length(min=2))
    summary = fields.Str(required=True, validate=validate.Length(min=5))


lesson_plan_schema = LessonPlanSchema()
lesson_plans_schema = LessonPlanSchema(many=True)
lesson_plan_update_schema = LessonPlanUpdateSchema()
smart_assist_schema = SmartAssistSchema()
