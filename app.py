import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib

# Load ML model + encoders
model = joblib.load("model.pkl")
le_start = joblib.load("le_start.pkl")
le_end = joblib.load("le_end.pkl")
le_traffic = joblib.load("le_traffic.pkl")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="RailSync Dashboard", layout="wide", initial_sidebar_state="collapsed")

# ---------------- LIGHT THEME & CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

body, .stApp {
    background-color: #111822; /* Deep dark blue background */
    color: #f8fafc;
}

/* Hide Streamlit elements */
[data-testid="stHeader"] {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp > header {background-color: transparent;}

/* Block padding overrides */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 1400px;
}

/* Titles */
.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.subtitle {
    color: #94a3b8;
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 24px;
}

/* Cards */
.card {
    background: #1e293b;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
    border: 1px solid #334155;
    margin-bottom: 24px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.2);
}

/* Section Headers inside Cards */
.card h3 {
    margin-top: 0;
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
    border-bottom: 1px solid #334155;
    padding-bottom: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Badges */
.badge {
    padding: 6px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-red { background-color: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-green { background-color: rgba(34, 197, 94, 0.2); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-blue { background-color: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3); }

/* Route Row styling */
.route-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: #0f172a;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid #334155;
    transition: background 0.2s ease;
}
.route-row:hover {
    background: #1e293b;
}
.route-name {
    font-weight: 500;
    color: #f1f5f9;
    font-size: 14px;
}

/* Streamlit Component Overrides */
div[data-baseweb="select"] > div {
    border-radius: 8px;
    border: 1px solid #334155;
    background-color: #0f172a;
}
input[data-baseweb="input"] {
    border-radius: 8px;
    border: 1px solid #334155;
    color: white !important;
}
div[data-baseweb="select"] * {
    color: white !important;
}
.stButton > button {
    background-color: #ffffff !important;
    color: #111822 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 6px -1px rgba(255, 255, 255, 0.1) !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #f1f5f9 !important;
    box-shadow: 0 6px 8px -1px rgba(255, 255, 255, 0.2) !important;
}

/* Top Stats */
.stat-box {
    background: #1e293b;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #334155;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    position: relative;
    overflow: hidden;
}
.stat-box::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background-color: #3b82f6;
    border-radius: 4px 0 0 4px;
}
.stat-box.red::before { background-color: #ef4444; }
.stat-box.green::before { background-color: #22c55e; }
.stat-box.orange::before { background-color: #f59e0b; }

.stat-value {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
}
.stat-label {
    font-size: 13px;
    color: #94a3b8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>🚆 RailSync</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Railway Traffic Intelligence & Smart Rerouting System</div>", unsafe_allow_html=True)

# ---------------- TOP STATS ROW ----------------
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown("""
        <div class='stat-box'>
            <div class='stat-value'>124</div>
            <div class='stat-label'>Active Trains</div>
        </div>
    """, unsafe_allow_html=True)
with metric_col2:
    st.markdown("""
        <div class='stat-box orange'>
            <div class='stat-value'>12</div>
            <div class='stat-label'>Delayed Trains</div>
        </div>
    """, unsafe_allow_html=True)
with metric_col3:
    st.markdown("""
        <div class='stat-box red'>
            <div class='stat-value'>3</div>
            <div class='stat-label'>Active Disruptions</div>
        </div>
    """, unsafe_allow_html=True)
with metric_col4:
    st.markdown("""
        <div class='stat-box green'>
            <div class='stat-value'>92%</div>
            <div class='stat-label'>On-Time Rate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- MAIN GRID LAYOUT ----------------
main_col1, main_col2 = st.columns([1, 2.2])  # Make map column slightly larger

with main_col1:
    # ---------------- DATE FILTER ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📅 Operation Target Date")
    selected_date = st.date_input("Simulation Date", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- TRAIN LINES / TRAFFIC ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🚦 Live Route Congestion")

    # Sample routes
    routes = [
        "Guwahati → Delhi",
        "Mumbai → Guwahati",
        "Chennai → Guwahati",
        "Kolkata → Guwahati",
        "Patna → Delhi"
    ]
    # Simulated traffic levels
    traffic_levels = ["High", "Medium", "Low", "Medium", "High"]

    traffic_html = ""
    for route, traffic in zip(routes, traffic_levels):
        if traffic == "High":
            badge = "<span class='badge badge-red'>Critical</span>"
        elif traffic == "Medium":
            badge = "<span class='badge badge-blue'>Moderate</span>"
        else:
            badge = "<span class='badge badge-green'>Optimal</span>"

        traffic_html += f"""
        <div class='route-row'>
            <div class='route-name'>🚄 {route}</div>
            <div>{badge}</div>
        </div>
        """
    st.markdown(traffic_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DISRUPTION INPUT ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ⚠️ Smart Rerouting")

    affected_route = st.selectbox("Select Affected Route", routes)
    issue_type = st.selectbox("Issue Type", ["Heavy Traffic", "Maintenance Block", "Flood", "Accident"])

    if "rerouting_active" not in st.session_state:
        st.session_state['rerouting_active'] = False
        st.session_state['affected_route'] = ""

    if st.button("Generate Alternate Route"):
        st.session_state['rerouting_active'] = True
        st.session_state['affected_route'] = affected_route

    if st.session_state['rerouting_active'] and st.session_state['affected_route'] == affected_route:
        st.markdown("<div style='margin-top: 15px;'>", unsafe_allow_html=True)
        # Rerouting logic
        if "Guwahati → Delhi" in affected_route:
            suggestion = "Barauni → Patna → Delhi"
            reduction = "20 mins"
            badge_color = "green"
        elif "Mumbai → Guwahati" in affected_route:
            suggestion = "Bhopal → Patna → Guwahati"
            reduction = "25 mins"
            badge_color = "green"
        else:
            suggestion = "Alternate parallel corridor"
            reduction = "15 mins"
            badge_color = "blue"

        st.success(f"**Route:** {suggestion}")
        st.info(f"**Saved Time:** {reduction}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with main_col2:
    # ---------------- MAP ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🗺 Network Traffic Visualization")

    # Station data (Pinpoint Cartesian X,Y percentage coordinates 0-1000 matched to the specific schematic map)
    stations = {
        "Dibrugarh": (910, 690),
        "Guwahati": (820, 640),
        "Patna": (640, 630),
        "Varanasi": (560, 590),
        "New Delhi": (435, 680),
        "Mumbai": (250, 410),
        "Kolkata": (740, 490),
        "Chennai": (490, 200),
        "Nagpur": (470, 470),
        "Barauni": (660, 630),
        "Bhopal": (430, 530),
        "New Jalpaiguri": (760, 620),
        "Malda Town": (720, 560),
        "Katihar": (700, 600),
        "Lumding": (860, 620),
        "Agartala": (880, 540),
        "Alipurduar Jn": (780, 640),
        "Rangiya": (800, 660),
        "Haldibari": (750, 630)
    }
    
    # Base Tracks
    tracks = [
        ("Guwahati", "Patna"),
        ("Patna", "Varanasi"),
        ("Varanasi", "New Delhi"),
        ("Mumbai", "Nagpur"),
        ("Nagpur", "Kolkata"),
        ("Kolkata", "Guwahati"),
        ("Chennai", "Kolkata"),
        ("Dibrugarh", "Guwahati"),
        ("Guwahati", "New Jalpaiguri"),
        ("New Jalpaiguri", "Malda Town"),
        ("Malda Town", "Kolkata"),
        ("Guwahati", "Lumding"),
        ("Lumding", "Agartala"),
        ("Katihar", "New Jalpaiguri"),
        ("Patna", "Katihar"),
        ("Rangiya", "Guwahati"),
        ("Alipurduar Jn", "New Jalpaiguri"),
        ("Rangiya", "Alipurduar Jn"),
        ("New Jalpaiguri", "Haldibari")
    ]
    
    # ---------------- ML-BASED TRAFFIC PREDICTION ----------------

    traffic_status = {}

    for (start, end) in tracks:
        try:
            # Encode stations
            start_enc = le_start.transform([start])[0]
            end_enc = le_end.transform([end])[0]

            # Dummy inputs (you can later connect UI inputs)
            hour = selected_date.hour if hasattr(selected_date, 'hour') else 12
            day = selected_date.day
            month = selected_date.month
            traffic_input = "medium"

            traffic_enc = le_traffic.transform([traffic_input])[0]

            features = [[start_enc, end_enc, hour, day, month, traffic_enc]]

            pred = model.predict(features)[0]

            # Convert prediction to traffic level
            if pred == 0:
                traffic_status[(start, end)] = "Low"
            elif pred == 1:
                traffic_status[(start, end)] = "Medium"
            else:
                traffic_status[(start, end)] = "High"

        except:
            traffic_status[(start, end)] = "Low"  # fallback
    
    
    color_map = {
        "Low": "#22c55e",
        "Medium": "#3b82f6",
        "High": "#ef4444"
    }

    # Rerouting logic for map updates
    active_reroutes = []
    affected_edges = []
    if getattr(st.session_state, 'rerouting_active', False):
        active_route = st.session_state['affected_route']
        if "Guwahati → Delhi" in active_route:
            affected_edges = [("Guwahati", "Patna"), ("Patna", "Varanasi")]
            active_reroutes = [("Guwahati", "Barauni"), ("Barauni", "Patna"), ("Patna", "New Delhi")]
        elif "Mumbai → Guwahati" in active_route:
            affected_edges = [("Mumbai", "Nagpur"), ("Nagpur", "Kolkata"), ("Kolkata", "Guwahati")]
            active_reroutes = [("Mumbai", "Bhopal"), ("Bhopal", "Patna"), ("Patna", "Guwahati")]
        elif "Chennai → Guwahati" in active_route:
            affected_edges = [("Chennai", "Kolkata"), ("Kolkata", "Guwahati")]
            active_reroutes = [("Chennai", "Nagpur"), ("Nagpur", "Patna"), ("Patna", "Guwahati")]
        elif "Kolkata → Guwahati" in active_route:
            affected_edges = [("Kolkata", "Guwahati")]
            active_reroutes = [("Kolkata", "Barauni"), ("Barauni", "Guwahati")]

    fig = go.Figure()

    # Draw regular connection lines
    for (start, end) in tracks:
        x1, y1 = stations[start]
        x2, y2 = stations[end]
        
        # Dimming color if it's currently affected by our simulated issue
        if (start, end) in affected_edges or (end, start) in affected_edges:
            color = "#94a3b8"  # Grey out affected line louder
            name = f"🚨 {start} → {end} (Disrupted)"
            width = 3
        else:
            traffic = traffic_status.get((start, end), "Low")
            color = color_map[traffic]
            name = f"{start} → {end} ({traffic})"
            width = 4

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(width=width, color=color),
            name=name,
            hoverinfo="name"
        ))
        
    # Draw reroute lines
    for (start, end) in active_reroutes:
        if start in stations and end in stations:
            x1, y1 = stations[start]
            x2, y2 = stations[end]
            fig.add_trace(go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(width=5, color="#a855f7", dash="dot"), # Purple dotted line for alternate route
                name=f"✅ Alternate: {start} → {end}",
                hoverinfo="name"
            ))

    xs = [coord[0] for coord in stations.values()]
    ys = [coord[1] for coord in stations.values()]
    names = list(stations.keys())

    # Draw stations
    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="markers+text",
        marker=dict(size=14, color="#1e293b", opacity=1.0, symbol="circle", line=dict(color="white", width=2)),
        text=names,
        textposition="top center",
        textfont=dict(family="Inter", size=14, color="#0f172a", weight="bold"),
        hoverinfo="text"
    ))

    # Add the static map image as background
    import base64
    import os
    
    if os.path.exists("india-rail-map.jpg"):
        with open("india-rail-map.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        fig.add_layout_image(
            dict(
                source=f"data:image/jpeg;base64,{encoded_string}",
                xref="x",
                yref="y",
                x=0,
                y=1000,
                sizex=1000,
                sizey=1000,
                sizing="stretch",
                opacity=0.7,
                layer="below"
            )
        )

    fig.update_layout(
        xaxis=dict(range=[0, 1000], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 1000], showgrid=False, zeroline=False, visible=False),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=700,  # Taller map to fit India well
        showlegend=False,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b'
    )

    st.plotly_chart(fig, use_container_width=True, key="main_map")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ANALYTICS ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Network Delay Analytics")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("<div style='font-size: 14px; font-weight: 500; color: #64748b; margin-bottom: 10px;'>Congestion Level Distribution</div>", unsafe_allow_html=True)
        chart1_fig = go.Figure(data=[go.Bar(
            x=["High", "Medium", "Low"],
            y=[12, 25, 63],
            marker_color=['#ef4444', '#3b82f6', '#22c55e'],
            text=[12, 25, 63], textposition='auto',
            textfont=dict(color='#ffffff')
        )])
        chart1_fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='#334155', tickfont=dict(color='#94a3b8'))
        )
        
    with col_chart2:
        st.markdown("<div style='font-size: 14px; font-weight: 500; color: #64748b; margin-bottom: 10px;'>Average Delay Over 24h (mins)</div>", unsafe_allow_html=True)
        time_ax = list(range(24))
        values_ax = [12, 10, 8, 15, 20, 35, 45, 60, 50, 40, 30, 25, 22, 18, 15, 10, 15, 30, 45, 55, 40, 25, 15, 10]
        chart2_fig = go.Figure(data=[go.Scatter(
            x=time_ax, y=values_ax,
            mode='lines+markers',
            line=dict(color='#ffffff', width=3),
            marker=dict(size=6, color='#ffffff')
        )])
        chart2_fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='#334155', tickfont=dict(color='#94a3b8'))
        )
        

    st.markdown("</div>", unsafe_allow_html=True)
