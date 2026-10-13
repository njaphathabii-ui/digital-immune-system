# Digital Immune System
## Testing and Evaluation

## 1. Introduction

This document records the functional testing and observed behaviour of the Digital Immune System prototype.

The project combines system monitoring, machine-learning anomaly detection, risk assessment, incident management, simulated response actions, evidence collection, and dashboard visualisation.

The purpose of testing is to establish whether the implemented components perform their intended functions and to identify areas that require further evaluation.

Functional testing and quantitative evaluation of machine-learning performance are treated separately.

## 2. Testing Environment

The project was developed and tested using the following environment:

| Item | Environment |
|---|---|
| Operating system | Windows 11 |
| Programming language | Python |
| Development environment | Visual Studio Code |
| Virtual environment | Python virtual environment |
| Machine-learning library | scikit-learn |
| System monitoring library | psutil |
| Dashboard framework | Streamlit |
| Data storage | CSV and JSON files |

The project uses a trained Isolation Forest model and a corresponding feature-scaling artifact stored in the `models/` directory.

## 3. Functional Test Cases

The following test cases describe the principal behaviours demonstrated by the project. The observed results are based on the previously run prototype and the available terminal and dashboard screenshots.

| Test ID | Component | Test procedure | Expected behaviour | Observed result |
|---|---|---|---|---|
| TC-01 | System monitoring | Run `monitoring/system_monitor.py` | Collect and save system metrics | Monitoring output and populated CSV records were observed |
| TC-02 | Feature engineering | Run `detection/feature_engineering.py` | Clean data and select numerical features | The implementation and prepared dataset were inspected |
| TC-03 | Anomaly detection | Run `detection/realtime_detector.py` | Process monitoring records and produce detection results | Detection output and saved results were observed |
| TC-04 | Dashboard | Run `streamlit run dashboard/dashboard.py` | Display status, risk, severity, and system metrics | Dashboard opened and displayed the monitoring interface |
| TC-05 | Incident creation | Process a qualifying detection | Create and record an incident | Incident creation was observed in response-engine output |
| TC-06 | Severity handling | Process higher-severity test detections | Apply the configured severity and response logic | HIGH and CRITICAL incident outputs were observed |
| TC-07 | Evidence collection | Process a qualifying incident | Save incident evidence as JSON | JSON evidence files were observed |
| TC-08 | Incident resolution | Process a normal-state detection | Resolve an incident according to the configured logic | Incident resolution was observed in test output |

These tests provide evidence of selected functional behaviours. They do not prove that every possible input or failure condition has been tested.

## 4. Monitoring and Data Validation

The monitoring component writes observations to `data/system_metrics.csv`.

During inspection, the file contained 15,388 records. The inspected dataset contained fields for timestamps, system resource usage, process counts, network traffic, packet counts, and connection states.

The feature-engineering workflow reads the monitoring dataset and produces `data/prepared_dataset.csv`. The prepared dataset contained 14,250 records during inspection.

The detection-results file contained 14,907 records, and the incident log contained 2,890 records at the time of inspection.

These counts describe the files at that point in time. They should not be interpreted as a single one-to-one processing sequence because the files may have been generated or updated at different times.

The feature-engineering implementation removes invalid timestamps, duplicate rows, invalid numerical values, and negative feature values before saving the selected features.

## 5. Anomaly Detection Observations

The real-time detection terminal displayed system metrics, a risk score, a severity classification, and the leading indicators associated with an observation.

One captured output reported:

- CPU usage: 16.60%
- Memory usage: 90.60%
- Disk usage: 84.10%
- Running processes: 375
- Risk score: 51.44/100
- Status: NORMAL
- Severity: NORMAL

The output also listed disk usage and packet counts among the leading indicators.

This example demonstrates the detector's reporting interface. It does not establish that the observation was malicious or that the model has a particular detection accuracy.

A risk score and a severity label are separate outputs and must be interpreted according to the implementation's configured rules.

## 6. Incident Escalation and Response Testing

The controlled escalation test is implemented in `testing/escalation_test.py`.

Previously observed test output demonstrated incident creation, response processing, evidence collection, and incident resolution.

The response engine also displayed higher-severity incidents with simulated containment labels.

The tested workflow included:

1. Processing a predefined detection.
2. Opening an incident.
3. Recording a response action.
4. Collecting evidence for a qualifying incident.
5. Processing a subsequent normal-state detection.
6. Marking the incident resolved.

The prototype simulates containment rather than performing actual operating-system or network changes.

The controlled test verifies selected incident-response behaviours. It does not establish the effectiveness of real containment mechanisms.

## 7. Evidence Collection Testing

The project stores incident evidence as JSON files in the `evidence/` directory.

An inspected evidence record included:

- Incident identifier
- Timestamp
- Risk score and severity
- Incident status
- Response label
- Detection count
- Highest recorded risk score
- System observation values
- Evidence collection status

The inspected example showed a HIGH-severity incident with a risk score of 70.0 and an evidence status of `COLLECTED`.

This demonstrates that structured incident information can be saved for later inspection. It should not be described as proof of a real cyberattack or a complete forensic investigation.

## 8. Dashboard Testing

The Streamlit dashboard was previously run and inspected.

The captured interface displayed:

- Current security status
- Risk score
- Severity
- Intelligent response information
- Live system resource measurements
- Latest detection information
- System activity visualisation

The dashboard provided a consolidated view of the monitoring and response information.

The captured example displayed a NORMAL status with a risk score of approximately 51.27/100. This is an example of the displayed output, not a universal threshold or proof that all system activity was benign.

## 9. Quantitative Model Evaluation

A formal quantitative evaluation has not yet been established by the functional tests documented above.

To assess detection performance, the model should be evaluated using a suitable labelled dataset containing normal and anomalous observations.

Recommended metrics include:

### 9.1 Precision

Precision measures the proportion of observations predicted as anomalous that are actually anomalous.

\[
\text{Precision}=\frac{TP}{TP+FP}
\]

### 9.2 Recall

Recall measures the proportion of actual anomalous observations correctly identified by the model.

\[
\text{Recall}=\frac{TP}{TP+FN}
\]

### 9.3 F1-score

The F1-score combines precision and recall using their harmonic mean.

\[
F_1=2\frac{\text{Precision}\times\text{Recall}}
{\text{Precision}+\text{Recall}}
\]

### 9.4 False-positive rate

The false-positive rate measures the proportion of normal observations incorrectly classified as anomalous.

\[
\text{FPR}=\frac{FP}{FP+TN}
\]

Where:

- TP = true positives
- FP = false positives
- TN = true negatives
- FN = false negatives

These metrics should only be reported after running an appropriate evaluation. No numerical performance values are claimed in this document.

## 10. Limitations and Threats to Validity

The current results have several limitations:

1. Functional tests do not establish real-world attack-detection accuracy.
2. The absence of labelled ground truth prevents reliable calculation of classification metrics.
3. Unusual system behaviour can arise from legitimate applications or workloads.
4. The prepared dataset and detection-results file have different record counts, and their processing relationship requires further verification.
5. The incident-response test uses predefined scenarios and does not cover every possible operational condition.
6. Simulated containment does not demonstrate actual system isolation or recovery.
7. The inspected results represent the project state at the time of testing and may change as new records are collected.

These limitations should be considered when interpreting the results.

## 11. Recommended Additional Tests

Further testing should include:

- Testing malformed or incomplete monitoring records.
- Verifying model input columns and feature order.
- Testing the detector with labelled normal and anomalous data.
- Measuring precision, recall, F1-score, and false-positive rate.
- Testing incident behaviour across multiple sequential detections.
- Checking whether repeated incidents are grouped according to the intended logic.
- Verifying that evidence files contain valid and complete JSON.
- Checking dashboard behaviour when input files are empty or missing.
- Measuring resource usage during extended monitoring.
- Repeating tests to establish consistency.

## 12. Conclusion

The available test evidence demonstrates that the prototype can collect system metrics, produce anomaly-detection output, display monitoring information, manage selected incident-response scenarios, and record structured evidence.

The controlled tests support the functional feasibility of the implemented workflow. However, formal quantitative evaluation is still required to determine the model's detection performance.

Future work should prioritise labelled-data evaluation, false-positive analysis, broader test coverage, and stronger validation of the end-to-end data pipeline.