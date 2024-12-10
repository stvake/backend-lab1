from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    money_spent = fields.Float(required=True)
