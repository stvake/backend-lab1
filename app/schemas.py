from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class CategorySchema(Schema):
    name = fields.Str(required=True)


class CategorySchemaForOutput(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class RecordSchema(Schema):
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    money_spent = fields.Float(required=True)


class RecordSchemaForOutput(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    money_spent = fields.Float(required=True)


class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Float()


class FundsSchema(Schema):
    user_id = fields.Int(required=True)
    amount = fields.Float(required=True)
