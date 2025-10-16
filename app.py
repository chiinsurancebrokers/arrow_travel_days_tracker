import streamlit as st
import pandas as pd
from datetime import datetime, date
import io

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Arrow Travel Days Tracker", page_icon="✈️", layout="wide")

POLICY_START_DATE = datetime(2025, 9, 30)
POLICY_LIMIT_DAYS = 250

st.title("✈️ Arrow Travel Days Tracker")
st.caption("Keep track of how many days Arrow employees have traveled and how many are left in the 250-day policy year.")

# -----------------------------
# LOAD EMPLOYEE DATA
# -----------------------------
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("employees.csv")
    return df

uploaded_file = st.file_uploader("📤 Upload or update employees CSV", type=["csv"])
df = load_data(uploaded_file)

# Ensure correct columns
expected_cols = ["Employee", "Days Traveled", "Travel Start", "Travel End", "Route"]
if list(df.columns) != expected_cols:
    st.error(f"❌ CSV must have columns: {', '.join(expected_cols)}")
    st.stop()

# -----------------------------
# ADD NEW TRIP
# -----------------------------
st.subheader("➕ Add a new trip")
with st.form("add_trip"):
    new_emp = st.text_input("Employee Name")
    start_date = st.date_input("Travel Start Date")
    end_date = st.date_input("Travel End Date")
    route = st.text_input("Route (e.g. ATH-SIN-ATH)")
    submit = st.form_submit_button("Add Trip")

if submit:
    if new_emp and start_date and end_date:
        days_traveled = (end_date - start_date).days + 1
        new_row = {
            "Employee": new_emp,
            "Days Traveled": days_traveled,
            "Travel Start": start_date.strftime("%d/%m/%Y"),
            "Travel End": end_date.strftime("%d/%m/%Y"),
            "Route": route
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("employees.csv", index=False)
        st.success(f"✅ Trip added for {new_emp} ({days_traveled} days)")
        st.rerun()
    else:
        st.error("⚠️ Please fill all fields.")

# -----------------------------
# CALCULATIONS
# -----------------------------
df["Days Traveled"] = df["Days Traveled"].astype(int)
total_days = df["Days Traveled"].sum()
remaining_days = POLICY_LIMIT_DAYS - total_days
elapsed_days = (date.today() - POLICY_START_DATE.date()).days

# -----------------------------
# DISPLAY DASHBOARD
# -----------------------------
st.divider()
st.header("📊 Current Travel Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Days Used", f"{total_days} 🧳")
col2.metric("Days Remaining", f"{remaining_days} 🎯")
col3.metric("Days Since Policy Start", f"{elapsed_days} ⏳")

st.bar_chart(df.set_index("Employee")["Days Traveled"], use_container_width=True)

# -----------------------------
# DETAILS TABLE
# -----------------------------
st.subheader("👥 Employee Travel Log")
st.dataframe(df, use_container_width=True)

# -----------------------------
# DOWNLOAD UPDATED CSV
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("💾 Download Updated CSV", csv, "updated_travel_data.csv", "text/csv")
