from app import app
import database as db

from flask import jsonify
from datetime import datetime


@app.get("/healthcheck")
def healthcheck():
    response = {
        "message": "Healthcheck is running",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 200
