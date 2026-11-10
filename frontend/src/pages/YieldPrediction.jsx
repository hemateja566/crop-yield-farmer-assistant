import React, { useState } from 'react'
import axios from 'axios'

function YieldPrediction() {
  const [form, setForm] = useState({
    crop: 'rice',
    area: 2,
    soil_ph: 6.5,
    nitrogen: 80,
    phosphorus: 40,
    potassium: 35,
    temperature: 29,
    rainfall: 120,
    humidity: 75,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const predict = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await axios.post('/api/predict/yield', form)
      setResult(res.data)
    } catch (err) {
      setError('Error generating prediction')
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-4">
      <Container>
        <Header>
          <h2 className="text-3xl font-bold text-gray-900">
            🔢 Yield Prediction
          </h2>
        </Header>

        {/* Prediction Form */}
        <div className="bg-white rounded-xl shadow p-8 mb-8 border border-gray-200 max-w-2xl">
          <h3 className="text-2xl font-semibold text-gray-800 mb-6">Predict Crop Yield</h3>

          <form
            onSubmit={e => {
              e.preventDefault()
              predict()
            }}
          >
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Crop Type
                </label>
                <select
                  value.form
                  value={form.crop}
                  onChange={e => setForm({ ...form, crop: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                >
                  <option value="rice">Rice / Paddy</option>
                  <option value="wheat">Wheat</option>
                  <option value="maize">Maize / Corn</option>
                  <option value="cotton">Cotton</option>
                  <option value="sugarcane">Sugarcane</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Farm Area (acres)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="area"
                  value={form.area}
                  onChange={e => setForm({ ...form, area: parseFloat(e.target.value) || 1 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0.1"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Soil pH
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="soil_ph"
                  value={form.soil_ph}
                  onChange={e => setForm({ ...form, soil_ph: parseFloat(e.target.value) || 6.5 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0"
                  max="14"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nitrogen (N) - kg/ha
                </label>
                <input
                  type="number"
                  name="nitrogen"
                  value={form.nitrogen}
                  onChange={e => setForm({ ...form, nitrogen: parseInt(e.target.value) || 50 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Phosphorus (P) - kg/ha
                </label>
                <input
                  type="number"
                  name="phosphorus"
                  value={form.phosphorus}
                  onChange={e => setForm({ ...form, phosphorus: parseInt(e.target.value) || 25 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Potassium (K) - kg/ha
                </label>
                <input
                  type="number"
                  name="potassium"
                  value={form.potassium}
                  onChange={e => setForm({ ...form, potassium: parseInt(e.target.value) || 20 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Temperature - °C
                </label>
                <input
                  type="number"
                  name="temperature"
                  value={form.temperature}
                  onChange={e => setForm({ ...form, temperature: parseFloat(e.target.value) || 28 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="-10"
                  max="50"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Rainfall - mm
                </label>
                <input
                  type="number"
                  name="rainfall"
                  value={form.rainfall}
                  onChange={e => setForm({ ...form, rainfall: parseInt(e.target.value) || 100 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Humidity - %
              </label>
              <input
                type="number"
                name="humidity"
                value={form.humidity}
                onChange={e => setForm({ ...form, humidity: parseInt(e.target.value) || 70 })}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                min="0"
                max="100"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700 font-medium transition disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? 'Predicting...' : 'Generate Yield Prediction'}
            </button>
          </form>
        </div>

        {/* Result Card */}
        {result && (
          <div className="bg-white rounded-xl shadow p-8 border-yellow-100">
            <h3 className="text-2xl font-semibold text-gray-800 mb-6">
              📊 Prediction Results
            </h3>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div>
                <p className="text-sm text-gray-500">Crop</p>
                <p className="font-medium text-lg text-green-600">{result.crop_type}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Farm Area</p>
                <p className="font-medium">
                  {result.area} acres
                </p>
              </div>
            </div>

            <div className="mb-6">
              <p className="text-sm text-gray-500">Estimated Total Yield</p>
              <p className="text-3xl font-bold text-green-700">
                {result.predicted_total_yield} tonnes
              </p>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-gray-500">Yield per Acre</p>
                <p className="text-2xl font-bold text-blue-600">
                  {result.yield_per_area} tonnes/acre
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Model Confidence</p>
                <p className="text-lg font-medium">
                  {result.confidence_interval.lower} - {result.confidence_interval.upper} tonnes
                </p>
              </div>
            </div>

            <div className="mt-6 p-4 bg-yellow-50 rounded border-y-2 border-yellow-300">
              <p className="text-sm text-gray-700">
                <strong>Confidence Interval:</strong> {result.confidence_interval.lower} -
                {result.confidence_interval.upper} tonnes (total yield)
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {result.confidence_interval.method}
              </p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 text-red-800 rounded border border-red-300">
            {error}
          </div>
        )}
      </Container>
    </div>
  )
}

export default YieldPrediction