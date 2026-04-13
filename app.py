import streamlit as st
import pandas as pd
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="RailSync", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

# ---------------- CUSTOM STYLE ----------------
st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    h1, h2, h3 {color: #ffffff;}
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align: center;'>🚆 RailSync: Smart Railway Intelligence System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Predict • Track • Optimize Train Operations</p>",
    unsafe_allow_html=True
)

# ---------------- TRAIN SELECTION ----------------
st.markdown("### 🔎 Track Your Train")

train_numbers = df["train_number"].unique()
train_no = st.selectbox("Select Train Number", train_numbers)

train_data = df[df["train_number"] == train_no].iloc[0]
route = train_data["route"]
delay = train_data["delay_minutes"]

# ---------------- KPI CARDS ----------------
st.markdown("### 📊 RailSync Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("🚆 Train No", train_no)
col2.metric("📍 Route", route)
col3.metric("⏱ Delay (min)", delay)

# ---------------- STATUS ----------------
st.markdown("---")
st.subheader("📌 Live Status")

if delay <= 5:
    st.success("✅ Running On Time")
elif delay <= 30:
    st.warning("⚠️ Slight Delay")
else:
    st.error("🚨 Major Delay")

# ---------------- MAP TRACKING ----------------
st.markdown("---")
st.subheader("🗺️ Live Train Tracking")

route_coords = {
    "Dibrugarh–New Delhi Rajdhani": [(27.47, 94.91), (25.31, 82.97), (28.61, 77.20)],
    "Kamrup Express (Howrah–Dibrugarh)": [(22.57, 88.36), (25.31, 82.97), (27.47, 94.91)],
    "Guwahati–Delhi Express": [(26.14, 91.73), (25.31, 82.97), (28.61, 77.20)]
}

coords = route_coords.get(route, [(26.14, 91.73)])

if st.button("▶️ Start Tracking"):

    st.info("🚆 RailSync tracking in progress...")

    map_placeholder = st.empty()

    for point in coords:
        map_data = pd.DataFrame({
            "lat": [point[0]],
            "lon": [point[1]]
        })

        map_placeholder.map(map_data)
        time.sleep(1)

# ---------------- SMART REROUTING ----------------
st.markdown("---")
st.subheader("🚦 RailSync Smart Rerouting")

avg_delay = df.groupby("route")["delay_minutes"].mean()[route]

st.write(f"📊 Average Delay: {avg_delay:.2f} minutes")

if avg_delay > 40:
    st.error("🚨 High Congestion Detected")
    st.success("🔄 RailSync Suggestion: Full Rerouting Recommended")

elif avg_delay > 20:
    st.warning("⚠️ Moderate Congestion")

    st.write("### 🔄 RailSync Optimization Suggestions")
    st.info("🕒 Adjust departure timing by 30–60 minutes")
    st.info("🚄 Optimize speed in low-traffic zones")
    st.info("🔀 Apply partial rerouting")
    st.info("🚉 Use alternate platforms at major stations")

else:
    st.success("✅ Route is Operating Efficiently")

# ---------------- ANALYTICS ----------------
st.markdown("---")
st.subheader("📊 RailSync Analytics: Top Delayed Routes")

top_routes = df.groupby("route")["delay_minutes"].mean().sort_values(ascending=False).head(5)
st.bar_chart(top_routes)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>🚆 RailSync | AI-Powered Railway Optimization System</p>",
    unsafe_allow_html=True
)