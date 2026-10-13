import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

# ============================================================
# DIGITAL IMMUNE SYSTEM - LIVE DASHBOARD
# ============================================================

st.set_page_config(
    page_title="Digital Immune System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# FILE LOCATIONS
# ============================================================

SYSTEM_FILE = "data/system_metrics.csv"
DETECTION_FILE = "data/detection_results.csv"

# ============================================================
# AUTO REFRESH
# ============================================================

REFRESH_SECONDS = 5

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
    }

    .status-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .normal {
        background-color: #123d22;
        color: #66ff99;
        border: 2px solid #28a745;
    }

    .anomaly {
        background-color: #4a1111;
        color: #ff6666;
        border: 2px solid #dc3545;
    }

    .metric-title {
        font-size: 15px;
        font-weight: bold;
    }

    .small-text {
        font-size: 13px;
    }

    .response-panel {
        padding: 14px 18px;
        border-radius: 10px;
        margin-top: 4px;
        margin-bottom: 18px;
        border: 1px solid #3a3f49;
        background-color: #171a21;
    }

    .response-header {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .response-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }

    .response-card {
        padding: 11px 13px;
        border-radius: 7px;
        background-color: #20242d;
        border: 1px solid #343945;
        min-height: 58px;
    }

    .response-label {
        font-size: 11px;
        opacity: 0.75;
        margin-bottom: 5px;
    }

    .response-value {
        font-size: 16px;
        font-weight: 700;
    }

    .response-normal {
        border-left: 4px solid #28a745;
    }

    .response-medium {
        border-left: 4px solid #ffc107;
    }

    .response-high {
        border-left: 4px solid #fd7e14;
    }

    .response-critical {
        border-left: 4px solid #dc3545;
    }

    @media (max-width: 900px) {
        .response-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 600px) {
        .response-grid {
            grid-template-columns: 1fr;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🦇BATMANS </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">REAL-TIME CYBERSECURITY MONITORING & THREAT DETECTION SYSTEM</div>',
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

def load_system_data():

    if not os.path.exists(SYSTEM_FILE):
        return None

    try:
        data = pd.read_csv(SYSTEM_FILE)

        if data.empty:
            return None

        return data

    except Exception:
        return None


def load_detection_data():

    if not os.path.exists(DETECTION_FILE):
        return None

    try:
        data = pd.read_csv(DETECTION_FILE)

        if data.empty:
            return None

        return data

    except Exception:
        return None


system_data = load_system_data()
detection_data = load_detection_data()

# ============================================================
# NO DATA MESSAGE
# ============================================================

if system_data is None:

    st.warning(
        "No monitoring data available yet!! "
        "Start Terminal 1 system monitoring."
    )

    time.sleep(REFRESH_SECONDS)
    st.rerun()


# ============================================================
# LATEST SYSTEM RECORD
# ============================================================

latest_system = system_data.iloc[-1]

cpu = float(latest_system["cpu_usage"])
memory = float(latest_system["memory_usage"])
disk = float(latest_system["disk_usage"])
processes = int(latest_system["process_count"])

timestamp = latest_system["timestamp"]

# ============================================================
# LATEST DETECTION
# ============================================================

latest_detection = None

if detection_data is not None:

    latest_detection = detection_data.iloc[-1]

# ============================================================
# DETECTION STATUS
# ============================================================

if latest_detection is not None:

    status = str(
        latest_detection.get(
            "anomaly_status",
            "NORMAL"
        )
    ).upper()

    risk_score = float(
        latest_detection.get(
            "risk_score",
            0
        )
    )

    severity = str(
        latest_detection.get(
            "severity",
            "NORMAL"
        )
    ).upper()

else:

    status = "NORMAL"
    risk_score = 0
    severity = "NORMAL"


# ============================================================
# INTELLIGENT RESPONSE STATUS
# ============================================================

if severity == "CRITICAL":
    response_action = "SIMULATED_CONTAINMENT_AND_EVIDENCE"
    response_state = "CRITICAL RESPONSE ACTIVE"
    response_class = "response-critical"
elif severity == "HIGH":
    response_action = "SIMULATED_CONTAINMENT"
    response_state = "HIGH-RISK RESPONSE ACTIVE"
    response_class = "response-high"
elif severity == "MEDIUM":
    response_action = "ALERT"
    response_state = "MEDIUM-RISK ALERT ACTIVE"
    response_class = "response-medium"
elif severity == "LOW":
    response_action = "LOG"
    response_state = "LOW-RISK EVENT LOGGED"
    response_class = "response-medium"
else:
    response_action = "LOG_ONLY"
    response_state = "SYSTEM NORMAL"
    response_class = "response-normal"


# ============================================================
# TOP STATUS
# ============================================================

if status == "ANOMALY":

    st.markdown(
        f"""
        <div class="status-box anomaly">
            🚨 ANOMALY DETECTED
            <br>
            <span style="font-size:18px;">
                Threat activity requires attention
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="status-box normal">
            🟢 SYSTEM OPERATING NORMALLY
            <br>
            <span style="font-size:18px;">
                No active threat detected
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LIVE SECURITY METRICS
# ============================================================

st.subheader("🚨 Current Security Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Risk Score",
        f"{risk_score:.2f}/100"
    )

with col2:
    st.metric(
        "Severity",
        severity
    )

with col3:
    st.metric(
        "Status",
        status
    )

with col4:
    st.metric(
        "Last Update",
        timestamp
    )


# ============================================================
# INTELLIGENT RESPONSE
# ============================================================

st.subheader("🛡️ Intelligent Response")

st.markdown(
    f'''
    <div class="response-panel {response_class}">
        <div class="response-header">{response_state}</div>
        <div class="response-grid">
            <div class="response-card">
                <div class="response-label">CURRENT SEVERITY</div>
                <div class="response-value">{severity}</div>
            </div>
            <div class="response-card">
                <div class="response-label">RISK SCORE</div>
                <div class="response-value">{risk_score:.2f}/100</div>
            </div>
            <div class="response-card">
                <div class="response-label">SYSTEM STATUS</div>
                <div class="response-value">{status}</div>
            </div>
            <div class="response-card">
                <div class="response-label">AUTOMATED RESPONSE</div>
                <div class="response-value">{response_action}</div>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)


# ============================================================
# SYSTEM RESOURCES
# ============================================================

st.subheader("Live System Resources")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "CPU Usage",
        f"{cpu:.1f}%"
    )

with col2:
    st.metric(
        "Memory Usage",
        f"{memory:.1f}%"
    )

with col3:
    st.metric(
        "Disk Usage",
        f"{disk:.1f}%"
    )

with col4:
    st.metric(
        "Running Processes",
        f"{processes}"
    )


# ============================================================
# LATEST THREAT INFORMATION
# ============================================================

if latest_detection is not None:

    st.subheader("Latest Detection")

    if status == "ANOMALY":

        st.error(
            f"🚨 Anomaly detected | "
            f"Risk Score: {risk_score:.2f}/100 | "
            f"Severity: {severity}"
        )

    else:

        st.success(
            f"✓ No active threat detected | "
            f"Risk Score: {risk_score:.2f}/100"
        )

    # Indicators
    if "indicators" in latest_detection.index:

        indicators = latest_detection["indicators"]

        if pd.notna(indicators):

            st.write("**Top Indicators:**")

            st.code(str(indicators))


# ============================================================
# LIVE GRAPHS
# ============================================================

st.subheader("📈 Live System Activity")

graph_data = system_data.tail(50).copy()

if not graph_data.empty:

    graph_data["timestamp"] = pd.to_datetime(
        graph_data["timestamp"]
    )

    chart_data = graph_data.set_index("timestamp")

    available_columns = []

    for column in [
        "cpu_usage",
        "memory_usage",
        "disk_usage"
    ]:

        if column in chart_data.columns:
            available_columns.append(column)

    if available_columns:

        st.line_chart(
            chart_data[available_columns]
        )


# ============================================================
# RECENT DETECTIONS
# ============================================================

st.subheader("🚨 Recent Detection History")

if detection_data is not None and not detection_data.empty:

    recent = detection_data.tail(10).copy()

    display_columns = [
        "timestamp",
        "risk_score",
        "severity",
        "anomaly_status"
    ]

    display_columns = [
        column
        for column in display_columns
        if column in recent.columns
    ]

    st.dataframe(
        recent[display_columns].iloc[::-1],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No detection results available yet.")


# ============================================================
# SYSTEM STATISTICS
# ============================================================

st.subheader("📊 Monitoring Statistics")

total_records = len(system_data)

if detection_data is not None:

    total_detections = len(detection_data)

    if "anomaly_status" in detection_data.columns:

        anomaly_count = (
            detection_data["anomaly_status"]
            .astype(str)
            .str.upper()
            .eq("ANOMALY")
            .sum()
        )

    else:

        anomaly_count = 0

else:

    total_detections = 0
    anomaly_count = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Monitoring Records",
        total_records
    )

with col2:
    st.metric(
        "Detection Records",
        total_detections
    )

with col3:
    st.metric(
        "Detected Anomalies",
        anomaly_count
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    f"Digital Immune System | "
    f"Last dashboard refresh: {datetime.now().strftime('%H:%M:%S')}"
)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(REFRESH_SECONDS)
st.rerun()