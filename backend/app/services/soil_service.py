import httpx
from app.config import SOILGRIDS_BASE


async def get_soil_data(latitude: float, longitude: float):
    """
    Get soil information from SoilGrids API.
    
    Returns soil properties including:
    - pH (H2O)
    - Organic carbon
    - Nitrogen
    - Phosphorus
    - Potassium
    - Sand, silt, clay fractions
    """
    url = f"{SOILGRIDS_BASE}/"
    
    # SoilGrids API endpoint for topsoil (0-5cm) properties
    params = {
        "lon": longitude,
        "lat": latitude,
        "depth": "0-5cm",
        "property": "ph_H2O,organic_carbon,nitrogen,phosphorus,potassium,sand,silt,clay",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            print(f"SoilGrids API error: {e}")
            return None


async def get_soil_ph(latitude: float, longitude: float):
    """Get just the soil pH from SoilGrids."""
    data = await get_soil_data(latitude, longitude)
    if data and "properties" in data:
        props = data["properties"]
        # Return pH value if available
        for key in ["ph_H2O", "ph", "pH"]:
            if key in props:
                return props[key]
    return None


async def get_soil_nutrients(latitude: float, longitude: float):
    """Get soil nitrogen, phosphorus, potassium from SoilGrids."""
    data = await get_soil_data(latitude, longitude)
    if data and "properties" in data:
        props = data["properties"]
        nutrients = {}
        for key in ["nitrogen", "phosphorus", "potassium"]:
            if key in props:
                nutrients[key] = props[key]
        return nutrients
    return {}