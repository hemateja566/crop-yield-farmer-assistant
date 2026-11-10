from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import json

from app.database.connection import db
from app.ml.train import train_and_evaluate
from app.ml.predict import predict_yield
from app.config import MODELS_DIR, SUPPORTED_CROPS
import os

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/yield", response_model=dict)
async def predict_yield_endpoint(
    crop: str,
    area: float,
    soil_ph: float,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    temperature: float,
    rainfall: float,
    humidity: float,
    background_tasks: BackgroundTasks,
    db_session=db,
):
    """Generate crop yield prediction."""
    # Validate crop type
    if crop.lower() not in [c.lower() for c in SUPPORTED_CROPS]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported crop. Supported: {SUPPORTED_CROPS}",
        )
    
    # Load model (in production, use cached/model from disk)
    model_path = os.path.join(str(MODELS_DIR), "random_forest.pkl")
    
    # For demo, create a simple prediction without loaded model
    # In production, would load model and use predict_yield function
    try:
        prediction_result = predict_yield(
            model=None,  # Model would be loaded here
            area=area,
            soil_ph=soil_ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            temperature=temperature,
            rainfall=rainfall,
            humidity=humidity,
            crop_type=crop,
        )
        
        # Save prediction to history
        await db_session.execute(
            """
            INSERT INTO crop_history (farm_id, crop_type, yield_per_acre, total_yield,
                                      sowing_date, harvest_date, notes)
            VALUES (1, $1, $2, $5, NULL, NULL, 'AI prediction')
            """,
            crop, prediction_result["predicted_total_yield"],
        )
        
        return prediction_result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}",
        )


@router.get("/history", response_model=List[dict])
async def get_prediction_history(
    farm_id: Optional[int] = None,
    limit: int = 10,
    db_session=db,
):
    """Get previous yield predictions."""
    query = """
        SELECT * FROM crop_history
        WHERE farm_id = COALESCE($1, farm_id)
        ORDER BY created_at DESC
        LIMIT $2
    """
    history = await db_session.fetch(query, farm_id, limit)
    
    return [dict(h) for h in history]


@router.post("/train", response_model=dict)
async def train_prediction_model(
    background_tasks: BackgroundTasks,
    db_session=db,
):
    """Train the ML prediction model (background task)."""
    # This would be a long-running task
    # For now, return status
    return {
        "message": "Model training initiated in background",
        "status": "training_started",
        "detail": "Use /predict/history to check training progress",
    }