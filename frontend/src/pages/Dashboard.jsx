import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Dashboard() {
  const [farmInfo, setFarmInfo] = useState(null)
  const [yieldPrediction, setYieldPrediction] = useState(null)
  const [weather, setWeather] = useState(null)
  const [soilInfo, setSoilInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [predictionsHistory, setPredictionsHistory] = useState([])

  useEffect(() => {
    fetchFarmData()
    fetchPredictionsHistory()
  }, [])

  const fetchFarmData = async () => {
    try {
      const res = await axios.get('/api/farms/')
      setFarmInfo(res.data)
    } catch (err) {
      console.error('Error fetching farm data:', err)
    }
  }

  const fetchPredictionsHistory = async () => {
    try {
      const res = await axios.get('/api/predict/history')
      setPredictionsHistory(res.data)
    } catch (err) {
      console.error('Error fetching predictions:', err)
    }
  }

  const predictYield = async () => {
    if (!farmInfo) return

    setLoading(true)
    try {
      const res = await axios.post('/api/predict/yield', {
        crop: farmInfo.crop_type || 'rice',
        area: farmInfo.area_acres,
        soil_ph: farmInfo.soil_type ? getPhForType(farmInfo.soil_type) : 6.5,
        nitrogen: 80,
        phosphorus: 40,
        potassium: 35,
        temperature: 29,
        rainfall: 120,
        humidity: 75,
      })
      setYieldPrediction(res.data)
    } catch (err) {
      console.error('Error predicting yield:', err)
    } finally {
      setLoading(false)
    }
  }

  const getPhForType = (soilType) => {
    const phMap = {
      'sandy': 5.5,
      'loamy': 6.5,
      'clay': 6.8,
      'peat': 5.0,
    }
    return phMap[soilType] || 6.5
  }

  const formatSoilHealth = (soil) => {
    if (!soil) return 'Not available'
    const pH = soil.soil_ph || 6.5
    return `pH: ${pH}, N: ${soil.nitrogen || 0}, P: ${soil.phosphorus || 0}, K: ${soil.potassium || 0}`
  }

  return (
    <div className="min-h-screen p-4">
      <Container>
        <Header>
          <h2 className="text-3xl font-bold text-gray-900">
            📊 Farmer Dashboard
          </h2>
        </Header>

        {/* Farm Summary Card */}
        {farmInfo && (
          <div className="bg-white rounded-xl shadow p-6 mb-8 border-green-100">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Farm Overview
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Farm Name</p>
                <p className="font-medium">{farmInfo.name || 'Unnamed'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Area</p>
                <p className="font-medium">
                  {farmInfo.area_acres} acres / {farmInfo.area_hectares} ha
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Crop</p>
                <p className="font-medium">{farmInfo.crop_type || 'Not selected'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Soil Type</p>
                <p className="font-medium">{farmInfo.soil_type || 'Not specified'}</p>
              </div>
            </div>
          </div>
        )}

        {/* Yield Prediction Card */}
        <div>
          <button
            onClick={predictYield}
            className="mb-6 inline-block bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700 transition"
          >
            🔮 Generate Yield Prediction
          </button>
        </div>

        {yieldPrediction && (
          <div className="bg-white rounded-xl shadow p-6 mb-8 border-yellow-100">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              📈 Prediction Results
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Crop</p>
                <p className="font-medium text-lg text-green-600">
                  {yieldPrediction.crop_type}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Farm Area</p>
                <p className="font-medium">
                  {yieldPrediction.area} acres
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Estimated Total Yield</p>
                <p className="font-medium text-2xl text-green-700">
                  {yieldPrediction.predicted_total_yield} tonnes
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Yield per Acre</p>
                <p className="font-medium text-2xl text-blue-600">
                  {yieldPrediction.yield_per_area} tonnes/acre
                </p>
              </div>
            </div>

            <div className="mt-4 p-4 bg-yellow-50 rounded border-y-2 border-yellow-300">
              <p className="text-sm text-gray-700">
                <strong>Confidence Interval:</strong> {yieldPrediction.confidence_interval.lower} -
                {yieldPrediction.confidence_interval.upper} tonnes (total)
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {yieldPrediction.confidence_interval.method}
              </p>
            </div>
          </div>
        }</>

        {/* Weather Forecast Card */}
        {/* {farmInfo && (
          <div className="bg-white rounded-xl shadow p-6 mb-8 border-blue-100">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              🌤️ Weather Forecast
            </h3>
            <button
              onClick={() =>
                axios.get('/api/weather/', { params: { farm_id: farmInfo.id } })
              }
              className="mb-4 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Fetch Weather Data
            </button>
            {weather && (
              <div>
                <p className="text-sm text-gray-500">Max Temp</p>
                <p className="font-medium">{weather.max_temp}°C</p>
                <p className="text-sm text-gray-500">Min Temp</p>
                <p className="font-medium">{weather.min_temp}°C</p>
                <p className="text-sm text-gray-500">Rainfall</p>
                <p className="font-medium">{weather.rainfall} mm</p>
              </div>
            )}
          </div>
        )} 

        {/* Soil Health Card */}
        {farmInfo && (
          <div className="bg-white rounded-xl shadow p-6 mb-8 border-purple-100">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              🌱 Soil Health
            </h3>
            <p className="text-sm text-gray-500">{formatSoilHealth(farmInfo)}</p>
          </div>
        )}

        {/* Predictions History */}
        <div>
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            📜 Prediction History
          </h3>
          {predictionsHistory.length === 0 ? (
            <p className="text-gray-500">No predictions yet. Generate your first prediction above.</p>
          ) : (
            <div className="space-y-3">
              {predictionsHistory.map((pred) => (
                <div
                  key={pred.id}
                  className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                >
                  <p className="font-medium text-gray-700">
                    {pred.crop_type} - {pred.yield_per_acre} tonnes/acre
                  </p>
                  <p className="text-xs text-gray-400">
                    {pred.created_at ? new Date(pred.created_at).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </Container>
    </div>
  )
}

export default Dashboard