from app import app

from flask import jsonify
from datetime import datetime


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    response = {
        "message": "Healthcheck is running",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 200
