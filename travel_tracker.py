import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt
import os

# ---------------------
# CONFIGURATION
# ---------------------
POLICY_START = datetime(2025, 9, 30)
POLICY_LIMIT = 250
DATA_FILE = "trips_data.csv"
AUTHORIZED_EMAILS = [
    "info@chiinsurancebrokers.com",
    "sof@arrowship.com",
    "info@okto.gr",
    "lsm@arrowship.com",
    "oslaney@pulse-insurance.co.uk"
]

st.title("✈️ Arrow Travel Tracker 2025")

# ---------------------
# LOGIN
# ---------------------
user_email = st.text_input("Enter your email to access the dashboard:")
if user_email.lower() not in AUTHORIZED_EMAILS:
    st.warning("⚠️ Access restricted. Please use an authorized email.")
    st.stop()
else:
    st.success(f"Welcome {user_email}! 👋")

# ---------------------
# LOAD OR INITIALIZE DATA
# ---------------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, parse_dates=["Travel Start", "Travel End"])
else:
    df = pd.DataFrame(columns=["Employee", "Travel Start", "Travel End"])

# ---------------------
# ADD NEW TRIP INTERACTIVE FORM
# ---------------------
st.subheader("➕ Add a New Travel Trip")
with st.form("add_trip_form"):
    employee = st.text_input("Employee Name")
    start_date = st.date_input("Travel Start Date")
    end_date = st.date_input("Travel End Date")
    submitted = st.form_submit_button("Add Trip ✈️")
    
    if submitted:
        if start_date > end_date:
            st.error("Start date cannot be after end date!")
        elif not employee.strip():
            st.error("Please enter an employee name.")
        else:
            new_trip = pd.DataFrame({
                "Employee": [employee.strip()],
                "Travel Start": [pd.to_datetime(start_date)],
                "Travel End": [pd.to_datetime(end_date)]
            })
            df = pd.concat([df, new_trip], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Trip added for {employee} from {start_date} to {end_date} ✈️")

# ---------------------
# CALCULATE DAYS USED
# ---------------------
if not df.empty:
    df["Days"] = (df["Travel End"] - df["Travel Start"]).dt.days
    df_summary = df.groupby("Employee").agg({
        "Days": "sum",
        "Travel Start": lambda x: list(x.dt.strftime('%d/%m/%Y')),
        "Travel End": lambda x: list(x.dt.strftime('%d/%m/%Y'))
    }).reset_index()

    df_summary["Days Left"] = POLICY_LIMIT - df_summary["Days"]
    df_summary["Usage %"] = (df_summary["Days"] / POLICY_LIMIT * 100).clip(upper=100)
    df_summary["Close to Limit"] = df_summary["Days"] >= 200

    # ---------------------
    # DISPLAY DASHBOARD
    # ---------------------
    st.subheader(f"🗓 Policy Start Date: {POLICY_START.strftime('%d/%m/%Y')}")
    days_since_start = (datetime.today() - POLICY_START).days
    st.write(f"⏱ Days since policy start: **{days_since_start} days**")

    st.subheader("📋 Travel Summary")
    st.dataframe(df_summary, hide_index=True)

    # ---------------------
    # FUN VISUALIZATION
    # ---------------------
    st.subheader("📊 Usage Visual Chart")
    chart = alt.Chart(df_summary).mark_bar().encode(
        x=alt.X("Days", title="Days Used"),
        x2="Days Left",
        y=alt.Y("Employee", sort="-x"),
        color=alt.condition(
            alt.datum["Close to Limit"],
            alt.value("red"),
            alt.value("skyblue")
        ),
        tooltip=[
            alt.Tooltip("Employee"),
            alt.Tooltip("Days"),
            alt.Tooltip("Days Left"),
            alt.Tooltip("Usage %")
        ]
    ).properties(height=40 * len(df_summary))
    st.altair_chart(chart, use_container_width=True)

    # Display travel periods
    st.subheader("🗓 Travel Periods")
    for _, row in df_summary.iterrows():
        periods = [f"{start} ➡ {end}" for start, end in zip(row["Travel Start"], row["Travel End"])]
        st.markdown(f"**{row['Employee']}** ✈️ " + ", ".join(periods))
else:
    st.info("No travel trips added yet.")

st.markdown("---")
st.markdown("👨‍💼 *Developed for Arrow Shipping by CHI Insurance Brokers*")
