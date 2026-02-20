# 🚀 Predictive Vendor Consistency Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

**The Problem:** Delivery Hero's delivery chain breaks when restaurant preparation times are unpredictable. This project implements a real-time inference service to predict "Food Prep Time" variance.

## 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **ML Framework:** XGBoost, Scikit-Learn
*   **Deployment:** FastAPI, Uvicorn, Docker
*   **Monitoring:** Latency benchmarking (TTFT) and P99 tail latencies

## 📈 Impact Metrics (Simulated)

*   **AUC Improvement:** 4% via feature engineering of "unpredictable actors"
*   **Latency:** Sub-200ms response time using asynchronous gRPC-style calls
*   **Reliability:** 100% environment parity using multi-stage Docker builds

## 📂 Structure

```text
├── app/
│   ├── main.py          # FastAPI application (Async)
│   ├── model.py         # XGBoost inference logic
│   └── schemas.py       # Pydantic data validation
├── data/
│   └── features.sql     # Sample BigQuery feature engineering script
├── notebooks/
│   └── exploration.ipynb # Model training & Interpretability (SHAP/AIC)
├── tests/               # Unit tests for API endpoints
├── Dockerfile           # Production-grade containerization
└── requirements.txt     # Strict versioning
```

## 🚀 Quick Start

### Local Development

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Service:**
    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Test Prediction:**
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/predict/prep-time' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "vendor_id": 12345,
      "order_hour": 19,
      "day_of_week": 4,
      "item_count": 3,
      "is_peak_hour": true,
      "historical_delay_avg": 5.2
    }'
    ```

### Docker Deployment

1.  **Build Image:**
    ```bash
    docker build -t vendor-predictor .
    ```

2.  **Run Container:**
    ```bash
    docker run -p 8000:8000 vendor-predictor
    ```

## 🧠 Model Logic
We use **XGBoost** for initial rollout to prioritize interpretability. Stakeholders need to see feature importance (e.g., historical vendor delay) before moving to black-box PyTorch models.
