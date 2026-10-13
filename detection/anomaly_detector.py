import os
import joblib
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ============================================================
# DIGITAL IMMUNE SYSTEM
# ANOMALY DETECTION ENGINE
# ============================================================

DATA_FILE = os.path.join(
    "data",
    "system_metrics.csv"
)

MODEL_FILE = os.path.join(
    "models",
    "isolation_forest.pkl"
)

SCALER_FILE = os.path.join(
    "models",
    "scaler.pkl"
)

RESULTS_FILE = os.path.join(
    "data",
    "detection_results.csv"
)


# ============================================================
# FEATURES USED BY THE MACHINE LEARNING MODEL
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
# LOAD DATA
# ============================================================

def load_data():

    print("\nLoading monitoring data...")

    data = pd.read_csv(DATA_FILE)

    print(
        f"Records loaded: {len(data)}"
    )

    missing = [
        feature
        for feature in FEATURES
        if feature not in data.columns
    ]

    if missing:

        raise ValueError(
            f"Missing required features: {missing}"
        )

    return data


# ============================================================
# PREPARE FEATURES
# ============================================================

def prepare_features(data):

    print(
        f"Features used: {len(FEATURES)}"
    )

    X = data[FEATURES].copy()

    # Make sure everything is numeric
    X = X.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Replace invalid values
    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Fill missing values with column medians
    X = X.fillna(
        X.median()
    )

    return X


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model(X):

    print(
        "\nTraining Isolation Forest..."
    )

    # Standardize the features
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Isolation Forest
    model = IsolationForest(
        n_estimators=200,
        contamination=0.10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_scaled
    )

    print(
        "Model training completed."
    )

    return model, scaler


# ============================================================
# SAVE MODEL
# ============================================================

def save_model(model, scaler):

    os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_FILE
    )

    joblib.dump(
        scaler,
        SCALER_FILE
    )

    print(
        "\nModel saved to:"
    )

    print(
        MODEL_FILE
    )

    print(
        "\nScaler saved to:"
    )

    print(
        SCALER_FILE
    )


# ============================================================
# ANALYZE TRAINING DATA
# ============================================================

def analyze_data(
    data,
    X,
    model,
    scaler
):

    print(
        "\nAnalyzing observations..."
    )

    X_scaled = scaler.transform(
        X
    )

    predictions = model.predict(
        X_scaled
    )

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly

    data = data.copy()

    data["anomaly_status"] = np.where(
        predictions == -1,
        "ANOMALY",
        "NORMAL"
    )

    # --------------------------------------------------------
    # Calculate anomaly score
    # --------------------------------------------------------

    raw_scores = -model.score_samples(
        X_scaled
    )

    # Normalize approximately to 0-100
    minimum = raw_scores.min()
    maximum = raw_scores.max()

    if maximum > minimum:

        risk_scores = (
            (raw_scores - minimum)
            /
            (maximum - minimum)
        ) * 100

    else:

        risk_scores = np.zeros(
            len(raw_scores)
        )

    data["risk_score"] = np.round(
        risk_scores,
        2
    )

    # --------------------------------------------------------
    # Determine severity
    # --------------------------------------------------------

    def severity(score, status):

        if status == "NORMAL":

            return "NORMAL"

        if score >= 75:

            return "CRITICAL"

        if score >= 60:

            return "HIGH"

        if score >= 40:

            return "MEDIUM"

        return "LOW"

    data["severity"] = [
        severity(
            score,
            status
        )
        for score, status
        in zip(
            data["risk_score"],
            data["anomaly_status"]
        )
    ]

    return data


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(data):

    data.to_csv(
        RESULTS_FILE,
        index=False
    )

    print(
        "\nDetection results saved to:"
    )

    print(
        RESULTS_FILE
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(data):
    print("\n" + "=" * 70)
    print("              ANOMALY DETECTION SUMMARY")
    print("=" * 70)

    total = len(data)

    normal_count = (data["anomaly_status"] == "NORMAL").sum()
    anomaly_count = (data["anomaly_status"] == "ANOMALY").sum()

    print(f"\nTotal records:        {total:,}")
    print(f"Normal records:       {normal_count:,}")
    print(f"Anomalies detected:   {anomaly_count:,}")

    if total > 0:
        anomaly_percentage = (anomaly_count / total) * 100
        print(f"Anomaly percentage:   {anomaly_percentage:.2f}%")

    print("\n" + "-" * 70)
    print("SEVERITY DISTRIBUTION")
    print("-" * 70)

    severity_counts = data["severity"].value_counts()

    for severity in ["NORMAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        count = severity_counts.get(severity, 0)
        print(f"{severity:<12} {count:>8,}")

    print("\n" + "-" * 70)
    print("HIGHEST-RISK OBSERVATION")
    print("-" * 70)

    highest_risk = data.loc[data["risk_score"].idxmax()]

    print(f"Timestamp:       {highest_risk['timestamp']}")
    print(f"CPU usage:       {highest_risk['cpu_usage']:.1f}%")
    print(f"Memory usage:    {highest_risk['memory_usage']:.1f}%")
    print(f"Risk score:      {highest_risk['risk_score']:.2f}")
    print(f"Severity:        {highest_risk['severity']}")
    print(f"Status:          {highest_risk['anomaly_status']}")

    print("\n" + "-" * 70)
    print("TOP 10 HIGHEST-RISK OBSERVATIONS")
    print("-" * 70)

    columns = [
        "timestamp",
        "cpu_usage",
        "memory_usage",
        "risk_score",
        "severity",
        "anomaly_status"
    ]

    top_risks = data.nlargest(10, "risk_score")[columns].copy()

    print(
        top_risks.to_string(
            index=False,
            formatters={
                "cpu_usage": "{:.1f}".format,
                "memory_usage": "{:.1f}".format,
                "risk_score": "{:.2f}".format
            }
        )
    )

    print("\n" + "=" * 70)
    print("              ANOMALY DETECTION ENGINE READY")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        + "=" * 70
    )

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       ANOMALY DETECTION ENGINE"
    )

    print(
        "=" * 70
    )

    # Load monitoring data
    data = load_data()

    # Prepare ML features
    X = prepare_features(
        data
    )

    # Train model
    model, scaler = train_model(
        X
    )

    # Save model
    save_model(
        model,
        scaler
    )

    # Analyze observations
    results = analyze_data(
        data,
        X,
        model,
        scaler
    )

    # Save detection results
    save_results(
        results
    )

    # Display results
    display_results(
        results
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()