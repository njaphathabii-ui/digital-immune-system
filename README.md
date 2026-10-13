# Digital Immune System

An intelligent, machine-learning-based system monitoring and anomaly detection prototype designed to identify unusual system activity, assess risk, track security incidents, and simulate automated responses.

## 1. Project Overview

The Digital Immune System is a cybersecurity research project inspired by the human immune system. Just as a biological immune system detects threats and responds to protect the body, this prototype monitors computer system activity, identifies potentially abnormal behaviour, and tracks incidents as their severity changes.

The project combines system monitoring, machine-learning-based anomaly detection, risk assessment, incident management, evidence collection, and a Streamlit dashboard.

**Important:** Automated containment and recovery are simulated. The prototype does not perform actual system containment or make changes to the operating system.

## 2. Project Objectives

- Continuously monitor system resource usage and network activity.
- Apply an Isolation Forest model to identify potentially anomalous behaviour.
- Assign risk scores and severity levels to detected activity.
- Group related anomalies into incidents and track severity escalation.
- Collect JSON evidence for high- and critical-severity incidents.
- Display monitoring, detection, and response information through a dashboard.
- Demonstrate a safe, simulated automated-response workflow.

## 3. System Architecture

The prototype follows this processing pipeline:

```text
System and Network Monitoring
             |
             v
     System Metrics CSV
             |
             v
   Machine Learning Detection
             |
             v
      Risk Assessment
             |
             v
   Incident Management
             |
       +-----+------+
       |            |
       v            v
 Evidence Files   Incident Log
       |
       v
 Streamlit Dashboard
```

The monitoring, detection, and response components operate as separate Python processes. The dashboard presents the available monitoring and response information.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| psutil | System and network monitoring |
| pandas and NumPy | Data processing |
| scikit-learn | Isolation Forest anomaly detection |
| joblib | Saving and loading machine-learning artifacts |
| Streamlit | Interactive monitoring dashboard |
| Plotly | Data visualisation |
| CSV | Storing monitoring and detection results |
| JSON | Storing incident evidence |

The project also includes additional libraries for networking, web applications, and supporting functionality.

## 5. Project Structure

```text
digital-immune-system/
├── backup/
│   ├── data/
│   └── legacy/
├── dashboard/
│   ├── dashboard.py
│   └── test.py
├── data/
│   ├── system_metrics.csv
│   ├── detection_results.csv
│   ├── incident_log.csv
│   └── security_events.csv
├── detection/
│   ├── anomaly_detector.py
│   ├── feature_engineering.py
│   └── realtime_detector.py
├── evidence/
├── forensics/
├── models/
│   ├── isolation_forest.pkl
│   └── scaler.pkl
├── monitoring/
│   ├── system_monitor.py
│   ├── network_monitor.py
│   └── log_monitor.py
├── response/
│   ├── response_engine.py
│   └── risk_assessor.py
├── simulation/
├── testing/
│   └── escalation_test.py
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

Some directories contain supporting or experimental modules and may not be required by the main execution pipeline. Generated CSV files, model artifacts, evidence files, and backups can vary as the system runs.

## 6. Installation

### Prerequisites

- Python installed on the computer.
- Visual Studio Code or another Python-compatible editor.
- PowerShell on Windows.
- The project source files and required trained model artifacts.

### Step 1: Open the project directory

Open PowerShell and navigate to the project folder:

```powershell
cd "C:\Users\admin\OneDrive - Sol Plaatje University\Desktop\vscode\digital-immune-system"
```

### Step 2: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The virtual environment isolates the project's Python dependencies from other Python projects.

## 7. Running the System

Start each component in a separate PowerShell terminal. Run the commands from the project root.

### Terminal 1: System monitoring

```powershell
python monitoring\system_monitor.py
```

This component collects system metrics and writes them to `data\system_metrics.csv`.

### Terminal 2: Real-time anomaly detection

```powershell
python detection\realtime_detector.py
```

This component processes incoming monitoring data using the configured anomaly-detection model and writes detection results to `data\detection_results.csv`.

The trained model and scaler must be available in the `models` directory.

### Terminal 3: Intelligent response engine

```powershell
python response\response_engine.py
```

This component tracks incidents, updates severity, records incident information, and collects evidence when the applicable severity threshold is reached.

### Terminal 4: Dashboard

```powershell
streamlit run dashboard\dashboard.py
```

Open the local URL printed by Streamlit in your browser.

### Stopping the system

Press `Ctrl + C` in each terminal to stop its process.

## 8. Anomaly Detection and Risk Assessment

The prototype uses the Isolation Forest algorithm, an unsupervised machine-learning technique for identifying observations that differ from normal patterns.

The monitoring data includes features such as:

- CPU usage
- Memory usage
- Disk usage
- Running process count
- Network bytes and packets sent or received
- Established network connections
- Listening network connections
- Other network connections

The detection component uses the configured feature-processing pipeline and trained model to evaluate system activity. Detected anomalies are passed to the risk-assessment and response components.

An anomaly indicates unusual behaviour, not necessarily a confirmed cyberattack. The system is a prototype and requires further evaluation before being used for operational security decisions.

## 9. Incident Management and Simulated Response

The response engine demonstrates a basic incident lifecycle:

1. **Detection:** Receive a potentially anomalous event.
2. **Incident creation:** Open an incident when required.
3. **Incident tracking:** Associate subsequent related detections with the active incident.
4. **Severity escalation:** Track changes in severity as risk increases.
5. **Evidence collection:** Record evidence for applicable high- and critical-severity events.
6. **Resolution:** Mark the incident resolved when the system returns to a normal state according to the configured logic.

The prototype uses simulated response actions. It does not actually terminate processes, block network connections, isolate the computer, or perform system recovery.

## 10. Testing

The project includes a controlled escalation test:

```powershell
python testing\escalation_test.py
```

The test generates controlled detection events to demonstrate incident creation, severity escalation, evidence collection, and resolution.

Run this test only when you understand how it interacts with the response engine and its output files. It may modify incident logs or create evidence files.

The controlled test complements live monitoring; it does not by itself establish the real-world detection accuracy of the model.

## 11. Generated Data and Model Files

The following files are produced or used during execution:

| File or directory | Purpose |
|---|---|
| `data/system_metrics.csv` | Collected monitoring metrics |
| `data/detection_results.csv` | Anomaly detection output |
| `data/incident_log.csv` | Incident tracking records |
| `data/security_events.csv` | Security event records |
| `models/isolation_forest.pkl` | Trained anomaly-detection model |
| `models/scaler.pkl` | Feature scaling artifact |
| `evidence/` | JSON incident evidence |
| `backup/` | Preserved older data and legacy files |

Some generated files are excluded by `.gitignore`. Back up important research data separately if it must be retained.

Only load trusted pickle or joblib model files, because loading untrusted serialized files can execute malicious code.

## 12. Current Limitations

- Anomalies may be false positives and do not automatically indicate an attack.
- Detection performance depends on the training data, feature preparation, and model configuration.
- The prototype uses simulated response actions rather than real containment.
- Some monitoring functions may require additional operating-system permissions.
- Results from a controlled test do not prove effectiveness against real cyberattacks.
- Further testing is required to evaluate detection accuracy, false-positive rates, performance, and recovery behaviour.

## 13. Future Improvements

Potential future enhancements include:

- Evaluating detection accuracy with labelled datasets.
- Measuring precision, recall, F1-score, and false-positive rates.
- Improving baseline learning and anomaly thresholds.
- Integrating additional security event sources.
- Expanding incident correlation and evidence analysis.
- Implementing carefully controlled response mechanisms in an isolated test environment.
- Adding automated test coverage and more detailed technical documentation.

## 14. Documentation

Additional project documentation is available in the `docs/` directory.

- [Technical Documentation](docs/technical-documentation.md) — explains the system architecture, monitoring, feature engineering, anomaly detection, incident management, evidence collection, and dashboard.
- [Testing and Evaluation](docs/testing-and-evaluation.md) — documents functional tests, observed results, testing limitations, and recommended quantitative evaluation.
- **Demonstration Evidence** — see `docs/evidence/` for screenshots of the dashboard, anomaly detection, incident escalation, and evidence collection.

## 15. Project Purpose

This project demonstrates how ideas from artificial intelligence, machine learning, cybersecurity, system monitoring, and automation can be combined into a prototype inspired by a digital immune system.

It is intended for educational and research purposes and should not be considered a replacement for a production intrusion detection or endpoint protection system.