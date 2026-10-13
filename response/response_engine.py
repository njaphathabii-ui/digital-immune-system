import pandas as pd
import os
import json
import time
import csv
from datetime import datetime


# ============================================================
# DIGITAL IMMUNE SYSTEM
# INTELLIGENT CONTINUOUS RESPONSE ENGINE
# ============================================================

RESULTS_FILE = os.path.join(
    "data",
    "detection_results.csv"
)

INCIDENT_LOG = os.path.join(
    "data",
    "incident_log.csv"
)

EVIDENCE_DIR = "evidence"

CHECK_INTERVAL = 5


# ============================================================
# ACTIVE INCIDENT
# ============================================================

active_incident = None


# ============================================================
# SEVERITY LEVELS
# ============================================================

SEVERITY_LEVELS = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}


# ============================================================
# GENERATE INCIDENT ID
# ============================================================

def generate_incident_id():

    return (
        "INC-" +
        datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )
    )


# ============================================================
# DETERMINE RESPONSE
# ============================================================

def determine_response(severity):

    severity = str(
        severity
    ).upper()

    if severity == "LOW":

        return "LOG"

    elif severity == "MEDIUM":

        return "ALERT"

    elif severity == "HIGH":

        return "SIMULATED_CONTAINMENT"

    elif severity == "CRITICAL":

        return (
            "SIMULATED_CONTAINMENT_AND_EVIDENCE"
        )

    return "LOG_ONLY"


# ============================================================
# GET INDICATOR NAMES
# ============================================================

def get_indicator_names(indicators):

    if indicators is None:

        return []

    indicators = str(
        indicators
    ).strip()

    if not indicators:

        return []

    names = []

    for item in indicators.split(","):

        item = item.strip()

        if not item:
            continue

        # Example:
        # bytes_sent (1.70σ)
        #
        # becomes:
        # bytes_sent

        if "(" in item:

            name = item.split(
                "(",
                1
            )[0].strip()

        else:

            name = item.strip()

        if name and name not in names:

            names.append(name)

    return names


# ============================================================
# CREATE INCIDENT RECORD
# ============================================================

def create_incident_record(
    row,
    response
):

    return {

        "incident_id":
            generate_incident_id(),

        "timestamp":
            str(
                row.get(
                    "timestamp",
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            ),

        "risk_score":
            float(
                row["risk_score"]
            ),

        "severity":
            str(
                row["severity"]
            ).upper(),

        "status":
            str(
                row.get(
                    "anomaly_status",
                    "ANOMALY"
                )
            ).upper(),

        "indicators":
            str(
                row.get(
                    "indicators",
                    ""
                )
            ),

        "indicator_names":
            get_indicator_names(
                row.get(
                    "indicators",
                    ""
                )
            ),

        "response":
            response,

        "response_timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "detection_count":
            1,

        "highest_risk_score":
            float(
                row["risk_score"]
            ),

        "incident_state":
            "ACTIVE",

        "last_seen":
            str(
                row.get(
                    "timestamp",
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )
    }

# ============================================================
# SAVE INCIDENT LOG
# ============================================================

def save_incident_log(incident):

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_exists = os.path.isfile(
        INCIDENT_LOG
    )

    # --------------------------------------------------------
    # indicator_names must remain JSON-compatible.
    # It is already a list, not a set.
    # --------------------------------------------------------

    log_incident = incident.copy()

    log_incident[
        "indicator_names"
    ] = ", ".join(
        incident.get(
            "indicator_names",
            []
        )
    )

    fieldnames = [
        "incident_id",
        "timestamp",
        "risk_score",
        "severity",
        "status",
        "indicators",
        "indicator_names",
        "response",
        "response_timestamp",
        "detection_count",
        "highest_risk_score",
        "incident_state"
    ]

    with open(
        INCIDENT_LOG,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        if not file_exists:

            writer.writeheader()

        writer.writerow(
            log_incident
        )


# ============================================================
# COLLECT EVIDENCE
# ============================================================

def collect_evidence(
    incident,
    row
):

    os.makedirs(
        EVIDENCE_DIR,
        exist_ok=True
    )

    filename = (
        f"{incident['incident_id']}.json"
    )

    filepath = os.path.join(
        EVIDENCE_DIR,
        filename
    )

    # --------------------------------------------------------
    # Make a JSON-safe copy of the incident.
    #
    # This is important because JSON cannot serialize
    # Python sets or other unsupported objects.
    # --------------------------------------------------------

    incident_for_json = {}

    for key, value in incident.items():

        if isinstance(
            value,
            set
        ):

            incident_for_json[key] = sorted(
                list(value)
            )

        elif isinstance(
            value,
            (list, tuple)
        ):

            incident_for_json[key] = list(
                value
            )

        else:

            incident_for_json[key] = value

    # --------------------------------------------------------
    # Convert system observation values safely.
    # --------------------------------------------------------

    system_observation = {}

    for key, value in row.items():

        try:

            if pd.isna(value):

                system_observation[key] = None

            elif isinstance(
                value,
                (int, float)
            ):

                system_observation[key] = float(
                    value
                )

            else:

                text = str(value)

                # Try converting numeric strings
                try:

                    system_observation[key] = float(
                        text
                    )

                except ValueError:

                    system_observation[key] = text

        except Exception:

            system_observation[key] = str(
                value
            )

    # --------------------------------------------------------
    # Build evidence
    # --------------------------------------------------------

    evidence = {

        "incident":
            incident_for_json,

        "system_observation":
            system_observation,

        "collection_time":
            datetime.now().isoformat(),

        "evidence_status":
            "COLLECTED"
    }

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evidence,
            file,
            indent=4
        )

    return filepath


# ============================================================
# CHECK WHETHER INCIDENTS ARE RELATED
# ============================================================

def is_related_incident(row):

    global active_incident

    if active_incident is None:
        return False

    # --------------------------------------------------------
    # Get current indicators
    # --------------------------------------------------------

    current_indicators = set(
        get_indicator_names(
            row.get(
                "indicators",
                ""
            )
        )
    )

    # --------------------------------------------------------
    # Get indicators from active incident
    # --------------------------------------------------------

    active_indicators = set(
        active_incident.get(
            "indicator_names",
            []
        )
    )

    # --------------------------------------------------------
    # If both events have indicators, check whether they share
    # at least one indicator.
    # --------------------------------------------------------

    shared_indicators = (
        current_indicators &
        active_indicators
    )

    if shared_indicators:
        return True

    # --------------------------------------------------------
    # If there are no shared indicators, check the time
    # difference between the two observations.
    #
    # Real-time detections occurring within 30 seconds of
    # each other are considered part of the same event.
    # --------------------------------------------------------

    try:

        current_time = pd.to_datetime(
            row.get("timestamp")
        )

        previous_time = pd.to_datetime(
            active_incident.get("last_seen")
        )

        time_difference = (
            current_time - previous_time
        ).total_seconds()

        if 0 <= time_difference <= 30:

            return True

    except Exception:

        pass

    return False

# ============================================================
# OPEN NEW INCIDENT
# ============================================================

def open_incident(row):

    global active_incident

    severity = str(
        row["severity"]
    ).upper()

    response = determine_response(
        severity
    )

    active_incident = (
        create_incident_record(
            row,
            response
        )
    )

    save_incident_log(
        active_incident
    )

    print()
    print(
        "🆕 NEW INCIDENT OPENED"
    )

    print(
        f"✓ Incident ID: "
        f"{active_incident['incident_id']}"
    )

    print(
        f"✓ Response: "
        f"{response}"
    )

    # --------------------------------------------------------
    # Evidence for HIGH / CRITICAL
    # --------------------------------------------------------

    if severity in [
        "HIGH",
        "CRITICAL"
    ]:

        evidence_file = collect_evidence(
            active_incident,
            row
        )

        print(
            "✓ Evidence collected."
        )

        print(
            f"  {evidence_file}"
        )

    print(
        "✓ Response processing completed."
    )


# ============================================================
# UPDATE EXISTING INCIDENT
# ============================================================

def update_incident(row):

    global active_incident

    new_severity = str(
        row["severity"]
    ).upper()

    new_risk = float(
        row["risk_score"]
    )

    old_severity = str(
        active_incident["severity"]
    ).upper()

    old_level = SEVERITY_LEVELS.get(
        old_severity,
        0
    )

    new_level = SEVERITY_LEVELS.get(
        new_severity,
        0
    )

    # --------------------------------------------------------
    # Increase detection count
    # --------------------------------------------------------

    active_incident[
        "detection_count"
    ] += 1

    # --------------------------------------------------------
    # Update latest risk score
    # --------------------------------------------------------

    active_incident[
        "risk_score"
    ] = new_risk

    # --------------------------------------------------------
    # Track highest risk score
    # --------------------------------------------------------

    if new_risk > active_incident[
        "highest_risk_score"
    ]:

        active_incident[
            "highest_risk_score"
        ] = new_risk

    # --------------------------------------------------------
    # Update timestamp
    # --------------------------------------------------------

    active_incident[
        "last_seen"
    ] = str(
        row.get(
            "timestamp",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    # --------------------------------------------------------
    # Add new indicators
    # --------------------------------------------------------

    new_indicators = get_indicator_names(
        row.get(
            "indicators",
            ""
        )
    )

    existing_indicators = active_incident.get(
        "indicator_names",
        []
    )

    for indicator in new_indicators:

        if indicator not in existing_indicators:

            existing_indicators.append(
                indicator
            )

    # IMPORTANT:
    # Keep this as a LIST, never a SET.
    active_incident[
        "indicator_names"
    ] = existing_indicators

    # --------------------------------------------------------
    # Check escalation
    # --------------------------------------------------------

    if new_level > old_level:

        active_incident[
            "severity"
        ] = new_severity

        response = determine_response(
            new_severity
        )

        active_incident[
            "response"
        ] = response

        print()
        print(
            "⬆️ INCIDENT ESCALATED"
        )

        print(
            f"Severity: "
            f"{old_severity} → {new_severity}"
        )

        print(
            f"Response: {response}"
        )

        # ----------------------------------------------------
        # Collect evidence after escalation
        # ----------------------------------------------------

        if new_severity in [
            "HIGH",
            "CRITICAL"
        ]:

            evidence_file = collect_evidence(
                active_incident,
                row
            )

            print(
                "✓ Evidence collected."
            )

            print(
                f"  {evidence_file}"
            )

    else:

        print()
        print(
            "🔄 EXISTING INCIDENT UPDATED"
        )

        print(
            f"Incident ID : "
            f"{active_incident['incident_id']}"
        )

        print(
            f"Detection # : "
            f"{active_incident['detection_count']}"
        )

        print(
            f"Risk Score  : "
            f"{new_risk:.2f}/100"
        )

        print(
            "✓ Same incident remains active."
        )

        print(
            f"Severity: "
            f"{active_incident['severity']}"
        )


# ============================================================
# RESOLVE INCIDENT
# ============================================================

def resolve_incident():

    global active_incident

    if active_incident is None:

        return

    print()
    print(
        "✅ INCIDENT RESOLVED"
    )

    print(
        f"Incident ID : "
        f"{active_incident['incident_id']}"
    )

    print(
        f"Total detections : "
        f"{active_incident['detection_count']}"
    )

    print(
        f"Highest risk : "
        f"{active_incident['highest_risk_score']:.2f}/100"
    )

    print(
        f"Final severity : "
        f"{active_incident['severity']}"
    )

    print(
        "✓ System returned to normal."
    )

    print(
        "✓ Incident closed."
    )

    active_incident = None


# ============================================================
# DISPLAY DETECTION
# ============================================================

def display_detection(row):

    status = str(
        row.get(
            "anomaly_status",
            ""
        )
    ).upper()

    severity = str(
        row.get(
            "severity",
            ""
        )
    ).upper()

    risk_score = float(
        row.get(
            "risk_score",
            0
        )
    )

    print("\n" + "=" * 65)

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       INTELLIGENT RESPONSE ENGINE"
    )

    print("=" * 65)

    print(
        f"Time       : "
        f"{datetime.now().strftime('%H:%M:%S')}"
    )

    print(
        f"Risk Score : "
        f"{risk_score:.2f}/100"
    )

    print(
        f"Severity   : "
        f"{severity}"
    )

    print(
        f"Status     : "
        f"{status}"
    )

    print(
        f"Indicators : "
        f"{row.get('indicators', 'N/A')}"
    )

    if status == "NORMAL":

        print(
            "\n🟢 SYSTEM NORMAL"
        )

    elif severity == "LOW":

        print(
            "\n⚠️ LOW-RISK ANOMALY"
        )

    elif severity == "MEDIUM":

        print(
            "\n🚨 MEDIUM-RISK ANOMALY"
        )

    elif severity == "HIGH":

        print(
            "\n🚨 HIGH-RISK ANOMALY"
        )

    elif severity == "CRITICAL":

        print(
            "\n🚨🚨 CRITICAL THREAT DETECTED"
        )


# ============================================================
# PROCESS DETECTION
# ============================================================

def process_detection(row):
    global active_incident

    severity = str(row.get("severity", "")).upper()

    # =========================================================
    # NORMAL SYSTEM CONDITION
    # =========================================================
    if severity == "NORMAL":
        if active_incident is not None:
            resolve_incident()

        print("🟢 SYSTEM NORMAL")
        print("✓ No new incident created.")
        print("✓ Monitoring continues.")
        return

    # =========================================================
    # ANOMALY DETECTED
    # =========================================================
    if str(row.get("anomaly_status", "")).upper() != "ANOMALY":
        return

    # =========================================================
    # NO ACTIVE INCIDENT → OPEN NEW INCIDENT
    # =========================================================
    if active_incident is None:
        open_incident(row)
        return

    # =========================================================
    # RELATED ANOMALY → UPDATE EXISTING INCIDENT
    # =========================================================
    if is_related_incident(row):
        update_incident(row)
        return

    # =========================================================
    # UNRELATED ANOMALY → CLOSE OLD, OPEN NEW
    # =========================================================
    print("\n🔀 NEW UNRELATED ANOMALY DETECTED")

    resolve_incident()
    open_incident(row)


# ============================================================
# LOAD DETECTION DATA SAFELY
# ============================================================

def load_detection_data():

    if not os.path.exists(
        RESULTS_FILE
    ):

        return None

    try:

        data = pd.read_csv(
            RESULTS_FILE
        )

        if data.empty:

            return None

        return data

    except pd.errors.ParserError:

        # File may currently be written
        # by realtime_detector.py.

        return None

    except Exception:

        return None


# ============================================================
# MAIN CONTINUOUS ENGINE
# ============================================================

def main():

    print("\n" + "=" * 65)

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       INTELLIGENT RESPONSE ENGINE"
    )

    print("=" * 65)

    print(
        "\nWatching:"
    )

    print(
        f"  {RESULTS_FILE}"
    )

    print(
        "\nChecking for new detection results "
        f"every {CHECK_INTERVAL} seconds."
    )

    print(
        "\nIntelligent incident tracking:"
    )

    print(
        "  ✓ Repeated anomalies are grouped."
    )

    print(
        "  ✓ Severity escalation is tracked."
    )

    print(
        "  ✓ Incidents resolve when system returns "
        "to normal."
    )

    print(
        "  ✓ HIGH/CRITICAL evidence is collected."
    )

    print(
        "  ✓ All containment actions are simulated."
    )

    print(
        "\nPress CTRL+C to stop."
    )

    # --------------------------------------------------------
    # Find existing records
    # --------------------------------------------------------

    data = load_detection_data()

    if data is not None:

        last_processed_index = len(data) - 1

        print(
            f"\n✓ Existing records found: "
            f"{len(data)}"
        )

        print(
            "✓ Existing records will NOT be "
            "processed again."
        )

    else:

        last_processed_index = -1

        print(
            "\nWaiting for first detection result..."
        )

    # --------------------------------------------------------
    # Continuous monitoring
    # --------------------------------------------------------

    try:

        while True:

            data = load_detection_data()

            if data is None:

                time.sleep(
                    CHECK_INTERVAL
                )

                continue

            current_count = len(data)

            # ------------------------------------------------
            # New records
            # ------------------------------------------------

            if current_count > (
                last_processed_index + 1
            ):

                new_records = data.iloc[
                    last_processed_index + 1:
                ]

                print(
                    f"\n🔎 {len(new_records)} "
                    f"new detection result(s) found."
                )

                for _, row in new_records.iterrows():

                    process_detection(
                        row
                    )

                    last_processed_index += 1

            # ------------------------------------------------
            # Handle file reset / replacement
            # ------------------------------------------------

            elif current_count < (
                last_processed_index + 1
            ):

                print(
                    "\n⚠ Detection file was reset."
                )

                print(
                    "✓ Restarting record tracking."
                )

                last_processed_index = (
                    current_count - 1
                )

            time.sleep(
                CHECK_INTERVAL
            )

    except KeyboardInterrupt:

        print(
            "\n\n✓ Intelligent response engine stopped."
        )

        print(
            "✓ No actual system changes were performed."
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()