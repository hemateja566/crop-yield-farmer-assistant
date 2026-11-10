from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.connection import db, Farmer, Farm, CropHistory
from app.config import SUPPORTED_CROPS

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_farm(
    farmer_id: int,
    name: Optional[str] = None,
    district: Optional[str] = None,
    village: Optional[str] = None,
    area_acres: float = 1,
    soil_type: Optional[str] = None,
    irrigation_available: bool = False,
    crop_type: Optional[str] = None,
    sowing_date: Optional[str] = None,
    gps_latitude: Optional[float] = None,
    gps_longitude: Optional[float] = None,
    db_session=db,
):
    """Register a new farm."""
    # Verify farmer exists
    farmer = await db_session.fetchrow(
        "SELECT id, name FROM farmers WHERE id = $1", farmer_id
    )
    
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer not found",
        )
    
    # Calculate area in hectares if acres provided
    area_hectares = round(area_acres * 0.4047, 2)
    
    # Create farm
    farm = Farm(
        farmer_id=farmer_id,
        name=name or f"Farm {farmer_id}",
        district=district,
        village=village,
        area_acres=area_acres,
        area_hectares=area_hectares,
        soil_type=soil_type,
        irrigation_available=irrigation_available,
        crop_type=crop_type,
        sowing_date=sowing_date,
        gps_latitude=gps_latitude,
        gps_longitude=gps_longitude,
    )
    
    await db_session.execute(
        """
        INSERT INTO farms (farmer_id, name, district, village, area_acres, area_hectares,
                          soil_type, irrigation_available, crop_type, sowing_date,
                          gps_latitude, gps_longitude)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """,
        farmer_id, farm.name, district, village, area_acres, area_hectares,
        soil_type, irrigation_available, crop_type, sowing_date,
        gps_latitude, gps_longitude,
    )
    
    return farm.to_dict()


@router.get("/{farm_id}")
async def get_farm(farm_id: int, db_session=db):
    """Get farm information."""
    farm = await db_session.fetchrow(
        """
        SELECT f.*, fr.preferred_language, fr.name as farmer_name
        FROM farms f
        JOIN farmers fr ON f.farmer_id = fr.id
        WHERE f.id = $1
        """,
        farm_id,
    )
    
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )
    
    return dict(farm)


@router.get("/", response_model=List[dict])
async def list_farms(
    farmer_id: Optional[int] = None,
    db_session=db,
):
    """List farms, optionally filtered by farmer."""
    if farmer_id:
        farms = await db_session.fetch(
            """
            SELECT f.*, fr.name as farmer_name, fr.preferred_language
            FROM farms f
            JOIN farmers fr ON f.farmer_id = fr.id
            WHERE f.farmer_id = $1
            """,
            farmer_id,
        )
    else:
        farms = await db_session.fetch(
            """
            SELECT f.*, fr.name as farmer_name, fr.preferred_language
            FROM farms f
            JOIN farmers fr ON f.farmer_id = fr.id
            """,
        )
    
    return [dict(f) for f in farms]


@router.put("/{farm_id}")
async def update_farm(
    farm_id: int,
    area_acres: Optional[float] = None,
    soil_type: Optional[str] = None,
    irrigation_available: Optional[bool] = None,
    crop_type: Optional[str] = None,
    db_session=db,
):
    """Update farm information."""
    # Check existing farm
    existing = await db_session.fetchrow(
        "SELECT * FROM farms WHERE id = $1", farm_id
    )
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )
    
    # Build update query dynamically
    update_fields = []
    params = []
    param_count = 0
    
    if area_acres is not None:
        area_hectares = round(area_acres * 0.4047, 2)
        update_fields.append(f"area_acres = ${param_count + 1}, area_hectares = ${param_count + 2}")
        params.extend([area_acres, area_hectares])
        param_count += 2
    
    if soil_type is not None:
        update_fields.append(f"soil_type = ${param_count + 1}")
        params.append(soil_type)
        param_count += 1
    
    if irrigation_available is not None:
        update_fields.append(f"irrigation_available = ${param_count + 1}")
        params.append(irrigation_available)
        param_count += 1
    
    if crop_type is not None:
        update_fields.append(f"crop_type = ${param_count + 1}")
        params.append(crop_type)
        param_count += 1
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )
    
    params.append(farm_id)
    query = f"UPDATE farms SET {', '.join(update_fields)} WHERE id = ${param_count + 1}"
    
    await db_session.execute(query, *params)
    
    return {"message": "Farm updated successfully", "farm_id": farm_id}


@router.post("/{farm_id}/history")
async def add_crop_history(
    farm_id: int,
    crop_type: str,
    yield_per_acre: float,
    total_yield: Optional[float] = None,
    sowing_date: Optional[str] = None,
    harvest_date: Optional[str] = None,
    notes: Optional[str] = None,
    db_session=db,
):
    """Add crop yield history record."""
    # Check farm exists
    farm = await db_session.fetchrow("SELECT id FROM farms WHERE id = $1", farm_id)
    if not farm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farm not found",
        )
    
    # Calculate total yield if not provided
    if total_yield is None and area_acres := existing.get("area_acres"):
        total_yield = yield_per_acre * area_acres
    
    await db_session.execute(
        """
        INSERT INTO crop_history (farm_id, crop_type, yield_per_acre, total_yield,
                                  sowing_date, harvest_date, notes)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        """,
        farm_id, crop_type, yield_per_acre, total_yield,
        sowing_date, harvest_date, notes,
    )
    
    return {"message": "Crop history recorded successfully"}


@router.get("/{farm_id}/history")
async def get_crop_history(farm_id: int, db_session=db):
    """Get crop history for a farm."""
    history = await db_session.fetch(
        """
        SELECT * FROM crop_history
        WHERE farm_id = $1
        ORDER BY created_at DESC
        """,
        farm_id,
    )
    
    return [dict(h) for h in history]


@router.get("/crops")
async def get_supported_crops():
    """Get list of supported crops."""
    return {
        "crops": SUPPORTED_CROPS,
        "total": len(SUPPORTED_CROPS),
    }