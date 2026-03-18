import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
import requests
import pydeck as pdk
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh



st.set_page_config(
    page_title="RED-ZONE SOC",
    layout="wide"
)

st.markdown(
"""
<h1 style='text-align:center;color:#00e5ff'>
🛡️ SOC Platform – Cyber Threat Monitoring
</h1>
<p style='text-align:center;color:gray'>
Real-time Security Operations Center Dashboard
</p>
""",
unsafe_allow_html=True
)

@st.cache_data
def load_data():

    data = {
        "time":["10:01","10:02","10:03","10:04","10:05","10:06"],

        "ip":[
            "192.168.1.1",
            "45.12.3.4",
            "10.0.0.1",
            "185.12.1.1",
            "172.16.0.5",
            "103.4.5.6"
        ],

        "country":[
            "Russia",
            "China",
            "USA",
            "Germany",
            "Russia",
            "China"
        ],

        "attack_type":[
            "Brute Force",
            "SQL Injection",
            "DDoS",
            "Brute Force",
            "Port Scan",
            "SQL Injection"
        ],

        "risk":[
            "High",
            "Critical",
            "Medium",
            "High",
            "Low",
            "Critical"
        ],

        "lat":[55,35,37,51,56,39],
        "lon":[37,103,-95,9,38,116]
    }

    df = pd.DataFrame(data)

    risk_map = {
        "Low":1,
        "Medium":2,
        "High":3,
        "Critical":4
    }

    df["risk_score"] = df["risk"].map(risk_map)

    return df


df = load_data()

# ======================
# SIDEBAR FILTERS
# ======================

with st.sidebar:

    st.title("🛡️ SOC Control")

    risk_filter = st.multiselect(
        "Filter Risk Level",
        df["risk"].unique(),
        default=df["risk"].unique()
    )

    attack_filter = st.multiselect(
        "Attack Type",
        df["attack_type"].unique(),
        default=df["attack_type"].unique()
    )

# ======================
# FILTER DATA
# ======================

df_view = df[
    (df["risk"].isin(risk_filter)) &
    (df["attack_type"].isin(attack_filter))
]

# ======================
# gen-att
# ======================
def generate_attack():
    attacks = ["Brute Force", "SQL Injection", "DDoS", "Port Scan"]

    countries = {
        "Russia": (61, 105),
        "China": (35, 104),
        "USA": (37, -95),
        "Germany": (51, 9)
    }

    country = random.choice(list(countries.keys()))
    lat, lon = countries[country]

    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "ip": f"185.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "country": country,
        "attack_type": random.choice(attacks),
        "risk": random.choice(["Low", "Medium", "High", "Critical"]),
        "lat": lat,
        "lon": lon
    }
if st.button("⚡ Generate Live Attack"):
    new_attack = generate_attack()
    df.loc[len(df)] = new_attack
    st.success(f"New attack from {new_attack['country']} ({new_attack['attack_type']})")

# ======================
# METRICS
# ======================

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Events", len(df_view))
m2.metric("Unique IPs", df_view["ip"].nunique())
m3.metric("Critical Alerts", len(df_view[df_view["risk"]=="Critical"]))
m4.metric("Top Attack", df_view["attack_type"].value_counts().idxmax())

# ======================
# MAP + PIE
# ======================

map_col, pie_col = st.columns([2,1])

with map_col:

    st.subheader("🌍 Global Threat Map")

    map_df = df_view.dropna(subset=["lat","lon"])

    fig = go.Figure()

    # نقاط الهجوم
    fig.add_trace(go.Scattergeo(
        lon=map_df["lon"],
        lat=map_df["lat"],
        hovertext=map_df["ip"],
        mode="markers",
        marker=dict(
            size=10,
            color="cyan",
            line=dict(width=1,color="white")
        )
    ))

    target_lon = 46.67
    target_lat = 24.71

    for _, r in map_df.iterrows():

        fig.add_trace(go.Scattergeo(
            lon=[r["lon"], target_lon],
            lat=[r["lat"], target_lat],
            mode="lines",
            line=dict(width=2,color="red"),
            opacity=0.7
        ))

    fig.update_geos(
        showcountries=True,
        showland=True,
        landcolor="#071726",
        showocean=True,
        oceancolor="#021024"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=0,r=0,t=0,b=0)
    )

    st.plotly_chart(
        fig,
        config={"displayModeBar": False},
        use_container_width=True,
        key="map_chart"
    )

with pie_col:

    st.subheader("📊 Attack Distribution")

    fig_pie = px.pie(
        df_view,
        names="attack_type",
        template="plotly_dark"
    )

    st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")


st.subheader("🌡 Threat Heatmap")

heatmap_data = df.groupby("country").size().reset_index(name="attacks")

fig_heat = px.choropleth(
    heatmap_data,
    locations="country",
    locationmode="country names",
    color="attacks",
    color_continuous_scale="Reds",
    title="Most Attacking Countries"
)

st.plotly_chart(fig_heat, use_container_width=True)

# ======================
# TIMELINE + ALERTS
# ======================

timeline_col, alert_col = st.columns([3,1])

with timeline_col:

    st.subheader("📈 Attack Timeline")

    fig_time = px.histogram(
        df_view,
        x="time",
        color="attack_type",
        template="plotly_dark"
    )

    fig_time.update_layout(height=350)

    st.plotly_chart(fig_time, use_container_width=True, key="timeline_chart")

with alert_col:

    st.subheader("🚨 Detection Alerts")

    counts = df_view["ip"].value_counts()

    for ip,count in counts.items():

        if count >= 2:

            st.warning(f"Possible attack from {ip}")

# ======================
# THREAT SCORE
# ======================

st.subheader("🔥 Threat Score by Country")

risk_score = {
    "Low":1,
    "Medium":2,
    "High":3,
    "Critical":4
}

df_view["threat_score"] = df_view["risk"].map(risk_score)

threat_score = df_view.groupby("country")["threat_score"].sum()

st.bar_chart(threat_score, use_container_width=True)

# ======================
# THREAT INTELLIGENCE
# ======================

st.subheader("🌐 Threat Intelligence Feed")

threat_data = {
"source":["AlienVault","AbuseIPDB","Spamhaus","MISP"],
"threat_level":["High","Medium","Critical","Medium"],
"ioc":["185.12.1.1","45.12.3.4","103.4.5.6","192.168.1.5"]
}

threat_df = pd.DataFrame(threat_data)

st.dataframe(threat_df,use_container_width=True, key="threat_feed")

# ======================
# MITRE MAPPING
# ======================

st.subheader("🧠 MITRE ATT&CK Mapping")

mitre_map = {
"Brute Force":"T1110",
"SQL Injection":"T1190",
"DDoS":"T1498",
"Port Scan":"Recon"
}

df_view["mitre"] = df_view["attack_type"].map(mitre_map)

st.dataframe(df_view[["ip","attack_type","mitre"]],use_container_width=True, key="mitre_table")

# ======================
# LOGS
# ======================

st.subheader("📄 Logs")

st.dataframe(df_view,use_container_width=True, key="logs_table")


st.subheader("⚡ Attack Simulator")

def simulate_attack():

    attacks = ["Brute Force","SQL Injection","DDoS","Port Scan"]

    countries = [
        ("Russia",55,37),
        ("China",35,103),
        ("USA",37,-95),
        ("Germany",51,9)
    ]

    attack = random.choice(attacks)
    country = random.choice(countries)

    risk = random.choice(["Low","Medium","High","Critical"])

    return {
        "time":"10:"+str(random.randint(10,59)),
        "ip":"192.168.1."+str(random.randint(10,200)),
        "country":country[0],
        "attack_type":attack,
        "risk":risk,
        "lat":country[1],
        "lon":country[2],
        "risk_score":{
            "Low":1,
            "Medium":2,
            "High":3,
            "Critical":4
        }[risk]
    }


if st.button("⚡ Simulate Attack"):

    new_attack = simulate_attack()

    df.loc[len(df)] = new_attack

    st.success(
        f"🚨 Attack from {new_attack['ip']} | {new_attack['country']} | {new_attack['attack_type']}"
    )

st.subheader("🔎 Investigate IP")

ip = st.selectbox(
"Select IP",
df["ip"].unique()
)

def check_ip(ip):

    url = f"http://ip-api.com/json/{ip}"

    try:

        r = requests.get(url, timeout=5)

        data = r.json()

        return data

    except:

        return {"error":"API connection failed"}


if st.button("Check Reputation"):

    result = check_ip(ip)

    st.json(result)

st.write("---")

st.caption(
"Developed by Abdulaziz Al-Khathami | SOC Platform Project"
)
