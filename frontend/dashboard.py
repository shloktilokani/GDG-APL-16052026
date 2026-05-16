import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import json

st.set_page_config(
    page_title="IPL Live Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    body { background-color: #0e1117; color: white; }
    .stMetric label { color: #cccccc !important; }
</style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Live Match Dashboard")
st.markdown("---")

r1_col1, r1_col2, r1_col3 = st.columns([1, 1, 2])
score_ph = r1_col1.empty()
over_ph = r1_col2.empty()
context_ph = r1_col3.empty()

st.markdown("---")

r2_col1, r2_col2 = st.columns(2)
prob_ph = r2_col1.empty()
momentum_ph = r2_col2.empty()

st.markdown("---")

r3_col1, r3_col2, r3_col3 = st.columns(3)
matchup_ph = r3_col1.empty()
donut_ph = r3_col2.empty()
phase_ph = r3_col3.empty()

st.markdown("---")

r4_col1, r4_col2 = st.columns(2)
batter_impact_ph = r4_col1.empty()
bowler_impact_ph = r4_col2.empty()

API_URL = "http://127.0.0.1:5000/get_analytics"

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=1)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def build_highcharts_html(chart_id, config):
    return f"""
    <style>
        body {{
            background-color: #0e1117;
            margin: 0;
            padding: 0;
            color: white;
            overflow: hidden;
        }}
    </style>
    <div id="{chart_id}" style="width:100%; height:100%; min-height: 350px;"></div>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            Highcharts.chart('{chart_id}', {json.dumps(config)});
        }});
    </script>
    """

while True:
    data = fetch_data()
    
    if data and "live_summary" in data:
        summary = data["live_summary"]
        analytics = data["analytics"]
        
        with score_ph.container():
            st.metric("Score", summary["score"])
        with over_ph.container():
            st.metric("Over", summary["over"])
        with context_ph.container():
            st.info(f"Batting: {summary['batter']} | Bowling: {summary['bowler']}")
            
        prob = analytics["win_probability"]
        prob_hist = analytics.get("win_probability_history", [])
        prob_config = {
            "chart": {"type": "spline", "backgroundColor": "transparent"},
            "title": {"text": "Live Win Probability", "style": {"color": "#fff"}},
            "xAxis": {"title": {"text": "Over", "style": {"color": "#fff"}}, "labels": {"style": {"color": "#fff"}}},
            "yAxis": {"min": 0, "max": 100, "title": {"text": "Win Prob %", "style": {"color": "#fff"}}, "labels": {"style": {"color": "#fff"}}},
            "series": [
                {"name": "Batting Team", "data": prob_hist, "color": "#00ffcc"}
            ],
            "credits": {"enabled": False}
        }
        with prob_ph.container():
            components.html(build_highcharts_html("prob_chart", prob_config), height=360)
            
        momentum = analytics["momentum_history"]
        mom_config = {
            "chart": {"type": "area", "backgroundColor": "transparent"},
            "title": {"text": "Momentum Wave", "style": {"color": "#fff"}},
            "xAxis": {"title": {"text": "Over", "style": {"color": "#fff"}}, "labels": {"style": {"color": "#fff"}}},
            "yAxis": {"title": {"text": "Momentum Score", "style": {"color": "#fff"}}, "labels": {"style": {"color": "#fff"}}},
            "series": [{"name": "Momentum", "data": momentum, "color": "#ffcc00"}],
            "credits": {"enabled": False}
        }
        with momentum_ph.container():
            components.html(build_highcharts_html("mom_chart", mom_config), height=360)
            
        status = analytics["matchup_status"]
        color = "#00e676" if status == "Dominating" else "#ff1744" if status == "Struggling" else "#ffea00"
        with matchup_ph.container():
            st.markdown(f"### Matchup Status<br/><h1 style='color:{color};'>{status}</h1>", unsafe_allow_html=True)
            
        dist = analytics["boundary_dot_distribution"]
        donut_config = {
            "chart": {"type": "pie", "backgroundColor": "transparent"},
            "title": {"text": "Boundary vs Dots", "style": {"color": "#fff"}},
            "plotOptions": {"pie": {"innerSize": "60%", "dataLabels": {"enabled": False}}},
            "series": [{
                "name": "Percentage",
                "data": [
                    {"name": "Dots", "y": dist["dots"], "color": "#666666"},
                    {"name": "Singles", "y": dist["singles"], "color": "#aaaaaa"},
                    {"name": "Boundaries", "y": dist["boundaries"], "color": "#00e676"}
                ]
            }],
            "credits": {"enabled": False}
        }
        with donut_ph.container():
            components.html(build_highcharts_html("donut_chart", donut_config), height=300)
            
        phases = analytics["phase_performance"]
        phase_config = {
            "chart": {"type": "column", "backgroundColor": "transparent"},
            "title": {"text": "Phase Performance", "style": {"color": "#fff"}},
            "xAxis": {"categories": ["Powerplay", "Middle", "Death"], "labels": {"style": {"color": "#fff"}}},
            "yAxis": {"title": {"text": "Runs", "style": {"color": "#fff"}}, "labels": {"style": {"color": "#fff"}}},
            "series": [{
                "name": "Runs",
                "data": [phases["powerplay"]["runs"], phases["middle_overs"]["runs"], phases["death_overs"]["runs"]],
                "color": "#33b5e5"
            }],
            "credits": {"enabled": False}
        }
        with phase_ph.container():
            components.html(build_highcharts_html("phase_chart", phase_config), height=300)
            
        impact = analytics["player_impact"]
        with batter_impact_ph.container():
            st.metric(f"Batter Impact: {summary['batter']}", impact["batter_score"])
        with bowler_impact_ph.container():
            st.metric(f"Bowler Impact: {summary['bowler']}", impact["bowler_score"])
            
    else:
        with score_ph.container():
            st.warning("Waiting for simulation data... Ensure generator.py and app.py are running.")
            
    time.sleep(2)
