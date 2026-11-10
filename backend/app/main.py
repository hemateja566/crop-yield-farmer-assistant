from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Crop Yield & Farmer Advisory API",
    description="AI-powered crop yield prediction and farmer advisory platform",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routes import auth, farms, prediction, chatbot

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(farms.router, prefix="/farms", tags=["Farms"])
app.include_router(prediction.router, prefix="/predict", tags=["Prediction"])
app.include_router(chatbot.router, prefix="/chat", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Crop Yield & Farmer Advisory API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}