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
├── dashboard/
│   └── dashboard.py
├── detection/
│   ├── __init__.py
│   ├── anomaly_detector.py
│   ├── feature_engineering.py
│   └── realtime_detector.py
├── docs/
│   ├── technical-documentation.md
│   ├── testing-and-evaluation.md
│   └── evidence/
│       ├── 01_dashboard.png
│       ├── 02_anomaly_detection.png
│       ├── 03_incident_escalation.png
│       └── 04_evidence_collection.png
├── forensics/
│   ├── __init__.py
│   ├── evidence.py
│   └── incident_logger.py
├── monitoring/
│   ├── __init__.py
│   ├── log_monitor.py
│   ├── network_monitor.py
│   └── system_monitor.py
├── response/
│   ├── __init__.py
│   ├── alerts.py
│   ├── containment.py
│   ├── recovery.py
│   ├── response_engine.py
│   └── risk_assessor.py
├── simulation/
│   ├── __init__.py
│   ├── abnormal_process.py
│   ├── port_scan.py
│   └── traffic_simulation.py
├── testing/
│   └── escalation_test.py
├── .gitignore
├── README.md
└── requirements.txt
```
**Note:** The `data/`, `models/`, and `evidence/` runtime folders are not committed. They are created or populated as you run the appropriate components. The screenshots are stored separately under `docs/evidence/`.


Some directories contain supporting or experimental modules and may not be required by the main execution pipeline. Generated CSV files, model artifacts, evidence files, and backups can vary as the system runs.

## 6. Installation

### Prerequisites

- Python installed on your computer.
- Git, if cloning the repository.
- PowerShell on Windows.
- Internet access to install Python dependencies.

### Step 1: Clone the repository

If you are setting up the project on a new computer:

```powershell
git clone https://github.com/njaphathabii-ui/digital-immune-system.git
cd digital-immune-system
```

If you are already working in your existing project folder, skip this step.

### Step 2: Create a virtual environment

```powershell
python -m venv venv
```

### Step 3: Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, consult the Python or PowerShell documentation for an appropriate execution-policy configuration.

### Step 4: Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The virtual environment isolates the project's dependencies from other Python projects.

## 7. Running the System

Start each component in a separate PowerShell terminal. Run the commands from the project root.

### Initial setup: Collect data and train the model

The real-time detector requires two trained model files:

- `models/isolation_forest.pkl`
- `models/scaler.pkl`

These files are generated locally and are not included in the GitHub repository.

**Step 1: Collect monitoring data**

Activate the virtual environment, then run:

```powershell
python monitoring\system_monitor.py
```

Allow the monitor to collect a representative sample of system activity. Stop it with `Ctrl + C` when you have enough data to train an initial model.

The collected data should be available at `data/system_metrics.csv`.

**Step 2: Train the anomaly-detection model**

Run:

```powershell
python detection\anomaly_detector.py
```

This script reads `data/system_metrics.csv`, prepares the numerical features, trains the Isolation Forest model, and saves the model and scaler under `models/`. It also writes batch detection results to `data/detection_results.csv`.

If the monitoring CSV does not exist or lacks the required features, resolve that issue before training.

**Step 3: Start the application components**

Once model training has completed, start the monitoring, real-time detection, response engine, and dashboard using the terminal commands below.

> Training on locally collected data creates an initial baseline; it does not establish detection accuracy against confirmed cyberattacks. For research evaluation, use an appropriate test dataset and document how it was labelled and evaluated.

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