import psutil
import csv
import os
import time
from datetime import datetime


DATA_FILE = os.path.join("data", "network_metrics.csv")


def get_network_metrics():
    """
    Collect information about the current network state.
    """

    # Get network I/O statistics
    network = psutil.net_io_counters()

    # Get currently active network connections
    connections = psutil.net_connections()

    # Count connections by status
    established = 0
    listening = 0
    other = 0

    for connection in connections:

        if connection.status == "ESTABLISHED":
            established += 1

        elif connection.status == "LISTEN":
            listening += 1

        else:
            other += 1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": timestamp,
        "bytes_sent": network.bytes_sent,
        "bytes_received": network.bytes_recv,
        "packets_sent": network.packets_sent,
        "packets_received": network.packets_recv,
        "established_connections": established,
        "listening_connections": listening,
        "other_connections": other
    }


def save_metrics(metrics):
    """
    Save network metrics to a CSV file.
    """

    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(DATA_FILE)

    fieldnames = [
        "timestamp",
        "bytes_sent",
        "bytes_received",
        "packets_sent",
        "packets_received",
        "established_connections",
        "listening_connections",
        "other_connections"
    ]

    with open(DATA_FILE, "a", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)


def display_metrics(metrics):
    """
    Display network information in the terminal.
    """

    print("\n" + "=" * 60)
    print("       DIGITAL IMMUNE SYSTEM")
    print("       NETWORK MONITORING ENGINE")
    print("=" * 60)

    print(f"Timestamp              : {metrics['timestamp']}")
    print(f"Bytes Sent             : {metrics['bytes_sent']}")
    print(f"Bytes Received         : {metrics['bytes_received']}")
    print(f"Packets Sent           : {metrics['packets_sent']}")
    print(f"Packets Received       : {metrics['packets_received']}")
    print(f"Established Connections: {metrics['established_connections']}")
    print(f"Listening Connections  : {metrics['listening_connections']}")
    print(f"Other Connections      : {metrics['other_connections']}")

    print(f"Data saved to          : {DATA_FILE}")

    print("=" * 60)


def monitor_network(interval=5):
    """
    Continuously monitor network activity.
    """

    print("\nDigital Immune System network monitoring started.")
    print("Monitoring interval: 5 seconds")
    print("Press CTRL+C to stop monitoring.\n")

    try:

        while True:

            metrics = get_network_metrics()

            save_metrics(metrics)

            display_metrics(metrics)

            time.sleep(interval)

    except KeyboardInterrupt:

        print("\nNetwork monitoring stopped.")
        print("Network monitor shut down safely.")


if __name__ == "__main__":
    monitor_network()