from datetime import datetime
from math import e
from os import environ

import requests
import sqlite3
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Variables
load_dotenv()
GOOGLE_CHAT_WEBHOOK_URL: str = environ.get("GOOGLE_CHAT_WEBHOOK_URL", "")
PORT: int = int(environ.get("PORT", 0))
THRESHOLD_TIME_STR = "10:15:00"

conn = sqlite3.connect("workflow.db", check_same_thread=False)
cur = conn.cursor()

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


@app.route("/zoho", methods=["POST"])
def workflow():
    try:
        form_data = request.form

        fname: str = form_data.get("emp_id", "").split(" ")[0]
        lname: str = form_data.get("emp_id", "").split(" ")[1]
        emp_id: str = form_data.get("emp_id", "").split(" ")[2]
        checkin_from_time: str = form_data.get("checkin_from_time", "")
        print(form_data.get("desc", ""))

        threshold_time = datetime.strptime(THRESHOLD_TIME_STR, "%H:%M:%S").time()
        checkin_time = datetime.strptime(checkin_from_time, "%d-%m-%Y %H:%M:%S").time()

        if checkin_time > threshold_time:
            print(f"{fname} {lname} is late at {checkin_time}")

        else:
            cur.execute("UPDATE employee SET ischeckin = 1 WHERE id = ?", (emp_id))
            conn.commit()

            print(f"{fname} {lname} is on time at {checkin_time}")

        return jsonify({"message": "Success"})

    except Exception as e:
        print(type(e).__name__, e)

        return jsonify({"message": "Error"}), 500


@app.route("/googlechat", methods=["GET"])
def googlechat():
    cur.execute("SELECT name FROM employee where ischeckin = 0")
    employee_list = cur.fetchall()

    message = f"Employees who have not yet checkin\n\n{'\n'.join((i[0] for i in employee_list))}"

    print(message)
    post_to_google_chat(message)

    cur.execute("UPDATE employee SET ischeckin = 0")
    conn.commit()

    return jsonify({"message": "Success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
