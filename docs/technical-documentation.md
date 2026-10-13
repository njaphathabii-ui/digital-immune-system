# Digital Immune System
## Technical Documentation

**Project type:** Computer Science research and development prototype  
**Primary language:** Python  
**Main interface:** Streamlit dashboard  
**Machine-learning approach:** Isolation Forest anomaly detection

---

## 1. Introduction

The Digital Immune System is a cybersecurity-oriented software prototype designed to monitor computer system activity, identify potentially anomalous behaviour, assess risk, and demonstrate an automated incident-response workflow.

The project is inspired by the human immune system. A biological immune system monitors for threats and responds to protect the body. Similarly, this software prototype collects system and network metrics, evaluates activity using machine learning, and records incidents that require further attention.

The prototype integrates system monitoring, data preparation, anomaly detection, risk assessment, incident management, evidence collection, and visualisation.

All containment actions are simulated. The software is intended for educational and research purposes and is not a replacement for a production security monitoring or endpoint protection solution.

## 2. System Objectives

The main objectives are to:

1. Collect system resource and network activity metrics.
2. Prepare numerical data for machine-learning processing.
3. Identify potentially anomalous observations using an Isolation Forest model.
4. Assign risk scores and severity classifications to detection results.
5. Group related detections into incidents and track changes in severity.
6. Record incident information and collect structured evidence.
7. Present monitoring and response information through a dashboard.
8. Demonstrate a controlled incident lifecycle without performing actual system containment.

## 3. System Architecture

The application is divided into modules with separate responsibilities.

### 3.1 Architectural components

| Component | Main responsibility |
|---|---|
| Monitoring | Collect system and network metrics |
| Feature engineering | Clean monitoring data and select model features |
| Anomaly detection | Evaluate observations using the trained model |
| Risk assessment | Determine risk scores and severity classifications |
| Response engine | Manage incident creation, updates, escalation, and resolution |
| Evidence collection | Save structured incident evidence in JSON format |
| Dashboard | Display system status, detections, and response information |
| Testing | Verify selected incident-response behaviours |

### 3.2 Data flow

The principal processing flow is:

```text
System and Network Monitoring
            |
            v
   system_metrics.csv
            |
            v
  Data Preparation and Cleaning
            |
            v
  prepared_dataset.csv
            |
            v
  Machine-Learning Detection
            |
            v
   detection_results.csv
            |
            v
       Risk Assessment
            |
            v
    Incident Response Engine
        /           \
       v             v
Incident Log     JSON Evidence
        \           /
         v         v
        Streamlit Dashboard
```

The diagram represents the project's logical workflow. The feature-engineering script and real-time detector are separate execution components; the diagram does not imply that every stage automatically invokes the next one.

## 4. System Monitoring

The monitoring component is implemented in `monitoring/system_monitor.py`.

It uses the `psutil` library to collect system and network measurements. The current monitoring dataset contains the following fields:

| Feature | Description |
|---|---|
| `timestamp` | Time when the observation was recorded |
| `cpu_usage` | CPU utilisation percentage |
| `memory_usage` | Memory utilisation percentage |
| `disk_usage` | Disk utilisation percentage |
| `process_count` | Number of running processes |
| `bytes_sent` | Cumulative network bytes sent |
| `bytes_received` | Cumulative network bytes received |
| `packets_sent` | Cumulative network packets sent |
| `packets_received` | Cumulative network packets received |
| `established_connections` | Number of established connections observed |
| `listening_connections` | Number of listening connections observed |
| `other_connections` | Number of connections in other states |

The monitoring process writes observations to `data/system_metrics.csv`. The configured monitoring interval is five seconds.

These measurements provide contextual information about system activity. Unusual resource consumption or connection patterns may justify further investigation, but individual measurements do not independently establish that a cyberattack has occurred.

## 5. Data Preparation and Feature Engineering

The data-preparation component is implemented in `detection/feature_engineering.py`.

Its input is `data/system_metrics.csv`, and its output is `data/prepared_dataset.csv`.

The preparation procedure performs the following operations:

1. Loads the monitoring CSV file.
2. Converts timestamps to datetime values.
3. Removes records with invalid timestamps.
4. Removes duplicate records.
5. Converts the selected features to numeric values.
6. Removes records containing invalid feature values.
7. Removes records with negative feature values.
8. Selects the eleven numerical features used for machine-learning processing.
9. Saves the resulting feature dataset.

The timestamp is excluded from the prepared feature matrix. The output contains the numerical system and network features rather than the original timestamp column.

Cleaning helps ensure that invalid values do not enter the selected feature dataset. It does not label records as malicious or benign.

## 6. Machine-Learning Anomaly Detection

The prototype uses the Isolation Forest algorithm from scikit-learn.

Isolation Forest is an unsupervised anomaly-detection method that identifies observations that can be isolated relatively easily within the model's feature space.

The project includes the following model artifacts:

- `models/isolation_forest.pkl`
- `models/scaler.pkl`

The detector uses the trained model and scaling artifact to process monitoring features. Its output includes monitoring values, an anomaly status, a risk score, and a severity classification.

The real-time detection component is implemented in `detection/realtime_detector.py`. Detection results are stored in `data/detection_results.csv`.

The selected features cover system utilisation, process activity, network traffic volumes, packet counts, and connection states.

### 6.1 Interpreting detections

An anomaly is an observation that differs from the patterns learned by the model. It is not necessarily a cyberattack.

Potential causes of unusual observations include legitimate software activity, heavy resource usage, changes in network traffic, measurement variation, or malicious activity.

Consequently, anomaly results should be interpreted as indicators for further investigation rather than definitive proof of compromise.

### 6.2 Risk score and severity

The detector and response components use risk scores and severity labels to communicate the assessed state of an observation or incident.

The dashboard displays these values to help the operator understand the current status.

Risk scores and severity labels are separate outputs. A risk score should not be interpreted as a probability of attack unless the model has been calibrated and validated for that interpretation.

The precise thresholds and scoring rules are defined by the implementation and should be documented alongside the relevant source code.

## 7. Incident Management and Response

The incident-response component is implemented in `response/response_engine.py`, with risk-assessment functionality in `response/risk_assessor.py`.

The response engine maintains incident information and processes incoming detection results.

### 7.1 Incident lifecycle

The prototype demonstrates the following lifecycle:

1. **Incident creation:** A qualifying detection opens an incident.
2. **Incident update:** Subsequent related detections update the existing incident.
3. **Severity tracking:** The engine records changes in the incident's assessed severity.
4. **Evidence collection:** Evidence is recorded for applicable high- and critical-severity incidents.
5. **Resolution:** The incident is marked resolved when the configured logic recognises a return to normal operation.

The incident log records fields such as the incident ID, timestamp, risk score, severity, status, response, detection count, highest risk score, and incident state.

### 7.2 Simulated response actions

The response logic maps incident conditions to response labels. Examples include logging normal activity, issuing alerts, and recording simulated containment actions for higher-severity events.

The prototype does not actually terminate processes, block network connections, isolate the host, or perform system recovery.

This restriction keeps the demonstration focused on the incident-management workflow without making unauthorised or potentially disruptive system changes.

## 8. Evidence Collection and Security Logging

The response workflow records incident evidence as JSON files in the `evidence/` directory.

A collected evidence record can contain:

- Incident identifier and timestamp
- Risk score and severity
- Incident status and response label
- Detection count and highest observed risk score
- Relevant system observations
- Evidence collection status

The incident log is stored in `data/incident_log.csv`. Additional security events are recorded in `data/security_events.csv`.

These files support inspection of the prototype's behaviour after an event has been processed.

The collected information represents the metrics and event details available to the application. It should not be described as a complete forensic image or proof of an actual cyberattack.

## 9. Dashboard and Visualisation

The dashboard is implemented in `dashboard/dashboard.py` and uses Streamlit.

It provides a visual interface for reviewing the prototype's current security status.

The demonstrated interface includes:

- Current risk score
- Severity and system status
- Intelligent response information
- CPU, memory, and disk utilisation
- Running process count
- Latest detection information
- Live system activity visualisation

The dashboard helps users interpret the information produced by the monitoring and response components without having to inspect every CSV or JSON file manually.

The dashboard is a presentation layer; its displayed values depend on the available data and the implementation's refresh and processing logic.

## 10. Testing Approach

The project includes a controlled escalation test in `testing/escalation_test.py`.

The test generates predefined detection scenarios to exercise incident creation, severity escalation, evidence collection, and resolution.

The demonstrated test workflow has included:

- Opening a new incident
- Updating or tracking an incident
- Recording simulated containment actions
- Collecting JSON evidence
- Resolving an incident when a normal state is processed

The test is useful for verifying selected response-engine behaviours. It does not establish the detector's accuracy against real-world cyberattacks.

Functional testing and quantitative machine-learning evaluation are different activities and should be reported separately.

## 11. Limitations

The current prototype has several limitations:

1. Anomaly detection can produce false positives and false negatives.
2. Unusual behaviour does not necessarily indicate malicious activity.
3. The effectiveness of the model depends on its training data, feature processing, and configuration.
4. Quantitative performance must be established using an appropriate evaluation dataset.
5. Simulated response actions do not provide actual host containment or recovery.
6. Monitoring coverage is limited to the metrics and event sources implemented.
7. CSV and JSON records depend on the availability and integrity of local application files.
8. Further testing is needed to establish performance, reliability, and behaviour under more diverse conditions.

## 12. Future Improvements

Potential improvements include:

- Evaluating the detector using labelled test data.
- Calculating precision, recall, F1-score, and false-positive rate.
- Comparing Isolation Forest with alternative anomaly-detection methods.
- Improving feature selection and model-threshold calibration.
- Expanding event correlation and evidence analysis.
- Adding automated unit and integration tests.
- Improving error handling and data validation.
- Producing additional visualisations and evaluation reports.
- Exploring safely controlled response integrations in an isolated test environment.

## 13. Conclusion

The Digital Immune System demonstrates how system monitoring, unsupervised machine learning, risk assessment, incident management, evidence collection, and visualisation can be combined into a cybersecurity-oriented prototype.

The implementation demonstrates a workflow for identifying unusual system behaviour, tracking incidents, and recording simulated responses. Further quantitative evaluation and broader testing are necessary before making claims about real-world cyberattack-detection effectiveness.

The project provides a foundation for exploring intelligent security monitoring and automated incident-response concepts in an educational research setting.