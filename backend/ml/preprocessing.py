import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


def load_data(filepath: str) -> pd.DataFrame:
    """Load agricultural dataset from CSV file."""
    df = pd.read_csv(filepath)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess agricultural data."""
    # Handle missing values
    df = df.fillna({
        'nitrogen': df['nitrogen'].median(),
        'phosphorus': df['phosphorus'].median(),
        'potassium': df['potassium'].median(),
        'temperature': df['temperature'].median(),
        'rainfall': df['rainfall'].median(),
        'humidity': df['humidity'].median(),
    })
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Ensure correct data types
    numeric_cols = ['area', 'temperature', 'rainfall', 'humidity', 
                    'soil_ph', 'nitrogen', 'phosphorus', 'potassium']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features for ML model."""
    # Create interaction features
    if 'nitrogen' in df.columns and 'phosphorus' in df.columns:
        df['np_ratio'] = df['nitrogen'] / (df['phosphorus'] + 0.01)
    
    if 'potassium' in df.columns and 'nitrogen' in df.columns:
        df['k_n_ratio'] = df['potassium'] / (df['nitrogen'] + 0.01)
    
    # Area-based features
    if 'area' in df.columns and 'yield' in df.columns:
        df['yield_per_area'] = df['yield'] / (df['area'] + 0.01)
    
    # Soil pH category
    if 'soil_ph' in df.columns:
        df['ph_category'] = pd.cut(
            df['soil_ph'], 
            bins=[0, 5.5, 6.5, 7.5, 14], 
            labels=['acidic', 'slightly_acidic', 'neutral', 'alkaline']
        )
    
    return df


def split_data(df: pd.DataFrame, target_column: str = "yield", 
               test_size: float = 0.2, val_size: float = 0.1) -> tuple:
    """Split data into train, validation, and test sets."""
    # First split: train+val vs test
    X = df.drop(columns=[target_column], errors='ignore')
    y = df[target_column]
    
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Second split: train vs val
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size / (1 - test_size), random_state=42
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def scale_features(X_train: pd.DataFrame, X_val: pd.DataFrame, X_test: pd.DataFrame) -> tuple:
    """Scale features using StandardScaler."""
    from sklearn.preprocessing import StandardScaler
    
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train), 
        columns=X_train.columns, 
        index=X_train.index
    )
    X_val_scaled = pd.DataFrame(
        scaler.transform(X_val), 
        columns=X_val.columns, 
        index=X_val.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test), 
        columns=X_test.columns, 
        index=X_test.index
    )
    
    return X_train_scaled, X_val_scaled, X_test_scaled


def prepare_data(filepath: str, target_column: str = "yield") -> dict:
    """Complete data preparation pipeline."""
    df = load_data(filepath)
    df = clean_data(df)
    df = engineer_features(df)
    
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df, target_column)
    
    X_train_scaled, X_val_scaled, X_test_scaled = scale_features(X_train, X_val, X_test)
    
    return {
        "X_train": X_train_scaled,
        "X_val": X_val_scaled,
        "X_test": X_test_scaled,
        "y_train": np.array(y_train),
        "y_val": np.array(y_val),
        "y_test": np.array(y_test),
        "feature_names": list(X_train.columns),
        "raw_train": df,
    }