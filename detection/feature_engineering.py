import pandas as pd
import os


INPUT_FILE = os.path.join(
    "data",
    "system_metrics.csv"
)

OUTPUT_FILE = os.path.join(
    "data",
    "prepared_dataset.csv"
)


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


def load_data():
    """
    Load the synchronized monitoring dataset.
    """

    if not os.path.exists(INPUT_FILE):

        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE}"
        )

    data = pd.read_csv(INPUT_FILE)

    return data


def clean_data(data):
    """
    Clean and validate the monitoring dataset.
    """

    print("\nInitial records:", len(data))

    # Convert timestamp
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce"
    )

    # Remove invalid timestamps
    data = data.dropna(
        subset=["timestamp"]
    )

    # Remove duplicate records
    data = data.drop_duplicates()

    # Make sure numerical columns are numeric
    for feature in FEATURES:

        data[feature] = pd.to_numeric(
            data[feature],
            errors="coerce"
        )

    # Remove rows containing invalid values
    data = data.dropna(
        subset=FEATURES
    )

    # Remove impossible negative values
    for feature in FEATURES:

        data = data[
            data[feature] >= 0
        ]

    data = data.reset_index(
        drop=True
    )

    print(
        "Records after cleaning:",
        len(data)
    )

    return data


def select_features(data):
    """
    Select features for anomaly detection.
    """

    return data[FEATURES]


def save_data(data):

    os.makedirs(
        "data",
        exist_ok=True
    )

    data.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nPrepared dataset saved to:"
    )

    print(
        OUTPUT_FILE
    )


def main():

    print("\n" + "=" * 65)

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       DATA PREPARATION"
    )

    print("=" * 65)

    print(
        "\nLoading synchronized monitoring data..."
    )

    data = load_data()

    print(
        f"Loaded records: {len(data)}"
    )

    print(
        "\nCleaning dataset..."
    )

    data = clean_data(data)

    print(
        "\nSelecting ML features..."
    )

    features = select_features(data)

    print(
        f"Number of ML features: {len(features.columns)}"
    )

    print("\nSelected features:")

    for feature in features.columns:

        print(
            f" - {feature}"
        )

    save_data(features)

    print(
        "\nData preparation completed successfully."
    )

    print("=" * 65)


if __name__ == "__main__":

    main()