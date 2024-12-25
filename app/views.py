from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from app.models import db, Accounts, User, Category, Record
from app.schemas import *

views = Blueprint("views", __name__)

user_schema = UserSchema()
categories_schema = CategorySchema()
categories_schema_for_output = CategorySchemaForOutput()
records_schema = RecordSchema()
records_schema_for_output = RecordSchemaForOutput()

account_schema = AccountSchema()
funds_schema = FundsSchema()


@views.get("/healthcheck")
def healthcheck():
    response = {
        "message": "Healthcheck is running",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 200


# users
@views.post("/user/register")
def register_user():
    user_data = request.get_json()
    err = user_schema.validate(user_data)
    if err:
        return jsonify(err), 400

    user = User(
        username=user_data["username"],
        password=pbkdf2_sha256.hash(user_data["password"])
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400

    response = {
        "id": user.id,
        "message": "User registered",
        "date": datetime.today(),
    }
    return jsonify(response), 201


@views.post("/user/login")
def login():
    user_data = request.get_json()

    err = user_schema.validate(user_data)
    if err:
        return jsonify(err), 400

    username = user_data["username"]
    password = user_data["password"]

    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "user_id": user.id
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401


@views.get("/users")
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)), 200


@views.get("/user/<int:user_id>")
@jwt_required()
def get_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user_schema.dump(user)), 200


@views.delete("/user/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


# categories
@views.post("/category")
def create_category():
    data = request.get_json()
    err = categories_schema.validate(data)
    if err:
        return jsonify(err), 400

    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()

    response = {
        "message": "Category created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201


@views.get("/category")
def get_categories():
    categories = Category.query.all()
    if categories:
        return jsonify(categories_schema_for_output.dump(categories, many=True)), 200
    else:
        return jsonify({"message": "Categories not found"}), 404


@views.delete("/category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


# records
@views.post("/record")
@jwt_required()
def create_record():
    data = request.get_json()
    err = records_schema.validate(data)
    if err:
        return jsonify(err), 400

    current_user_id = int(get_jwt_identity())
    if current_user_id != data["user_id"]:
        return jsonify({"message": "Access denied"}), 403

    user = User.query.filter_by(id=data["user_id"]).first()
    if not user:
        return jsonify({"message": "User with the given ID does not exist"}), 400
    category = Category.query.filter_by(id=data["category_id"]).first()
    if not category:
        return jsonify({"message": "Category with the given ID does not exist"}), 400

    account = Accounts.query.filter_by(user_id=data['user_id']).first()
    if not account:
        return jsonify({"message": "Account for user with this id not found"}), 400

    if account.balance >= data['money_spent']:
        record = Record(user_id=user.id, category_id=category.id, money_spent=data["money_spent"])
        db.session.add(record)
        account.balance -= data['money_spent']
        db.session.commit()
        response = {
            "message": "Record created",
            "amount": data['money_spent'],
            "date": datetime.today(),
            "status": "ok"
        }
        return jsonify(response), 201
    else:
        return jsonify({"message": "Insufficient funds, operation aborted"}), 400


@views.get("/record/<int:record_id>")
@jwt_required()
def get_record(record_id):
    record = Record.query.filter_by(id=record_id).first()

    current_user_id = int(get_jwt_identity())
    if current_user_id != record.user_id or not record:
        return jsonify({"message": "Access denied"}), 403

    return jsonify(records_schema_for_output.dump(record)), 200


@views.delete("/record/<int:record_id>")
@jwt_required()
def delete_record(record_id):
    record = Record.query.filter_by(id=record_id).first()

    current_user_id = int(get_jwt_identity())
    if current_user_id != record.user_id or not record:
        return jsonify({"message": "Access denied"}), 403

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted"}), 200


@views.get("/record")
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return jsonify({"message": "user_id or category_id is required"}), 400

    query = Record.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    if category_id is not None:
        query = query.filter_by(category_id=category_id)

    filtered_records = query.all()
    return jsonify(records_schema_for_output.dump(filtered_records, many=True)), 200


# PostgreSQL DB endpoints
@views.get("/dbcheck")
def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"message": "Database connection is healthy"}), 200
    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500


@views.post("/accounts/create")
@jwt_required()
def create_account():
    data = request.get_json()
    err = account_schema.validate(data)
    if err:
        return jsonify(err), 400

    current_user_id = int(get_jwt_identity())
    if current_user_id != data["user_id"]:
        return jsonify({"message": "Access denied"}), 403

    try:
        account = Accounts(user_id=data['user_id'], balance=data.get('balance', 0.0))
        db.session.add(account)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Account creation failed", "error": "You already have your account"}), 400

    return jsonify(account_schema.dump(account)), 201


@views.post("/accounts/add-funds")
@jwt_required()
def add_funds():
    data = request.get_json()
    err = funds_schema.validate(data)
    if err:
        return jsonify(err), 400

    current_user_id = int(get_jwt_identity())
    if current_user_id != data["user_id"]:
        return jsonify({"message": "Access denied"}), 403

    account = Accounts.query.filter_by(user_id=data['user_id']).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404

    account.balance += data['amount']
    db.session.commit()
    response = {
        "message": "Funds added",
        "amount": data['amount'],
        "date": datetime.today()
    }
    return jsonify(response), 201


@views.get("/accounts")
def get_all_accounts():
    accounts = Accounts.query.all()
    if accounts:
        return jsonify(account_schema.dump(accounts, many=True)), 200
    else:
        return jsonify({"message": "Accounts not found"}), 404


@views.get("/accounts/user/<int:user_id>")
@jwt_required()
def get_account_by_user_id(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    account = Accounts.query.filter_by(user_id=user_id).first()
    if account:
        return jsonify(account_schema.dump(account)), 200
    else:
        return jsonify({"message": "Account not found"}), 404


@views.delete("/accounts/user/<int:user_id>")
@jwt_required()
def delete_account(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"message": "Access denied"}), 403

    account = Accounts.query.filter_by(user_id=user_id).first()
    if not account:
        return jsonify({"message": "Account not found"}), 404

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200
