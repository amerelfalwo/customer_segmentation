# Customer Segmentation System

A professional customer segmentation system using **K-Means Clustering**, designed to analyze customer behavior and categorize them into distinct groups to help marketing teams make data-driven decisions.

## 🚀 Project Overview
This project is an end-to-end solution covering data analysis, machine learning modeling, and deployment via a high-performance **FastAPI**. It leverages modern tools like `Python 3.12` and `uv` for efficient dependency management.

---

## 🛠️ Project Workflow

### 1. Data Analysis & Preparation
Data processing and exploration are handled in `analysisi.ipynb`, including:
- **Feature Engineering**: Transforming raw data into meaningful metrics:
    - Calculated `age` from birth year.
    - Derived `total_spent` by aggregating various spending categories.
- **Feature Selection**: Focused on key drivers of behavior: `Income`, `total_spent`, `age`, `NumWebPurchases`, `NumStorePurchases`, `NumWebVisitsMonth`, and `Recency`.
- **Data Preprocessing**: Handling outliers and missing values to ensure model stability.

### 2. Modeling
- **Scaling**: Used `StandardScaler` to normalize features, which is critical for distance-based algorithms like K-Means.
- **Clustering**: Implemented **K-Means Clustering** to segment customers into **4 optimal clusters**.
- **Serialization**: Saved the trained model, scaler, and feature metadata using `joblib` for reliable and fast loading in production.

### 3. Service Layer
The `ModelService` in `src/customer_segmentation/services/model_service.py` handles:
- Automatic model loading on application startup.
- Real-time preprocessing and prediction for new customer data.
- Returning detailed segment descriptions and confidence scores.

---

## 💻 Project Structure
```text
customer_segmentation/
├── models/               # Serialized model files (joblib)
├── src/
│   └── customer_segmentation/
│       ├── api/         # FastAPI implementation and routes
│       ├── core/        # Configuration, schemas, and constants
│       ├── services/    # Business logic and model management
│       └── cli/         # Command-line interface
├── analysisi.ipynb      # Data analysis and training notebook
└── pyproject.toml       # Dependency management (uv)
```

---

## 🔌 API Documentation

### 1. Health Check
- **Endpoint**: `GET /health`
- **Description**: Verifies if the API is running and the models are successfully loaded.

### 2. Single Prediction
- **Endpoint**: `POST /api/v1/predict`
- **Request Body (JSON)**:
```json
{
  "age": 35,
  "Income": 55000,
  "total_spent": 1200,
  "NumWebPurchases": 4,
  "NumStorePurchases": 6,
  "NumWebVisitsMonth": 5,
  "Recency": 15
}
```

### 3. Batch Prediction
- **Endpoint**: `POST /api/v1/batch_predict`
- **Description**: Process a list of customers and receive their segments in a single request.

### 4. Segment Information
- **Endpoint**: `GET /api/v1/segments`
- **Description**: Retrieve detailed descriptions and characteristics of all 4 customer segments.

---

## ⚙️ Installation & Usage

### Prerequisites
- Python 3.12+
- `uv` (recommended for dependency management)

### Setup
```bash
uv sync
```

### Start the API Server
```bash
uv run segmentation-api
```

### Use the CLI for Quick Predictions
```bash
uv run segmentation-cli predict <age> <income> <spent> <web_purchases> <store_purchases> <visits> <recency>
```

---

## 💡 Customer Segments
1. **Low-Value**: Low income and low spending.
2. **Premium Customers**: High income and very high spending.
3. **Occasional Buyers**: Currently inactive or infrequent customers.
4. **Active High-Value**: Frequent buyers with solid income/spending.

---
*Developed with a focus on performance, security, and scalability.*
