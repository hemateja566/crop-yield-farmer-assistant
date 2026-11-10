import React, { useState, useEffect } from 'react'
import axios from 'axios'

function WeatherForecast() {
  const [weather, setWeather] = useState(null)
  const [farmInfo, setFarmInfo] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFarmData()
    fetchWeather()
  }, [])

  const fetchFarmData = async () => {
    try {
      const res = await axios.get('/api/farms/')
      setFarmInfo(res.data[0] || null)
    } catch (err) {
      console.error('Error fetching farm data:', err)
    }
  }

  const fetchWeather = async () => {
    if (!farmInfo) return

    setLoading(true)
    try {
      const res = await axios.get('/api/weather/', {
        params: { farm_id: farmInfo.id },
      })
      setWeather(res.data)
    } catch (err) {
      console.error('Error fetching weather:', err)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-4">
      <Container>
        <Header>
          <h2 className="text-3xl font-bold text-gray-900">
            🌤️ Weather Forecast
          </h2>
        </Header>

        {farmInfo ? (
          <div className="bg-white rounded-xl shadow p-6 mb-8 border-blue-100">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Weather for {farmInfo.district || 'Your Farm'}
            </h3>

            {loading ? (
              <p className="text-gray-500">Loading weather data...</p>
            ) : weather ? (
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-500">Maximum Temperature</p>
                  <p className="text-2xl font-medium text-red-600">
                    {weather.temperature_2m_max}°C
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Minimum Temperature</p>
                  <p className="text-2xl font-medium text-blue-600">
                    {weather.temperature_2m_min}°C
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-500">Rainfall (24h)</p>
                  <p className="text-2xl font-medium text-orange-600">
                    {weather.precipitation_sum} mm
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Weather Code</p>
                  <p className="text-2xl font-medium">
                    {getWeatherDescription(weather.weathercode)}
                  </p>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-500">Humidity</p>
                <p className="text-2xl font-medium">
                  {weather.relative_humidity_2m_max}%
                </p>
              </div>
            </div> : (
              <p className="text-gray-500">Connect to Open-Meteo API to view forecast</p>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow p-6 text-center border border-gray-200">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Add a farm to view weather
            </h3>
            <p className="text-gray-500">
              Set up your farm first to get localized weather forecasts
            </p>
            <button
              onClick={() => alert('Go to Farm Management')}
              className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Go to Farm Management
            </button>
          </div>
        )}
      </Container>
    </div>
  )
}

const getWeatherDescription = (code) => {
  const codes = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    71: 'Slight snow fall',
    73: 'Moderate snow fall',
    75: 'Heavy snow fall',
    80: 'Rain showers',
    81: 'Rain showers',
    82: 'Rain showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with hail',
    99: 'Thunderstorm with hail',
  }
  return codes[code] || 'Unknown'
}

export default WeatherForecast