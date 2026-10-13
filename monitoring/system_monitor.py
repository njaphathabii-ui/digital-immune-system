import psutil
import time
import csv
import os
from datetime import datetime


# ============================================================
# FILE LOCATION
# ============================================================

DATA_FILE = os.path.join("data", "system_metrics.csv")


# ============================================================
# EXPECTED DATA COLUMNS
# ============================================================

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
    "other_connections"
]


# ============================================================
# COLLECT SYSTEM METRICS
# ============================================================

def get_system_metrics():
    """
    Collect the current state of the Windows system.
    """

    # --------------------------------------------------------
    # CPU usage
    # --------------------------------------------------------

    cpu_usage = psutil.cpu_percent(interval=1)

    # --------------------------------------------------------
    # Memory usage
    # --------------------------------------------------------

    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    # --------------------------------------------------------
    # Disk usage
    # --------------------------------------------------------

    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    # --------------------------------------------------------
    # Number of running processes
    # --------------------------------------------------------

    process_count = len(psutil.pids())

    # --------------------------------------------------------
    # Network I/O statistics
    # --------------------------------------------------------

    network = psutil.net_io_counters()

    bytes_sent = network.bytes_sent
    bytes_received = network.bytes_recv

    packets_sent = network.packets_sent
    packets_received = network.packets_recv

    # --------------------------------------------------------
    # Network connection statistics
    # --------------------------------------------------------

    established_connections = 0
    listening_connections = 0
    other_connections = 0

    try:

        connections = psutil.net_connections(
            kind="inet"
        )

        for connection in connections:

            status = connection.status

            if status == psutil.CONN_ESTABLISHED:

                established_connections += 1

            elif status == psutil.CONN_LISTEN:

                listening_connections += 1

            else:

                other_connections += 1

    except (psutil.AccessDenied, PermissionError):

        # Some Windows connections may require
        # elevated privileges.

        established_connections = 0
        listening_connections = 0
        other_connections = 0

    # --------------------------------------------------------
    # Timestamp
    # --------------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "timestamp": timestamp,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "process_count": process_count,
        "bytes_sent": bytes_sent,
        "bytes_received": bytes_received,
        "packets_sent": packets_sent,
        "packets_received": packets_received,
        "established_connections": established_connections,
        "listening_connections": listening_connections,
        "other_connections": other_connections
    }


# ============================================================
# CHECK CSV STRUCTURE
# ============================================================

def prepare_data_file():
    """
    Make sure system_metrics.csv has the correct
    12-column structure.

    The previous version of the monitor created a
    7-column file. We create a fresh file so the new
    records have the correct structure.
    """

    os.makedirs(
        "data",
        exist_ok=True
    )

    # --------------------------------------------------------
    # If the existing file has the old structure,
    # create a backup before replacing it.
    # --------------------------------------------------------

    if os.path.isfile(DATA_FILE):

        try:

            with open(
                DATA_FILE,
                "r",
                newline=""
            ) as file:

                reader = csv.reader(file)

                existing_header = next(
                    reader,
                    None
                )

            if existing_header != FIELDNAMES:

                backup_file = os.path.join(
                    "data",
                    "system_metrics_old.csv"
                )

                # Avoid overwriting an existing backup

                counter = 1

                while os.path.exists(
                    backup_file
                ):

                    backup_file = os.path.join(
                        "data",
                        f"system_metrics_old_{counter}.csv"
                    )

                    counter += 1

                os.rename(
                    DATA_FILE,
                    backup_file
                )

                print(
                    "\nPrevious monitoring dataset "
                    "backed up to:"
                )

                print(
                    f"  {backup_file}"
                )

        except (PermissionError, OSError) as error:

            print(
                "\nWARNING:"
            )

            print(
                "Could not inspect the existing "
                "monitoring file."
            )

            print(
                f"Reason: {error}"
            )

            raise


# ============================================================
# SAVE METRICS
# ============================================================

def save_metrics(metrics):
    """
    Save monitoring data to a CSV file.
    """

    os.makedirs(
        "data",
        exist_ok=True
    )

    file_exists = os.path.isfile(
        DATA_FILE
    )

    with open(
        DATA_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        # Add headings when creating the file

        if not file_exists:

            writer.writeheader()

        writer.writerow(
            metrics
        )


# ============================================================
# DISPLAY METRICS
# ============================================================

def display_metrics(metrics):
    """
    Display collected system metrics
    in the terminal.
    """

    print(
        "\n" + "=" * 65
    )

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       SYSTEM MONITORING ENGINE"
    )

    print(
        "=" * 65
    )

    print(
        f"Timestamp              : "
        f"{metrics['timestamp']}"
    )

    print(
        f"CPU Usage              : "
        f"{metrics['cpu_usage']}%"
    )

    print(
        f"Memory Usage           : "
        f"{metrics['memory_usage']}%"
    )

    print(
        f"Disk Usage             : "
        f"{metrics['disk_usage']}%"
    )

    print(
        f"Running Processes      : "
        f"{metrics['process_count']}"
    )

    print(
        f"Bytes Sent             : "
        f"{metrics['bytes_sent']}"
    )

    print(
        f"Bytes Received         : "
        f"{metrics['bytes_received']}"
    )

    print(
        f"Packets Sent           : "
        f"{metrics['packets_sent']}"
    )

    print(
        f"Packets Received       : "
        f"{metrics['packets_received']}"
    )

    print(
        f"Established Connections: "
        f"{metrics['established_connections']}"
    )

    print(
        f"Listening Connections  : "
        f"{metrics['listening_connections']}"
    )

    print(
        f"Other Connections      : "
        f"{metrics['other_connections']}"
    )

    print(
        f"Data saved to          : "
        f"{DATA_FILE}"
    )

    print(
        "=" * 65
    )


# ============================================================
# MONITOR SYSTEM
# ============================================================

def monitor_system(interval=5):
    """
    Continuously monitor the system.

    Args:
        interval (int):
            Seconds between measurements.
    """

    print(
        "\nDigital Immune System monitoring started."
    )

    print(
        "Monitoring interval: 5 seconds"
    )

    print(
        "Press CTRL+C to stop monitoring.\n"
    )

    # Make sure the CSV structure is correct

    prepare_data_file()

    try:

        while True:

            # ------------------------------------------------
            # Collect current system information
            # ------------------------------------------------

            metrics = get_system_metrics()

            # ------------------------------------------------
            # Save information
            # ------------------------------------------------

            save_metrics(
                metrics
            )

            # ------------------------------------------------
            # Display information
            # ------------------------------------------------

            display_metrics(
                metrics
            )

            # ------------------------------------------------
            # Wait before next measurement
            # ------------------------------------------------

            time.sleep(
                interval
            )

    except KeyboardInterrupt:

        print(
            "\nMonitoring stopped."
        )

        print(
            "Digital Immune System "
            "shut down safely."
        )


# ============================================================
# START MONITOR
# ============================================================

if __name__ == "__main__":

    monitor_system()