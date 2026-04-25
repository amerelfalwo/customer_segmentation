"""
FastAPI application for Customer Segmentation
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from contextlib import asynccontextmanager

from ..core.schemas import (
    CustomerInput, 
    SegmentationResponse, 
    BatchSegmentationResponse
)
from ..core.config import SEGMENT_DESCRIPTIONS
from ..services.model_service import ModelService

# Initialize model service
model_service = ModelService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    success = model_service.load_models()
    if success:
        print("Models loaded successfully!")
    else:
        print("Warning: Models could not be loaded on startup.")
    yield

app = FastAPI(
    title="Customer Segmentation API",
    description="API for customer segmentation using K-Means clustering",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Customer Segmentation API is running",
        "endpoints": {
            "predict": "/api/v1/predict",
            "batch_predict": "/api/v1/batch_predict",
            "segments": "/api/v1/segments"
        }
    }

@app.get("/health", tags=["Health"])
async def health():
    """Detailed health check"""
    is_ready = model_service.is_ready()
    return {
        "status": "healthy" if is_ready else "unhealthy",
        "models_loaded": is_ready,
        "features": model_service.features,
        "n_clusters": model_service.kmeans.n_clusters if is_ready else None
    }

@app.get("/api/v1/segments", tags=["Information"])
async def get_segments():
    """Get information about all customer segments"""
    return SEGMENT_DESCRIPTIONS

@app.post("/api/v1/predict", response_model=SegmentationResponse, tags=["Prediction"])
async def predict(customer: CustomerInput):
    """Predict customer segment based on their characteristics"""
    if not model_service.is_ready():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        return model_service.predict(customer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/batch_predict", response_model=BatchSegmentationResponse, tags=["Prediction"])
async def batch_predict(customers: List[CustomerInput]):
    """Predict segments for multiple customers at once"""
    if not model_service.is_ready():
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if len(customers) == 0:
        raise HTTPException(status_code=400, detail="Empty customer list")
    
    if len(customers) > 1000:
        raise HTTPException(status_code=400, detail="Too many customers (max 1000)")
    
    try:
        results = model_service.batch_predict(customers)
        return BatchSegmentationResponse(
            results=results,
            total_processed=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
