from app import app
import database as db

from flask import jsonify, request
from datetime import datetime


@app.get("/healthcheck")
def healthcheck():
    response = {
        "message": "Healthcheck is running",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 200


@app.post("/user")
def create_user():
    db.add_user(request.get_json())
    response = {
        "message": "User created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201


@app.get("/users")
def get_users():
    return jsonify(db.get_all_users()), 200


@app.get("/user/<int:user_id>")
def get_user(user_id):
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404


@app.delete("/user/<int:user_id>")
def delete_user(user_id):
    if db.delete_user_by_id(user_id):
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404