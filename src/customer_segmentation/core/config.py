"""
Configuration and constants for the customer segmentation project.
"""

SEGMENT_DESCRIPTIONS = {
    0: {
        "name": "Low-Value Customers",
        "description": "Customers with low income and low spending",
        "characteristics": {
            "avg_income": 34393.72,
            "avg_spending": 117.15,
            "avg_web_purchases": 2.18,
            "avg_store_purchases": 3.32
        }
    },
    1: {
        "name": "Premium Customers",
        "description": "High-income, high-spending customers with frequent purchases",
        "characteristics": {
            "avg_income": 77137.73,
            "avg_spending": 1270.85,
            "avg_web_purchases": 4.44,
            "avg_store_purchases": 8.43
        }
    },
    2: {
        "name": "Occasional Buyers",
        "description": "Low-spending customers with high recency (inactive)",
        "characteristics": {
            "avg_income": 36715.75,
            "avg_spending": 136.26,
            "avg_web_purchases": 2.42,
            "avg_store_purchases": 3.50
        }
    },
    3: {
        "name": "Active High-Value",
        "description": "Active customers with good income and high spending",
        "characteristics": {
            "avg_income": 60153.42,
            "avg_spending": 893.99,
            "avg_web_purchases": 7.61,
            "avg_store_purchases": 8.03
        }
    }
}

MODEL_FILENAMES = {
    "scaler": "customer_segmentation_scaler.pkl",
    "kmeans": "customer_segmentation_kmeans_model.pkl",
    "features": "customer_segmentation_features.pkl"
}
