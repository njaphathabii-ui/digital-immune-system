import os
import time
import joblib
import pandas as pd
import numpy as np
from datetime import datetime


# ============================================================
# DIGITAL IMMUNE SYSTEM
# REAL-TIME DETECTION ENGINE
# ============================================================


# ============================================================
# FILE LOCATIONS
# ============================================================

MODEL_FILE = os.path.join(
    "models",
    "isolation_forest.pkl"
)

SCALER_FILE = os.path.join(
    "models",
    "scaler.pkl"
)

MONITORING_FILE = os.path.join(
    "data",
    "system_metrics.csv"
)

# IMPORTANT:
# This is the file used by the dashboard.
DETECTION_FILE = os.path.join(
    "data",
    "detection_results.csv"
)


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "process_count",
    "bytes_sent",
    "bytes_received",
    "packets_sent",
    "packets_received",
    "established_connections",
    "listening_connections",
    "other_connections"
]


# ============================================================
# DETECTION RESULT COLUMNS
# ============================================================

OUTPUT_COLUMNS = [
    "timestamp",
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "process_count",
    "bytes_sent",
    "bytes_received",
    "packets_sent",
    "packets_received",
    "established_connections",
    "listening_connections",
    "other_connections",
    "anomaly_status",
    "risk_score",
    "severity"
]


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not os.path.exists(MODEL_FILE):

        raise FileNotFoundError(
            "Isolation Forest model not found.\n"
            "Run:\n"
            "python detection\\anomaly_detector.py"
        )

    if not os.path.exists(SCALER_FILE):

        raise FileNotFoundError(
            "Scaler not found.\n"
            "Run:\n"
            "python detection\\anomaly_detector.py"
        )

    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)

    return model, scaler


# ============================================================
# LOAD MONITORING DATA
# ============================================================

def load_monitoring_data():

    if not os.path.exists(MONITORING_FILE):

        raise FileNotFoundError(
            f"Monitoring file not found:\n"
            f"{MONITORING_FILE}"
        )

    data = pd.read_csv(MONITORING_FILE)

    if data.empty:

        raise ValueError(
            "Monitoring dataset is empty."
        )

    # Make sure all required features exist
    missing = [
        feature
        for feature in FEATURES
        if feature not in data.columns
    ]

    if missing:

        raise ValueError(
            f"Missing monitoring features: {missing}"
        )

    return data


# ============================================================
# CALCULATE RISK
# ============================================================

def calculate_risk(anomaly_score):

    reference_min = -0.5
    reference_max = 0.5

    normalized = (
        (anomaly_score - reference_min)
        /
        (reference_max - reference_min)
    )

    normalized = np.clip(
        normalized,
        0,
        1
    )

    risk = (1 - normalized) * 100

    return round(risk, 2)


# ============================================================
# DETERMINE SEVERITY
# ============================================================

def determine_severity(
    risk_score,
    prediction
):

    # Isolation Forest:
    # 1  = normal
    # -1 = anomaly

    if prediction == 1:
        return "NORMAL"

    if risk_score < 30:
        return "LOW"

    elif risk_score < 60:
        return "MEDIUM"

    elif risk_score < 80:
        return "HIGH"

    else:
        return "CRITICAL"


# ============================================================
# FIND TOP INDICATORS
# ============================================================

def find_indicators(
    record,
    data
):

    indicators = []

    for feature in FEATURES:

        values = pd.to_numeric(
            data[feature],
            errors="coerce"
        )

        mean = values.mean()
        std = values.std()

        if std == 0 or pd.isna(std):

            z_score = 0

        else:

            z_score = (
                float(record[feature]) - mean
            ) / std

        indicators.append(
            (
                feature,
                abs(z_score),
                z_score
            )
        )

    indicators.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return indicators[:3]


# ============================================================
# DETECT ANOMALY
# ============================================================

def detect(
    model,
    scaler,
    record
):

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in record.index
    ]

    if missing_features:

        raise ValueError(
            f"Missing features: {missing_features}"
        )

    # Keep feature names.
    # This prevents the sklearn warning.

    values = pd.DataFrame(
        [[
            record[feature]
            for feature in FEATURES
        ]],
        columns=FEATURES
    )

    values = values.astype(float)

    # Scale the observation

    scaled = scaler.transform(values)

    # Isolation Forest prediction

    prediction = model.predict(
        scaled
    )[0]

    decision_score = model.decision_function(
        scaled
    )[0]

    # Higher value = more anomalous

    anomaly_score = -decision_score

    # Calculate risk

    risk_score = calculate_risk(
        anomaly_score
    )

    # Determine severity

    severity = determine_severity(
        risk_score,
        prediction
    )

    return {
        "prediction": prediction,
        "anomaly_score": anomaly_score,
        "risk_score": risk_score,
        "severity": severity
    }


# ============================================================
# SAVE DETECTION RESULT
# ============================================================

def save_detection(
    record,
    result,
    indicators
):

    os.makedirs("data", exist_ok=True)

    status = (
        "NORMAL"
        if result["prediction"] == 1
        else "ANOMALY"
    )

    output = {
        "timestamp": datetime.now().isoformat()
    }

    # --------------------------------------------------------
    # System monitoring features
    # --------------------------------------------------------

    for feature in FEATURES:
        output[feature] = float(record[feature])

    # --------------------------------------------------------
    # Detection results
    # --------------------------------------------------------

    output["anomaly_status"] = status
    output["risk_score"] = float(
        result["risk_score"]
    )
    output["severity"] = result["severity"]

    # --------------------------------------------------------
    # Fixed 15-column schema
    # --------------------------------------------------------

    columns = [
        "timestamp",
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "process_count",
        "bytes_sent",
        "bytes_received",
        "packets_sent",
        "packets_received",
        "established_connections",
        "listening_connections",
        "other_connections",
        "anomaly_status",
        "risk_score",
        "severity"
    ]

    dataframe = pd.DataFrame(
        [[output[column] for column in columns]],
        columns=columns
    )

    dataframe.to_csv(
        DETECTION_FILE,
        mode="a",
        header=False,
        index=False
    )

# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(
    record,
    result,
    indicators
):

    status = (
        "NORMAL"
        if result["prediction"] == 1
        else "ANOMALY"
    )

    print("\n" + "=" * 65)

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       REAL-TIME DETECTION"
    )

    print("=" * 65)

    print(
        f"Time       : "
        f"{record['timestamp']}"
    )

    print(
        f"CPU        : "
        f"{float(record['cpu_usage']):.2f}%"
    )

    print(
        f"Memory     : "
        f"{float(record['memory_usage']):.2f}%"
    )

    print(
        f"Disk       : "
        f"{float(record['disk_usage']):.2f}%"
    )

    print(
        f"Processes  : "
        f"{int(record['process_count'])}"
    )

    print(
        f"Status     : "
        f"{status}"
    )

    print(
        f"Risk Score : "
        f"{result['risk_score']:.2f}/100"
    )

    print(
        f"Severity   : "
        f"{result['severity']}"
    )

    print(
        "\nTop indicators:"
    )

    for feature, _, z_score in indicators:

        print(
            f"  • {feature}: "
            f"{z_score:.2f}σ"
        )

    if status == "ANOMALY":

        print(
            "\n🚨 ANOMALY DETECTED"
        )

    else:

        print(
            "\n✓ System behaviour appears normal."
        )

    print("=" * 65)


# ============================================================
# REAL-TIME ENGINE
# ============================================================

def main():

    print("\n" + "=" * 65)

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       REAL-TIME DETECTION ENGINE"
    )

    print("=" * 65)

    print(
        "\nLoading trained model..."
    )

    model, scaler = load_model()

    print(
        "✓ Isolation Forest loaded."
    )

    print(
        "✓ Scaler loaded."
    )

    print(
        "\nMonitoring every 5 seconds."
    )

    print(
        "Waiting for NEW monitoring records..."
    )

    print(
        "Results will be written to:"
    )

    print(
        f"  {DETECTION_FILE}"
    )

    print(
        "\nPress CTRL+C to stop."
    )

    # --------------------------------------------------------
    # Remember the last record processed.
    # --------------------------------------------------------

    last_processed_record = None

    try:

        while True:

            data = load_monitoring_data()

            # Get newest monitoring record

            record = data.iloc[-1]

            # Create unique fingerprint

            current_record = tuple(
                record[FEATURES]
                .astype(float)
                .round(6)
            )

            # ------------------------------------------------
            # Only process a NEW monitoring record
            # ------------------------------------------------

            if current_record != last_processed_record:

                result = detect(
                    model,
                    scaler,
                    record
                )

                indicators = find_indicators(
                    record,
                    data
                )

                display_result(
                    record,
                    result,
                    indicators
                )

                # SAVE TO detection_results.csv

                save_detection(
                    record,
                    result,
                    indicators
                )

                print(
                    f"✓ Detection saved to: "
                    f"{DETECTION_FILE}"
                )

                # Remember record

                last_processed_record = (
                    current_record
                )

            time.sleep(5)

    except KeyboardInterrupt:

        print(
            "\n\nReal-time monitoring stopped."
        )

        print(
            "Digital Immune System shut down safely."
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()