from datetime import datetime
from os import environ

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

GOOGLE_CHAT_WEBHOOK_URL = environ.get("GOOGLE_CHAT_WEBHOOK_URL", "")

app = Flask(__name__)


def post_to_google_chat(message: str):
    res = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json={"text": message})
    if res.status_code == 200:
        print("Message posted successfully")
    else:
        print("Failed to post message")


@app.route("/")
def index():
    return jsonify({"message": "Hello, World!"})


@app.route("/workflow", methods=["POST"])
def workflow():
    form_data = request.form

    emp_id = form_data.get("emp_id", "")
    checkin_from_time = form_data.get("checkin_from_time", "")

    threshold_time_str = "10:15:00"
    threshold_time = datetime.strptime(threshold_time_str, "%H:%M:%S").time()

    checkin_time = datetime.strptime(checkin_from_time, "%d-%m-%Y %H:%M:%S").time()

    if checkin_time > threshold_time:
        late_by = datetime.combine(datetime.min, checkin_time) - datetime.combine(
            datetime.min, threshold_time
        )
        print(f"{emp_id} is late by {late_by}")
        post_to_google_chat(f"{emp_id} is late by {late_by}")

    else:
        print(f"{emp_id} is on time at {checkin_time}")

    return jsonify({"message": "Success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
