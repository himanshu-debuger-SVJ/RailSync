import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="RailSync", layout="wide")

# ---------------- LIGHT THEME CSS ----------------


# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🚆 RailSync</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Railway Intelligence System</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SAMPLE DATA ----------------
train_data = {
    "train_number": 12423,
    "route": "Dibrugarh–New Delhi Rajdhani",
    "delay": 35,
    "previous": "Dibrugarh",
    "current": "Guwahati",
    "next": "Patna"
}

# ---------------- TOP SECTION ----------------
col1, col2, col3 = st.columns(3)

# Track Train
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔎 Track Your Train</div>", unsafe_allow_html=True)
    train_no = st.text_input("Train Number", "12423")
    st.markdown("</div>", unsafe_allow_html=True)

# Train Info
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<b>{train_data['train_number']}</b>", unsafe_allow_html=True)
    st.write(train_data["route"])
    st.markdown("<span class='badge badge-red'>Major Delay</span>", unsafe_allow_html=True)
    st.write(f"{train_data['delay']} min delay")
    st.markdown("</div>", unsafe_allow_html=True)

# Predictor
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>⏱ Delay Predictor</div>", unsafe_allow_html=True)

    route = st.selectbox("Route", [train_data["route"]], key="route1")

    if st.button("Predict Delay"):
        st.success("Prediction: Major Delay 🚨")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- LIVE + REROUTING ----------------
col4, col5 = st.columns(2)

# Live Train Status
with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📍 Live Train Status</div>", unsafe_allow_html=True)

    st.write(f"Previous Station: **{train_data['previous']}**")
    st.write(f"Current Station: **{train_data['current']}**")
    st.write(f"Next Station: **{train_data['next']}**")

    st.markdown("<span class='badge badge-red'>HEAVILY DELAYED</span>", unsafe_allow_html=True)

    st.markdown("### Journey Progress")
    stations = ["Dibrugarh", "Guwahati", "Patna", "Varanasi", "New Delhi"]

    for s in stations:
        if s == train_data["current"]:
            st.write(f"🔵 {s}")
        elif stations.index(s) < stations.index(train_data["current"]):
            st.write(f"✅ {s}")
        else:
            st.write(f"⚪ {s}")

    st.markdown("</div>", unsafe_allow_html=True)

# Smart Rerouting
with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔁 Smart Rerouting</div>", unsafe_allow_html=True)

    problem = st.text_area("Problem Description", "Track congestion near Guwahati")

    if st.button("Generate Suggestions"):
        st.success("Use alternate route via Barauni → Patna")
        st.info("Delay can be reduced by ~15 minutes")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAP ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🗺 Live Train Tracking</div>", unsafe_allow_html=True)

map_data = pd.DataFrame({
    "lat": [26.14],
    "lon": [91.73]
})

st.map(map_data)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📊 Operational Analytics</div>", unsafe_allow_html=True)

col6, col7 = st.columns(2)

with col6:
    st.write("Top Delayed Routes")
    routes = ["Mumbai–Guwahati", "Delhi–Guwahati", "Hyderabad–Guwahati"]
    delays = [80, 60, 70]
    st.bar_chart(pd.DataFrame({"Delay": delays}, index=routes))

with col7:
    st.write("Average Delay Over Time")
    time = list(range(24))
    values = np.random.randint(20, 80, size=24)
    st.line_chart(pd.DataFrame(values, index=time, columns=["Delay"]))

st.markdown("</div>", unsafe_allow_html=True)
