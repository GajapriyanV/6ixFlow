"""
FastAPI Backend for Toronto Traffic Hotspot Prediction.

Serves ML predictions for traffic congestion and vehicle counts.
Loads trained models and provides REST API endpoints for the frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
import pandas as pd
import numpy as np
import joblib
import os
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Toronto Traffic Hotspot API",
    description="ML-powered traffic congestion prediction for Toronto road segments",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to store loaded models and data
models = {}
encoder = None
metadata = {}
road_segments_data = None

class PredictionRequest(BaseModel):
    """Request model for traffic predictions."""
    datetime: str = Field(
        ..., 
        description="ISO datetime string (e.g., '2024-10-03T17:00:00')",
        example="2024-10-03T17:00:00"
    )

class PredictionResponse(BaseModel):
    """Response model for traffic predictions."""
    centreline_id: int
    location_name: str
    longitude: float
    latitude: float
    congestion_level: str
    predicted_vehicles: int

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str
    models_loaded: bool
    road_segments_count: int

def load_models_and_data():
    """
    Load trained models, encoder, and metadata on startup.
    """
    global models, encoder, metadata, road_segments_data
    
    try:
        models_dir = "../ml/models"
        
        # Load models
        logger.info("Loading trained models...")
        models['classifier'] = joblib.load(os.path.join(models_dir, "rf_congestion_cls.joblib"))
        models['regressor'] = joblib.load(os.path.join(models_dir, "rf_volume_reg.joblib"))
        encoder = joblib.load(os.path.join(models_dir, "onehot_encoder.joblib"))
        metadata = joblib.load(os.path.join(models_dir, "training_metadata.joblib"))
        
        logger.info("Models loaded successfully!")
        logger.info(f"Classification model: {type(models['classifier'])}")
        logger.info(f"Regression model: {type(models['regressor'])}")
        logger.info(f"Encoder: {type(encoder)}")
        
        # Load road segments data for location mapping
        logger.info("Loading road segments data...")
        data_path = "../data/processed/svc_clean_2022_2024.csv"
        df = pd.read_csv(data_path)
        
        # Get unique road segments with their coordinates and names
        road_segments_data = df.groupby('centreline_id').agg({
            'location_name': 'first',
            'longitude': 'first', 
            'latitude': 'first'
        }).reset_index()
        
        logger.info(f"Loaded {len(road_segments_data)} unique road segments")
        logger.info(f"Date range in training data: {metadata['date_range']['start']} to {metadata['date_range']['end']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")
        return False

def prepare_features_for_prediction(dt: datetime) -> pd.DataFrame:
    """
    Prepare feature matrix for prediction at given datetime.
    """
    # Extract time features
    hour = dt.hour
    day_of_week = dt.weekday()  # 0=Monday, 6=Sunday
    month = dt.month
    is_weekend = 1 if day_of_week in [5, 6] else 0  # Saturday=5, Sunday=6
    
    # Create features for all road segments
    features_list = []
    for _, row in road_segments_data.iterrows():
        centreline_id = row['centreline_id']
        features_list.append({
            'hour': hour,
            'day_of_week': day_of_week,
            'month': month,
            'is_weekend': is_weekend,
            'centreline_id': centreline_id
        })
    
    # Convert to DataFrame
    features_df = pd.DataFrame(features_list)
    
    # Separate numerical and categorical features (same as training)
    numerical_features = ['hour', 'day_of_week', 'month', 'is_weekend']
    categorical_features = ['centreline_id']
    
    # Extract numerical features
    X_numerical = features_df[numerical_features].copy()
    
    # OneHotEncode centreline_id
    X_encoded = encoder.transform(features_df[categorical_features])
    
    # Get feature names for encoded data
    encoded_feature_names = [f"centreline_{id}" for id in encoder.categories_[0]]
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_feature_names, index=features_df.index)
    
    # Combine numerical and encoded features
    X_processed = pd.concat([X_numerical, X_encoded_df], axis=1)
    
    return X_processed

@app.on_event("startup")
async def startup_event():
    """Load models and data when the application starts."""
    logger.info("Starting Toronto Traffic Hotspot API...")
    success = load_models_and_data()
    if not success:
        logger.error("Failed to load models. API may not work correctly.")
    else:
        logger.info("API startup completed successfully!")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns API status and model information.
    """
    models_loaded = len(models) == 2 and encoder is not None
    road_segments_count = len(road_segments_data) if road_segments_data is not None else 0
    
    return HealthResponse(
        status="healthy" if models_loaded else "unhealthy",
        message="API is running" if models_loaded else "Models not loaded",
        models_loaded=models_loaded,
        road_segments_count=road_segments_count
    )

@app.post("/predict_at", response_model=List[PredictionResponse])
async def predict_traffic_at_time(request: PredictionRequest):
    """
    Predict traffic congestion and vehicle counts for all road segments at a specific time.
    
    Args:
        request: Contains datetime string for prediction
        
    Returns:
        List of predictions for all road segments with coordinates and congestion levels
    """
    try:
        # Check if models are loaded
        if not models or encoder is None or road_segments_data is None:
            raise HTTPException(
                status_code=503, 
                detail="Models not loaded. Please check /health endpoint."
            )
        
        # Parse datetime
        try:
            dt = datetime.fromisoformat(request.datetime.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid datetime format. Use ISO format: '2024-10-03T17:00:00'"
            )
        
        logger.info(f"Making predictions for datetime: {dt}")
        
        # Prepare features for all road segments
        X_processed = prepare_features_for_prediction(dt)
        
        # Make predictions
        congestion_predictions = models['classifier'].predict(X_processed)
        vehicle_predictions = models['regressor'].predict(X_processed)
        
        # Round vehicle predictions to integers
        vehicle_predictions = np.round(vehicle_predictions).astype(int)
        
        # Create response
        predictions = []
        for i, (_, row) in enumerate(road_segments_data.iterrows()):
            predictions.append(PredictionResponse(
                centreline_id=int(row['centreline_id']),
                location_name=row['location_name'],
                longitude=float(row['longitude']),
                latitude=float(row['latitude']),
                congestion_level=congestion_predictions[i],
                predicted_vehicles=int(vehicle_predictions[i])
            ))
        
        logger.info(f"Generated {len(predictions)} predictions")
        return predictions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/road_segments")
async def get_road_segments():
    """
    Get information about all available road segments.
    Useful for frontend to know which locations are available for prediction.
    """
    if road_segments_data is None:
        raise HTTPException(status_code=503, detail="Road segments data not loaded")
    
    return {
        "count": len(road_segments_data),
        "segments": road_segments_data.to_dict('records')
    }

@app.get("/model_info")
async def get_model_info():
    """
    Get information about the loaded models and training metadata.
    """
    if not metadata:
        raise HTTPException(status_code=503, detail="Model metadata not loaded")
    
    return {
        "training_date": metadata.get('training_date'),
        "data_shape": metadata.get('data_shape'),
        "date_range": metadata.get('date_range'),
        "unique_locations": metadata.get('unique_locations'),
        "classification_accuracy": metadata.get('classification_accuracy'),
        "regression_mae": metadata.get('regression_mae'),
        "regression_r2": metadata.get('regression_r2'),
        "feature_columns": metadata.get('feature_columns'),
        "classification_target": metadata.get('classification_target'),
        "regression_target": metadata.get('regression_target')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)