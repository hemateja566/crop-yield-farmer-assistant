import React, { useState, useEffect } from 'react'
import axios from 'axios'

function FarmManagement() {
  const [farms, setFarms] = useState([])
  const [farmForm, setFarmForm] = useState({
    name: '',
    district: '',
    village: '',
    area_acres: 1,
    soil_type: '',
    irrigation_available: false,
    crop_type: '',
    sowing_date: '',
    gps_latitude: null,
    gps_longitude: null,
  })
  const [editingFarm, setEditingFarm] = useState(null)
  const [showForm, setShowForm] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetchFarms()
  }, [])

  const fetchFarms = async () => {
    try {
      const res = await axios.get('/api/farms/')
      setFarms(res.data)
    } catch (err) {
      console.error('Error fetching farms:', err)
    }
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFarmForm({
      ...farmForm,
      [name]: type === 'checkbox' ? checked : value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editingFarm) {
        // Update existing farm
        await axios.put(`/api/farms/${editingFarm.id}`, farmForm)
        setMessage('Farm updated successfully')
      } else {
        // Create new farm
        await axios.post('/api/farms/', farmForm)
        setMessage('Farm registered successfully')
      }
      setFarmForm(initialForm)
      setShowForm(false)
      fetchFarms()
    } catch (err) {
      console.error('Error saving farm:', err)
      setMessage('Error saving farm')
    }
  }

  const initialForm = {
    name: '',
    district: '',
    village: '',
    area_acres: 1,
    soil_type: '',
    irrigation_available: false,
    crop_type: '',
    sowing_date: '',
    gps_latitude: null,
    gps_longitude: null,
  }

  const editFarm = (farm) => {
    setEditingFarm(farm)
    setFarmForm({
      name: farm.name,
      district: farm.district,
      village: farm.village,
      area_acres: farm.area_acres,
      soil_type: farm.soil_type,
      irrigation_available: farm.irrigation_available,
      crop_type: farm.crop_type,
      sowing_date: farm.sowing_date,
      gps_latitude: farm.gps_latitude,
      gps_longitude: farm.gps_longitude,
    })
    setShowForm(true)
  }

  const deleteFarm = async (farmId) => {
    if (confirm('Are you sure you want to delete this farm?')) {
      try {
        await axios.delete(`/api/farms/${farmId}`)
        setMessage('Farm deleted successfully')
        fetchFarms()
      } catch (err) {
        console.error('Error deleting farm:', err)
        setMessage('Error deleting farm')
      }
    }
  }

  return (
    <div className="min-h-screen p-4">
      <Container>
        <Header>
          <h2 className="text-3xl font-bold text-gray-900">
            🚜 Farm Management
          </h2>
        </Header>

        {/* Message */}
        {message && (
          <div className="mb-6 p-4 rounded {message.includes('success') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
            {message}
          </div>
        )}

        {/* Farms List */}
        <div className="bg-white rounded-xl shadow mb-8 border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-xl font-semibold text-gray-800">
              My Farms ({farms.length})
            </h3>
          </div>
          {farms.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              No farms registered yet.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="p-3 text-left text-gray-600 font-medium">Name</th>
                    <th className="p-3 text-left text-gray-600 font-medium">Location</th>
                    <th className="p-3 text-left text-gray-600 font-medium">Area</th>
                    <th className="p-3 text-left text-gray-600 font-medium">Crop</th>
                    <th className="p-3 text-left text-gray-600 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {farms.map((farm) => (
                    <tr key={farm.id} className="hover:bg-gray-50">
                      <td className="p-3 font-medium">{farm.name || 'Unnamed'}</td>
                      <td className="p-3 text-sm text-gray-500">
                        {farm.district}, {farm.village}
                      </td>
                      <td className="p-3 text-sm text-gray-600">
                        {farm.area_acres} acres
                      </td>
                      <td className="p-3 text-sm text-gray-500">
                        {farm.crop_type || '—'}
                      </td>
                      <td className="p-3">
                        <button
                          onClick={() => editFarm(farm)}
                          className="text-blue-600 hover/underline mr-2"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => deleteFarm(farm.id)}
                          className="text-red-600 hover/underline"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Farm Form */}
        {showForm && (
          <div className="bg-white rounded-xl shadow p-6 mb-8 border border-gray-200">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              {editingFarm ? 'Edit Farm' : 'New Farm'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Farm Name
                </label>
                <input
                  type="text"
                  name="name"
                  value={farmForm.name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    District
                  </label>
                  <input
                    type="text"
                    name="district"
                    value={farmForm.district}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Village
                  </label>
                  <input
                    type="text"
                    name="village"
                    value={farmForm.village}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Area (acres)
                </label>
                <input
                  type="number"
                  name="area_acres"
                  value={farmForm.area_acres}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  min="0.1"
                  step="0.1"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Soil Type
                  </label>
                  <input
                    type="text"
                    name="soil_type"
                    value={farmForm.soil_type}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                    placeholder="e.g., loamy, sandy, clay"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Irrigation Available
                  </label>
                  <input
                    type="checkbox"
                    name="irrigation_available"
                    checked={farmForm.irrigation_available}
                    onChange={handleInputChange}
                    className="w-4 h-4 rounded border-gray-500 focus:ring-green-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Crop Type
                </label>
                <select
                  name="crop_type"
                  value={farmForm.crop_type}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                  required
                >
                  <option value="">Select crop</option>
                  <option value="rice">Rice / Paddy</option>
                  <option value="wheat">Wheat</option>
                  <option value="maize">Maize / Corn</option>
                  <option value="cotton">Cotton</option>
                  <option value="sugarcane">Sugarcane</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Sowing Date
                </label>
                <input
                  type="date"
                  name="sowing_date"
                  value={farmForm.sowing_date}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    GPS Latitude
                  </label>
                  <input
                    type="number"
                    name="gps_latitude"
                    value={farmForm.gps_latitude}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                    placeholder="e.g., 17.3850"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    GPS Longitude
                  </label>
                  <input
                    type="number"
                    name="gps_longitude"
                    value={farmForm.gps_longitude}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
                    placeholder="e.g., 78.4885"
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 bg-green-600 text-white px-5 py-3 rounded hover:bg-green-700 transition">
                  {editingFarm ? 'Update' : 'Create Farm'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 bg-gray-200 text-gray-700 px-5 py-3 rounded hover:bg-gray-300 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}
      </Container>
    </div>
  )
}

export default FarmManagement