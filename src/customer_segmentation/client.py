"""
Python client library for Customer Segmentation API
"""

import requests
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Customer:
    """Customer data class"""
    age: float
    Income: float
    total_spent: float
    NumWebPurchases: float
    NumStorePurchases: float
    NumWebVisitsMonth: float
    Recency: float

@dataclass
class SegmentationResult:
    """Segmentation result"""
    cluster: int
    segment_name: str
    description: str
    characteristics: Dict[str, float]
    confidence_score: float

class SegmentationClient:
    """Client for Customer Segmentation API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize client with API base URL"""
        self.base_url = base_url
        self.api_v1 = f"{base_url}/api/v1"
        self.session = requests.Session()

    def health(self) -> Dict[str, Any]:
        """Check API health"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def get_segments(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all customer segments"""
        response = self.session.get(f"{self.api_v1}/segments")
        response.raise_for_status()
        return response.json()

    def predict(self, customer: Customer) -> SegmentationResult:
        """Predict segment for a single customer"""
        data = {
            "age": customer.age,
            "Income": customer.Income,
            "total_spent": customer.total_spent,
            "NumWebPurchases": customer.NumWebPurchases,
            "NumStorePurchases": customer.NumStorePurchases,
            "NumWebVisitsMonth": customer.NumWebVisitsMonth,
            "Recency": customer.Recency
        }
        response = self.session.post(f"{self.api_v1}/predict", json=data)
        response.raise_for_status()
        result = response.json()
        return SegmentationResult(**result)

    def batch_predict(self, customers: List[Customer]) -> List[SegmentationResult]:
        """Predict segments for multiple customers"""
        data = [
            {
                "age": c.age,
                "Income": c.Income,
                "total_spent": c.total_spent,
                "NumWebPurchases": c.NumWebPurchases,
                "NumStorePurchases": c.NumStorePurchases,
                "NumWebVisitsMonth": c.NumWebVisitsMonth,
                "Recency": c.Recency
            }
            for c in customers
        ]
        response = self.session.post(f"{self.api_v1}/batch_predict", json=data)
        response.raise_for_status()
        result = response.json()
        return [SegmentationResult(**r) for r in result["results"]]
