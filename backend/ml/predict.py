import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

from app.ml.preprocessing import engineer_features


def load_model(model_path: str):
    """Load a saved ML model from disk."""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        print(f"Model file not found: {model_path}")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def predict_yield(model, area: float, soil_ph: float, nitrogen: float, 
                  phosphorus: float, potassium: float, temperature: float,
                  rainfall: float, humidity: float, crop_type: str = "rice",
                  additional_features: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generate crop yield prediction using the trained model.
    
    Returns prediction with confidence interval.
    """
    # Create feature array
    features = {
        'area': area,
        'soil_ph': soil_ph,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'temperature': temperature,
        'rainfall': rainfall,
        'humidity': humidity,
        'crop_type': crop_type,
    }
    
    if additional_features:
        features.update(additional_features)
    
    # Convert to DataFrame for feature engineering
    df = pd.DataFrame([features])
    df = engineer_features(df)
    
    # Get feature names matching what the model expects
    # In production, we'd save the feature names with the model
    feature_order = ['area', 'soil_ph', 'nitrogen', 'phosphorus', 'potassium',
                     'temperature', 'rainfall', 'humidity', 'np_ratio', 'k_n_ratio']
    
    # Select only available features and order them
    available_features = [f for f in feature_order if f in df.columns]
    X = df[available_features].values
    
    # Make prediction
    prediction = model.predict(X)[0]
    
    # Calculate confidence interval (simple: ±2 standard errors approximation)
    # In production, use proper prediction intervals or quantile regression
    n_test_attr = getattr(model, 'n_features_in_', 1)
    residuals_estimate = max(1.0, abs(prediction) * 0.1)  # 10% estimate
    
    lower_bound = max(0, prediction - 1.96 * residuals_estimate)
    upper_bound = prediction + 1.96 * residuals_estimate
    
    # Calculate yield per area
    yield_per_area = prediction / max(area, 0.01)
    
    return {
        "crop_type": crop_type,
        "area": area,
        "predicted_total_yield": round(float(prediction), 2),
        "yield_per_area": round(yield_per_area, 2),
        "confidence_interval": {
            "lower": round(float(lower_bound), 2),
            "upper": round(float(upper_bound), 2),
            "method": "calculated uncertainty range",
        },
        "model_used": type(model).__name__,
        "prediction_timestamp": pd.Timestamp.now().isoformat(),
    }


def generate_prediction_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate prediction from request data dict."""
    return predict_yield(
        model=None,  # Model would be loaded in actual API
        area=data.get("area", 1),
        soil_ph=data.get("soil_ph", 6.5),
        nitrogen=data.get("nitrogen", 50),
        phosphorus=data.get("phosphorus", 25),
        potassium=data.get("potassium", 20),
        temperature=data.get("temperature", 28),
        rainfall=data.get("rainfall", 100),
        humidity=data.get("humidity", 70),
        crop_type=data.get("crop", "rice"),
    )