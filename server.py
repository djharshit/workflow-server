from datetime import datetime
from os import environ

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Variables
load_dotenv()
GOOGLE_CHAT_WEBHOOK_URL: str = environ.get("GOOGLE_CHAT_WEBHOOK_URL", "")
THRESHOLD_TIME_STR = "10:15:00"

employee_list: list[str] = [
    "Siva Munaga 227243",
    "sainath Billadar 227242",
    "Naresh Batta 227241",
    "Divyang Dheer 227240",
    "Aswin KS 227239",
    "Harshit Mehra 227238",
    "Hrithika Madireddy 227237",
    "Aditi Padshala 227236",
    "Shivakumar kummari 227235",
    "Saikiran Bhushaboina 227229",
    "Rohit Sai Katikireddy 227228",
    "Maroju Brahmateja 227225",
    "Varun Bukka 227224",
    "Abbas Khan 227149",
    "Shubham Singh 227175",
    "Saikiran Bhushaboina 227229",
    "Rohit Sai Katikireddy 227228",
    "Maroju Brahmateja 227225",
    "Varun Bukka 227224",
    "Abbas Khan 227149",
    "Shubham Singh 227175",
]
admin_list: list[str] = [
    "Chinmay Sanghi CEO",
    "CSM CSM Mentor",
    "Ashish ashishjain MD",
    "Manideep Singapaka 227234",
]
empl_ontime: list[str] = []
admin_ontime: list[str] = []

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

    emp_id: str = form_data.get("emp_id", "")
    checkin_from_time: str = form_data.get("checkin_from_time", "")

    threshold_time = datetime.strptime(THRESHOLD_TIME_STR, "%H:%M:%S").time()
    checkin_time = datetime.strptime(checkin_from_time, "%d-%m-%Y %H:%M:%S").time()

    if checkin_time > threshold_time:
        pass

    else:
        if emp_id in employee_list:
            empl_ontime.append(emp_id)
            print(f"{emp_id} is on time at {checkin_time}")
        elif emp_id in admin_list:
            admin_ontime.append(emp_id)
            print(f"{emp_id} is on time at {checkin_time}")

    return jsonify({"message": "Success"})


@app.route("/googlechat", methods=["GET"])
def googlechat():
    message = f"""Employees who have not yet checkin\n\n{'\n'.join(set(employee_list) - set(empl_ontime))}
    \nAdmins who have not yet checkin\n\n{'\n'.join(set(admin_list) - set(admin_ontime))}"""

    print(message)
    post_to_google_chat(message)

    empl_ontime.clear()
    admin_ontime.clear()

    return jsonify({"message": "Success"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
