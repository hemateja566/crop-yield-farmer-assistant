from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.database.connection import db, Farmer, FarmerRegistration
from app.config import SUPPORTED_LANGUAGES

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_farmer(
    name: str,
    email: str,
    phone: Optional[str] = None,
    preferred_language: str = "en",
    location: Optional[str] = None,
    db_session=db,
):
    """Register a new farmer."""
    # Check if farmer already exists
    existing = await db_session.fetch(
        "SELECT id FROM farmers WHERE email = $1", email
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farmer with this email already registered",
        )
    
    # Register as farmer_registration (pending verification)
    registration = FarmerRegistration(
        name=name,
        email=email,
        phone=phone,
        preferred_language=preferred_language,
        location=location,
    )
    
    await db_session.execute(
        """
        INSERT INTO farmer_registrations (name, email, phone, preferred_language, location)
        VALUES ($1, $2, $3, $4, $5)
        """,
        name, email, phone, preferred_language, location,
    )
    
    return {
        "message": "Registration successful. Please verify your account.",
        "registration_id": registration.id,
    }


@router.post("/login")
async def login_farmer(
    email: str,
    password: str,  # In production, verify hashed password
    db_session=db,
):
    """Authenticate farmer login."""
    # For demo purposes - in production, verify password hash
    user = await db_session.fetchrow(
        "SELECT id, name, email, preferred_language FROM farmers WHERE email = $1",
        email,
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found. Please register first.",
        )
    
    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "preferred_language": user["preferred_language"],
        },
    }


@router.get("/me")
async def get_current_farmer(db_session=db):
    """Get current farmer profile."""
    # In a real app, this would use auth token
    # For demo, return a default farmer
    return {
        "id": 1,
        "name": "Sample Farmer",
        "email": "farmer@example.com",
        "preferred_language": "en",
    }