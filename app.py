import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="RailSync", layout="wide")

# ---------------- LIGHT THEME ----------------
st.markdown("""
<style>
body, .stApp {
    background-color: #f4f6fb;
    color: #111827;
}

/* Titles */
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #111827;
}
.subtitle {
    color: #4b5563;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* Labels */
.label {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 5px;
}

/* Badges */
.badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    color: white;
}
.badge-red { background-color: #ef4444; }
.badge-green { background-color: #22c55e; }
.badge-blue { background-color: #3b82f6; }

/* Button */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🚆 RailSync</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Railway Intelligence System</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- DATA ----------------
train_list = ["12423 Rajdhani", "12505 North East Express", "15646 Guwahati Mumbai"]
stations = ["Dibrugarh", "Guwahati", "Patna", "Varanasi", "New Delhi"]

route_stations = [
    ("Dibrugarh", 27.47, 94.91),
    ("Guwahati", 26.14, 91.73),
    ("Patna", 25.60, 85.14),
    ("Varanasi", 25.32, 82.97),
    ("New Delhi", 28.61, 77.20)
]

# ---------------- FORM ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🚆 Track Your Train")

col1, col2, col3 = st.columns(3)

# Train Number Dropdown
with col1:
    st.markdown("<div class='label'>Train Number</div>", unsafe_allow_html=True)
    train_no = st.selectbox("", train_list, key="train")

# Date Picker
with col2:
    st.markdown("<div class='label'>Date</div>", unsafe_allow_html=True)
    journey_date = st.date_input("", key="date")

# Station Dropdown
with col3:
    st.markdown("<div class='label'>Current Station</div>", unsafe_allow_html=True)
    current_station_input = st.selectbox("", stations, key="station")

track_btn = st.button("🔍 Track Train")

# ---------------- TRACKING ----------------
if track_btn:
    station_names = [s[0] for s in route_stations]
    idx = station_names.index(current_station_input)

    current_station = route_stations[idx]
    next_station = route_stations[min(idx+1, len(route_stations)-1)]

    lat = (current_station[1] + next_station[1]) / 2
    lon = (current_station[2] + next_station[2]) / 2

    delay = np.random.randint(5, 60)

    st.markdown("---")
    st.write(f"### 🚆 {train_no} Live Status")
    st.write(f"📍 Current: **{current_station[0]}**")
    st.write(f"➡️ Next: **{next_station[0]}**")
    st.write(f"⏱ Delay: **{delay} mins**")

    if delay > 30:
        st.markdown("<span class='badge badge-red'>HEAVILY DELAYED</span>", unsafe_allow_html=True)
    elif delay > 10:
        st.markdown("<span class='badge badge-blue'>SLIGHT DELAY</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge badge-green'>ON TIME</span>", unsafe_allow_html=True)

    st.markdown("### 🗺 Live Train Location")

    map_data = pd.DataFrame({
        "lat": [lat],
        "lon": [lon]
    })

    st.map(map_data)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- REROUTING ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🔁 Smart Rerouting")

problem = st.text_area("Problem Description", "Track congestion near Guwahati")

if st.button("Generate Suggestions"):
    st.success("Use alternate route via Barauni → Patna")
    st.info("Delay can be reduced by ~15 minutes")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 📊 Analytics")

col4, col5 = st.columns(2)

with col4:
    st.write("Top Delayed Routes")
    routes = ["Mumbai–Guwahati", "Delhi–Guwahati", "Hyderabad–Guwahati"]
    delays = [80, 60, 70]
    st.bar_chart(pd.DataFrame({"Delay": delays}, index=routes))

with col5:
    st.write("Average Delay")
    time = list(range(24))
    values = np.random.randint(20, 80, size=24)
    st.line_chart(pd.DataFrame(values, index=time, columns=["Delay"]))

st.markdown("</div>", unsafe_allow_html=True)
