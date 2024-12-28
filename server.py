import sqlite3
from datetime import datetime
from os import environ

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Variables
load_dotenv()
GOOGLE_CHAT_WEBHOOK_URL: str = environ.get("GOOGLE_CHAT_WEBHOOK_URL", "")
PORT: int = int(environ.get("PORT", 0))


def post_to_google_chat(message: str) -> bool:
    res = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json={"text": message})
    if res.status_code == 200:
        print(res.text)
        print("Message posted successfully")

        return True
    else:
        print("Failed to post message")

        return False


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "Workflow server is running...", "status": "ok"})


@app.route("/zoho", methods=["POST"])
def workflow():
    try:
        form_data = request.form

        if form_data.get("emp_id", "") == "EmployeeID":
            return jsonify({"message": "Invalid request"}), 400

        fname: str = form_data.get("emp_id", "").split(" ")[0]
        lname: str = form_data.get("emp_id", "").split(" ")[1]
        emp_id: str = form_data.get("emp_id", "").split(" ")[2]
        checkin_from_time: str = form_data.get("checkin_from_time", "")

        print(form_data.get("desc", ""))

        checkin_time = datetime.strptime(checkin_from_time, "%d-%m-%Y %H:%M:%S").strftime("%H:%M:%S")
        print(fname, emp_id, checkin_time)

        conn = sqlite3.connect("workflow.db")
        cur = conn.cursor()
        cur.execute(
            "UPDATE employee SET ischeckin = 1, checktime = ? WHERE id = ?",
            (checkin_time, emp_id),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Success"}), 200

    except Exception as e:
        print(type(e).__name__, e)

        return jsonify({"message": "Error"}), 500


@app.route("/<int:t>", methods=["GET"])
def googlechat(t: int):
    ttime = ""

    conn = sqlite3.connect("workflow.db")
    cur = conn.cursor()

    cur.execute("SELECT name FROM employee where ischeckin = 0")

    employee_list = cur.fetchall()
    print(employee_list)

    if t == 1:
        ttime = "10:15 AM"
    elif t == 2:
        ttime = "11:00 AM"
        cur.execute("UPDATE employee SET ischeckin = 0")
        conn.commit()

    conn.close()

    message = f"Team members who have not checked-in till {ttime}\n\n{'\n'.join((i[0] for i in employee_list))}"
    print(message)

    # post_to_google_chat(message)

    return jsonify({"message": "Success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT)
