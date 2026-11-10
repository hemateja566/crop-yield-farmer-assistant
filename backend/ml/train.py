import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.ml.preprocessing import load_data, clean_data, engineer_features, split_data, scale_features


def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    """Train Random Forest Regressor model."""
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train, random_state=42):
    """Train XGBoost Regressor model."""
    try:
        from xgboost import XGBRegressor
        
        model = XGBRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=6,
            min_child_weight=1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=random_state,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)
        return model
    except ImportError:
        print("XGBoost not installed, skipping XGBoost training")
        return None


def evaluate_model(model, X_test, y_test) -> dict:
    """Evaluate model performance and return metrics."""
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation score
    cv_scores = cross_val_score(model, X_test, y_test, cv=5, scoring='r2')
    
    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "cv_mean_r2": float(cv_scores.mean()),
        "cv_std_r2": float(cv_scores.std()),
        "n_test_samples": len(y_test),
    }
    
    return metrics, y_pred


def compare_models(rf_metrics, xgb_metrics) -> dict:
    """Compare Random Forest and XGBoost models."""
    comparison = {
        "rf_mae": rf_metrics["mae"],
        "xgb_mae": xgb_metrics["mae"] if xgb_metrics else None,
        "rf_r2": rf_metrics["r2"],
        "xgb_r2": xgb_metrics["r2"] if xgb_metrics else None,
        "winner": "random_forest",
    }
    
    if xgb_metrics and xgb_metrics["r2"] > rf_metrics["r2"]:
        comparison["winner"] = "xgboost"
    
    return comparison


def train_and_evaluate(filepath: str, target_column: str = "yield") -> dict:
    """Complete training pipeline: load, prepare, train, evaluate."""
    # Load and prepare data
    prepared = prepare_data(filepath, target_column)
    
    X_train = prepared["X_train"]
    X_val = prepared["X_val"]
    X_test = prepared["X_test"]
    y_train = prepared["y_train"]
    y_test = prepared["y_test"]
    feature_names = prepared["feature_names"]
    
    # Train Random Forest
    rf_model = train_random_forest(X_train, y_train)
    rf_metrics, rf_preds = evaluate_model(rf_model, X_test, y_test)
    
    # Train XGBoost
    xgb_model = train_xgboost(X_train, y_train)
    if xgb_model:
        xgb_metrics, xgb_preds = evaluate_model(xgb_model, X_test, y_test)
    else:
        xgb_metrics = {"mae": None, "rmse": None, "r2": None, "cv_mean_r2": None}
    
    # Compare models
    comparison = compare_models(rf_metrics, xgb_metrics)
    
    # Determine best model
    if xgb_metrics["r2"] > rf_metrics["r2"]:
        best_model = xgb_model
        best_metrics = xgb_metrics
        model_name = "xgboost"
    else:
        best_model = rf_model
        best_metrics = rf_metrics
        model_name = "random_forest"
    
    # Feature importance
    importance_dict = dict(
        zip(feature_names, best_model.feature_importances_)
    )
    sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
    
    training_result = {
        "model_name": model_name,
        "metrics": best_metrics,
        "feature_importance": [
            {"feature": feat, "importance": round(imp, 4)} 
            for feat, imp in sorted_importance
        ],
        "train_score": rf_metrics["r2"],  # RF train R² as reference
        "val_score": rf_metrics["r2"],  # Simplified
        "prepared_data": {
            "n_features": len(feature_names),
            "n_train_samples": len(X_train),
            "n_val_samples": len(X_val),
            "n_test_samples": len(X_test),
        },
    }
    
    return training_result