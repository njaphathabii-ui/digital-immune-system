import csv
import os
import time
from datetime import datetime

DETECTION_FILE = "data/detection_results.csv"


FIELDNAMES = [
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


def add_test_detection(risk_score, severity):

    """
    Adds a controlled detection result for testing.

    This does NOT modify the computer,
    kill processes, block connections,
    or change Windows settings.
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    row = {
        "timestamp": timestamp,

        "cpu_usage": "95.0",
        "memory_usage": "95.0",
        "disk_usage": "95.0",
        "process_count": "500",

        "bytes_sent": "999999",
        "bytes_received": "999999",
        "packets_sent": "99999",
        "packets_received": "99999",

        "established_connections": "200",
        "listening_connections": "50",
        "other_connections": "100",

        "anomaly_status": "ANOMALY",
        "risk_score": risk_score,
        "severity": severity
    }

    file_exists = os.path.exists(
        DETECTION_FILE
    )

    with open(
        DETECTION_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print()
    print("=" * 65)
    print("CONTROLLED ESCALATION TEST")
    print("=" * 65)
    print(f"Time       : {timestamp}")
    print(f"Risk Score : {risk_score}/100")
    print(f"Severity   : {severity}")
    print("Status     : ANOMALY")
    print("=" * 65)


print()
print("=" * 65)
print("DIGITAL IMMUNE SYSTEM")
print("CONTROLLED ESCALATION TEST")
print("=" * 65)
print()

print("This is a SAFE simulation.")
print("No processes will be killed.")
print("No network connections will be blocked.")
print("No Windows settings will be changed.")
print()

input(
    "Press ENTER to begin the test..."
)


# ---------------------------------------------------------
# TEST 1 — MEDIUM
# ---------------------------------------------------------

print("\n[1/4] Sending MEDIUM anomaly...")

add_test_detection(
    45.0,
    "MEDIUM"
)

time.sleep(8)


# ---------------------------------------------------------
# TEST 2 — HIGH
# ---------------------------------------------------------

print("\n[2/4] Sending HIGH anomaly...")

add_test_detection(
    70.0,
    "HIGH"
)

time.sleep(8)


# ---------------------------------------------------------
# TEST 3 — CRITICAL
# ---------------------------------------------------------

print("\n[3/4] Sending CRITICAL anomaly...")

add_test_detection(
    90.0,
    "CRITICAL"
)

time.sleep(8)


# ---------------------------------------------------------
# TEST 4 — NORMAL
# ---------------------------------------------------------

print("\n[4/4] Sending NORMAL result...")

normal_timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

normal_row = {
    "timestamp": normal_timestamp,

    "cpu_usage": "20.0",
    "memory_usage": "70.0",
    "disk_usage": "80.0",
    "process_count": "350",

    "bytes_sent": "1000",
    "bytes_received": "1000",
    "packets_sent": "100",
    "packets_received": "100",

    "established_connections": "20",
    "listening_connections": "5",
    "other_connections": "10",

    "anomaly_status": "NORMAL",
    "risk_score": 5.0,
    "severity": "NORMAL"
}

with open(
    DETECTION_FILE,
    "a",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=FIELDNAMES
    )

    writer.writerow(normal_row)

print()
print("=" * 65)
print("NORMAL RESULT SENT")
print("=" * 65)
print(f"Time       : {normal_timestamp}")
print("Risk Score : 5.0/100")
print("Severity   : NORMAL")
print("Status     : NORMAL")
print("=" * 65)


print()
print("=" * 65)
print("CONTROLLED TEST COMPLETE")
print("=" * 65)
print()

print("Expected response-engine sequence:")
print()
print("MEDIUM   → NEW INCIDENT")
print("HIGH     → SAME INCIDENT + ESCALATION")
print("CRITICAL → SAME INCIDENT + ESCALATION")
print("NORMAL   → INCIDENT RESOLVED")
print()
print("Check Terminal 3 for the actual results.")