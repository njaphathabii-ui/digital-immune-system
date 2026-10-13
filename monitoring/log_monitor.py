import csv
import os
import time
from datetime import datetime


DATA_FILE = os.path.join("data", "security_events.csv")


def create_security_event(event_type, severity, description):
    """
    Create a standardized security event.
    """

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "severity": severity,
        "description": description
    }


def save_event(event):
    """
    Save a security event to the CSV evidence dataset.
    """

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(DATA_FILE)

    fieldnames = [
        "timestamp",
        "event_type",
        "severity",
        "description"
    ]

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(event)


def display_event(event):
    """
    Display a security event.
    """

    print("\n" + "=" * 60)
    print("       DIGITAL IMMUNE SYSTEM")
    print("       SECURITY EVENT MONITOR")
    print("=" * 60)

    print(f"Timestamp   : {event['timestamp']}")
    print(f"Event Type  : {event['event_type']}")
    print(f"Severity    : {event['severity']}")
    print(f"Description : {event['description']}")

    print("=" * 60)


def monitor_logs(interval=10):
    """
    Demonstration security-event monitoring loop.

    This version creates monitoring heartbeat events.
    Actual Windows Event Log integration will be added
    in the next stage.
    """

    print("\nDigital Immune System security monitoring started.")
    print("Press CTRL+C to stop monitoring.\n")

    try:

        while True:

            event = create_security_event(
                "MONITORING_HEARTBEAT",
                "INFO",
                "Security monitoring system is operating normally."
            )

            save_event(event)

            display_event(event)

            time.sleep(interval)

    except KeyboardInterrupt:

        print("\nSecurity monitoring stopped.")
        print("Log monitor shut down safely.")


if __name__ == "__main__":
    monitor_logs()