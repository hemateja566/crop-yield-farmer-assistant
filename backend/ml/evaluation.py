import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score


def calculate_metrics(y_true, y_pred) -> dict:
    """Calculate evaluation metrics for regression model."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    # MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1e-10))) * 100
    
    return {
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4),
        "mape": round(float(mape), 2),
    }


def model_comparison(results: dict) -> dict:
    """Compare multiple model results."""
    comparison = {}
    for model_name, result in results.items():
        comparison[model_name] = calculate_metrics(result["y_true"], result["y_pred"])
    
    # Find best model by R²
    best_model = max(results.keys(), key=lambda k: results[k]["r2"])
    
    return {
        "individual_metrics": comparison,
        "best_model": best_model,
        "best_r2": comparison[best_model]["r2"],
    }


def print_metrics(metrics: dict, title: str = "Model Evaluation"):
    """Print metrics in a readable format."""
    print(f"\n{title}")
    print(f"{'='*50}")
    print(f"MAE: {metrics['mae']}")
    print(f"RMSE: {metrics['rmse']}")
    print(f"R² Score: {metrics['r2']}")
    print(f"MAPE: {metrics['mape']}%")


def analyze_residuals(y_true, y_pred, feature_names: list = None) -> dict:
    """Analyze prediction residuals for patterns."""
    residuals = y_true - y_pred
    
    analysis = {
        "mean_residual": float(np.mean(residuals)),
        "median_residual": float(np.median(residuals)),
        "residual_std": float(np.std(residuals)),
        "max_positive_residual": float(np.max(residuals)),
        "max_negative_residual": float(np.min(residuals)),
    }
    
    # Check for patterns in residuals
    if feature_names:
        # Simple analysis: are errors larger for certain ranges?
        analysis["residual_range"] = {
            "positive": float(np.sum(residuals > 0)),
            "negative": float(np.sum(residuals < 0)),
        }
    
    return analysis