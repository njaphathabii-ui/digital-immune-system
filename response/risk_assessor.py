import pandas as pd
import os


RESULTS_FILE = os.path.join(
    "data",
    "detection_results.csv"
)


def assess_risk(risk_score, anomaly_status):

    # Normal observations are logged but do not
    # trigger an incident response.
    if anomaly_status == "NORMAL":

        return {
            "severity": "NORMAL",
            "response": "LOG_ONLY"
        }

    # Only anomalous observations reach the
    # incident response levels.

    if risk_score < 40:

        return {
            "severity": "LOW",
            "response": "LOG"
        }

    elif risk_score < 60:

        return {
            "severity": "MEDIUM",
            "response": "ALERT"
        }

    elif risk_score < 75:

        return {
            "severity": "HIGH",
            "response": "SIMULATED_CONTAINMENT"
        }

    else:

        return {
            "severity": "CRITICAL",
            "response": "SIMULATED_CONTAINMENT_AND_EVIDENCE"
        }


def main():

    print("\n" + "=" * 65)

    print(
        "       DIGITAL IMMUNE SYSTEM"
    )

    print(
        "       RISK ASSESSMENT ENGINE"
    )

    print("=" * 65)

    if not os.path.exists(
        RESULTS_FILE
    ):

        print(
            "\nDetection results not found."
        )

        print(
            "Run anomaly_detector.py first."
        )

        return

    data = pd.read_csv(
        RESULTS_FILE
    )

    print(
        f"\nAssessing {len(data)} observations..."
    )

    print("\nRisk assessment:\n")

    for _, row in data.iterrows():

        risk = row["risk_score"]

        assessment = assess_risk(
            risk,
            row["anomaly_status"]
        )

        print(
            f"Risk Score : {risk:.2f}/100"
        )

        print(
            f"Severity   : "
            f"{assessment['severity']}"
        )

        print(
            f"Response   : "
            f"{assessment['response']}"
        )

        print(
            f"Status     : "
            f"{row['anomaly_status']}"
        )

        print(
            f"Indicators : "
            f"{row['indicators']}"
        )

        print("-" * 65)

    print(
        "\nRisk assessment completed."
    )

    print("=" * 65)


if __name__ == "__main__":

    main()