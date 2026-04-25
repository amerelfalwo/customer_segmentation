"""
Service for loading models and performing segmentation.
"""

import os
import joblib
import numpy as np
from typing import List, Optional
from ..core.config import SEGMENT_DESCRIPTIONS, MODEL_FILENAMES
from ..core.schemas import CustomerInput, SegmentationResponse

class ModelService:
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.scaler = None
        self.kmeans = None
        self.features = None

    def load_models(self):
        """Load trained models from the models directory."""
        try:
            scaler_path = os.path.join(self.models_dir, MODEL_FILENAMES["scaler"])
            kmeans_path = os.path.join(self.models_dir, MODEL_FILENAMES["kmeans"])
            features_path = os.path.join(self.models_dir, MODEL_FILENAMES["features"])

            # Check if paths exist relative to current working directory or absolute
            # If not found, try to look relative to the project root
            for path in [scaler_path, kmeans_path, features_path]:
                if not os.path.exists(path):
                    # Fallback: try to find the project root
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
                    scaler_path = os.path.join(project_root, "models", MODEL_FILENAMES["scaler"])
                    kmeans_path = os.path.join(project_root, "models", MODEL_FILENAMES["kmeans"])
                    features_path = os.path.join(project_root, "models", MODEL_FILENAMES["features"])
                    break

            self.scaler = joblib.load(scaler_path)
            self.kmeans = joblib.load(kmeans_path)
            self.features = joblib.load(features_path)
            
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False

    def is_ready(self) -> bool:
        return self.scaler is not None and self.kmeans is not None

    def predict(self, customer: CustomerInput) -> SegmentationResponse:
        """Predict customer segment."""
        if not self.is_ready():
            raise RuntimeError("Models not loaded")

        # Prepare input data
        customer_data = np.array([[
            customer.age,
            customer.Income,
            customer.total_spent,
            customer.NumWebPurchases,
            customer.NumStorePurchases,
            customer.NumWebVisitsMonth,
            customer.Recency
        ]])
        
        # Scale input
        customer_scaled = self.scaler.transform(customer_data)
        
        # Predict cluster
        cluster = self.kmeans.predict(customer_scaled)[0]
        
        # Calculate confidence
        distances = np.linalg.norm(
            customer_scaled[0] - self.kmeans.cluster_centers_, axis=1
        )
        min_distance = distances.min()
        max_distance = distances.max()
        
        confidence = 1 - (min_distance / (max_distance + 1e-10))
        confidence = max(0, min(1, confidence))
        
        segment_info = SEGMENT_DESCRIPTIONS[int(cluster)]
        
        return SegmentationResponse(
            cluster=int(cluster),
            segment_name=segment_info["name"],
            description=segment_info["description"],
            characteristics=segment_info["characteristics"],
            confidence_score=round(float(confidence), 3)
        )

    def batch_predict(self, customers: List[CustomerInput]) -> List[SegmentationResponse]:
        """Predict segments for multiple customers."""
        return [self.predict(c) for c in customers]
