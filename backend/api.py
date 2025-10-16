from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

EMPLOYEES_FILE = "employees.csv"

# Load employees
def load_employees():
    df = pd.read_csv(EMPLOYEES_FILE)
    employees = []
    for _, row in df.iterrows():
        trips = []
        if pd.notna(row["trips"]):
            for t in row["trips"].split(";"):
                d, dates, route = t.split("|")
                trips.append({"days": int(d), "dates": dates, "route": route})
        employees.append({"name": row["name"], "email": row.get("email", ""), "trips": trips})
    return employees

# Get all employees
@app.route("/api/employees", methods=["GET"])
def get_employees():
    return jsonify(load_employees())

# Add a new trip
@app.route("/api/add-trip", methods=["POST"])
def add_trip():
    data = request.json
    employees = load_employees()
    for emp in employees:
        if emp["name"] == data["employee"]:
            emp["trips"].append(data["trip"])
    # Save back to CSV
    rows = []
    for emp in employees:
        trips_str = ";".join([f'{t["days"]}|{t["dates"]}|{t["route"]}' for t in emp["trips"]])
        rows.append({"name": emp["name"], "email": emp.get("email", ""), "trips": trips_str})
    pd.DataFrame(rows).to_csv(EMPLOYEES_FILE, index=False)
    return jsonify({"status": "success"})
