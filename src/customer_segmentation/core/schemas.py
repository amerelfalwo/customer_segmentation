"""
Pydantic schemas for the customer segmentation API.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class CustomerInput(BaseModel):
    age: float = Field(..., description="Customer age in years")
    Income: float = Field(..., description="Annual income")
    total_spent: float = Field(..., description="Total spending amount")
    NumWebPurchases: float = Field(..., description="Number of web purchases")
    NumStorePurchases: float = Field(..., description="Number of store purchases")
    NumWebVisitsMonth: float = Field(..., description="Number of web visits per month")
    Recency: float = Field(..., description="Days since last purchase")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 45,
                "Income": 50000,
                "total_spent": 500,
                "NumWebPurchases": 5,
                "NumStorePurchases": 8,
                "NumWebVisitsMonth": 6,
                "Recency": 30
            }
        }
    }

class SegmentationResponse(BaseModel):
    cluster: int
    segment_name: str
    description: str
    characteristics: Dict[str, float]
    confidence_score: float

class BatchSegmentationResponse(BaseModel):
    results: List[SegmentationResponse]
    total_processed: int
