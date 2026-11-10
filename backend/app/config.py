import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "saved_models"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Database settings
POSTGRES_URL = os.getenv(
    "POSTGRES_URL", 
    f"postgresql://postgres:postgres@db:5432/crop_yield"
)

# Redis settings
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# External APIs
OPEN_METEO_BASE = "https://api.open-meteo.com/v1"
SOILGRIDS_BASE = "https://rest.soilgrids.org"

# ML settings
MODEL_DIR = MODELS_DIR
DEFAULT_MODEL = "random_forest"  # or "xgboost"

# Supported crops
SUPPORTED_CROPS = [
    "rice", "wheat", "maize", "cotton", "sugarcane",
    "paddy", "barley", "potato", "onion", "tomato"
]

# Languages
SUPPORTED_LANGUAGES = ["en", "te", "hi"]  # English, Telugu, Hindi