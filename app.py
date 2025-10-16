# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="Arrow Travel Days Tracker", page_icon="✈️", layout="wide")

POLICY_START_DATE = datetime(2025, 9, 30)
POLICY_LIMIT_DAYS = 250
DATA_FILE = "employees.csv"  # persistent CSV

AUTHORIZED_EMAILS = {
    "info@chiinsurancebrokers.com",
    "sof@arrowship.com",
    "info@okto.gr",
    "lsm@arrowship.com",
    "oslaney@pulse-insurance.co.uk"
}

# -----------------------------
# Helper functions
# -----------------------------
def safe_load_csv(path):
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Normalize columns
        expected = ["Employee", "Days Traveled", "Travel Start", "Travel End", "Route", "Email"]
        for c in expected:
            if c not in df.columns:
                df[c] = ""
        # Parse Days Traveled to int (coerce)
        df["Days Traveled"] = pd.to_numeric(df["Days Traveled"], errors="coerce").fillna(0).astype(int)
        return df[expected]
    else:
        # create empty with headers
        df = pd.DataFrame(columns=["Employee", "Days Traveled", "Travel Start", "Travel End", "Route", "Email"])
        df.to_csv(path, index=False)
        return df

def compute_summary(df):
    total_days = df["Days Traveled"].sum()
    remaining = POLICY_LIMIT_DAYS - total_days
    elapsed = (date.today() - POLICY_START_DATE.date()).days
    # group trips by employee and collect trips
    trips = {}
    for _, row in df.iterrows():
        name = row["Employee"]
        trips.setdefault(name, []).append({
            "days": int(row["Days Traveled"]),
            "start": row["Travel Start"],
            "end": row["Travel End"],
            "route": row["Route"],
            "email": row.get("Email", "")
        })
    return {
        "total_days": int(total_days),
        "days_remaining": int(remaining),
        "days_since_policy_start": int(elapsed),
        "trips_by_employee": trips
    }

# -----------------------------
# API mode (JSON output for frontend)
# -----------------------------
query_params = st.experimental_get_query_params()
if query_params.get("api", ["false"])[0].lower() == "true":
    df_api = safe_load_csv(DATA_FILE)
    summary = compute_summary(df_api)
    st.json(summary)
    st.stop()

# -----------------------------
# App UI
# -----------------------------
st.title("✈️ Arrow Travel Days Tracker (backend)")

# login via session_state
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

st.session_state.user_email = st.text_input("Enter your email to access the dashboard:", value=st.session_state.user_email)

if st.session_state.user_email.strip().lower() not in AUTHORIZED_EMAILS:
    st.warning("⚠️ Access restricted. Please use an authorized email.")
    st.stop()
else:
    st.success(f"Welcome {st.session_state.user_email}! 👋")

# load CSV
df = safe_load_csv(DATA_FILE)

# Add new trip form
st.subheader("➕ Add / Append a new trip (will be saved to employees.csv)")
with st.form("add_trip_form", clear_on_submit=True):
    employee = st.text_input("Employee Name")
    email = st.text_input("Employee Email (optional)")
    start_date = st.date_input("Travel Start Date")
    end_date = st.date_input("Travel End Date")
    route = st.text_input("Route (e.g. ATH-SIN-ATH)")
    submitted = st.form_submit_button("Add Trip ✈️")
    if submitted:
        if not employee.strip():
            st.error("Please enter an employee name.")
        elif start_date > end_date:
            st.error("Start date cannot be after End date.")
        else:
            days_traveled = (end_date - start_date).days + 1
            new_row = {
                "Employee": employee.strip(),
                "Days Traveled": days_traveled,
                "Travel Start": start_date.strftime("%Y-%m-%d"),
                "Travel End": end_date.strftime("%Y-%m-%d"),
                "Route": route.strip(),
                "Email": email.strip()
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Trip added for {employee} — {days_traveled} days saved to {DATA_FILE}")
            st.experimental_rerun()

# show dashboard
summary = compute_summary(df)
st.header("📊 Current Travel Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Days Used", f"{summary['total_days']} 🧳")
col2.metric("Days Remaining", f"{summary['days_remaining']} 🎯")
col3.metric("Days Since Policy Start", f"{summary['days_since_policy_start']} ⏳")

# show trips table
st.subheader("👥 All trips (employees.csv)")
st.dataframe(df, use_container_width=True)

# Download CSV
st.download_button("💾 Download CSV", df.to_csv(index=False).encode("utf-8"), file_name="employees.csv", mime="text/csv")
