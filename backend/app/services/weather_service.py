import httpx
from app.config import OPEN_METEO_BASE, SUPPORTED_CROPS


async def get_weather_forecast(latitude: float, longitude: float, days: int = 7):
    """
    Get weather forecast from Open-Meteo API.
    
    Parameters:
    - latitude: Farm latitude
    - longitude: Farm longitude
    - days: Number of forecast days (1-16)
    
    Returns:
    - Weather forecast data
    """
    url = f"{OPEN_METEO_BASE}/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "timezone": "auto",
        "forecast_days": days,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            print(f"Weather API error: {e}")
            return None


async def get_current_weather(latitude: float, longitude: float):
    """
    Get current weather conditions from Open-Meteo API.
    """
    url = f"{OPEN_METEO_BASE}/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data.get("current_weather", {})
        except httpx.HTTPError as e:
            print(f"Current weather API error: {e}")
            return None


async def get_historical_weather(latitude: float, longitude: float, 
                                  start_date: str, end_date: str):
    """
    Get historical weather data from Open-Meteo API.
    """
    url = f"{OPEN_METEO_BASE}/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "timezone": "auto",
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            print(f"Historical weather API error: {e}")
            return None