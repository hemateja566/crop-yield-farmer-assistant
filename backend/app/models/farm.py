from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database.connection import Base


class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, nullable=False, index=True)
    name = Column(String(200), nullable=True)
    location = Column(Text, nullable=True)
    district = Column(String(100), nullable=True)
    village = Column(String(100), nullable=True)
    gps_latitude = Column(Float, nullable=True)
    gps_longitude = Column(Float, nullable=True)
    area_acres = Column(Float, nullable=False)
    area_hectares = Column(Float, nullable=True)
    soil_type = Column(String(50), nullable=True)
    irrigation_available = Column(Boolean, default=False, nullable=False)
    crop_type = Column(String(50), nullable=True)
    sowing_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "name": self.name,
            "location": self.location,
            "district": self.district,
            "village": self.village,
            "gps_latitude": float(self.gps_latitude) if self.gps_latitude else None,
            "gps_longitude": float(self.gps_longitude) if self.gps_longitude else None,
            "area_acres": self.area_acres,
            "area_hectares": float(self.area_hectares) if self.area_hectares else None,
            "soil_type": self.soil_type,
            "irrigation_available": self.irrigation_available,
            "crop_type": self.crop_type,
            "sowing_date": str(self.sowing_date) if self.sowing_date else None,
            "created_at": str(self.created_at) if self.created_at else None,
            "updated_at": str(self.updated_at) if self.updated_at else None,
        }
    
    @property
    def area_unit(self):
        """Return area unit label"""
        if self.area_hectares:
            return "hectares"
        return "acres"


class CropHistory(Base):
    __tablename__ = "crop_history"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, nullable=False, index=True)
    crop_type = Column(String(50), nullable=False)
    season = Column(String(50), nullable=True)
    yield_per_acre = Column(Float, nullable=False)
    total_yield = Column(Float, nullable=True)
    sowing_date = Column(DateTime(timezone=True), nullable=True)
    harvest_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())