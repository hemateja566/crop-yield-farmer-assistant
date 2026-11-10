import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import axios from 'axios'

// Dashboard pages
import Dashboard from './pages/Dashboard'
import FarmManagement from './pages/FarmManagement'
import YieldPrediction from './pages/YieldPrediction'
import Chatbot from './pages/Chatbot'
import WeatherForecast from './pages/WeatherForecast'
import Advisory from './pages/Advisory'

// Components
import { Container, Header, Nav, ThemeToggle } from './components/Layout'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    // Check auth status
    axios.get('/api/auth/me')
      .then(res => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <Router>
      <Container>
        <Header>
          <Nav>
            <Link to="/">Home</Link>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/farms">Farm Management</Link>
            <Link to="/predict">Yield Prediction</Link>
            <Link to="/chat">Chatbot</Link>
            {user && <span className="ml-auto">Welcome, {user.name}</span>}
            {!user && <Link to="/login">Login</Link>}
          </Nav>
          <ThemeToggle />
        </Header>

        <main className="min-h-[600px]">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/farms" element={<FarmManagement />} />
            <Route path="/predict" element={<YieldPrediction />} />
            <Route path="/chat" element={<Chatbot />} />
            <Route path="/advisory" element={<Advisory />} />
            <Route path="/weather" element={<WeatherForecast />} />
          </Routes>
        </main>
      </Container>
    </Router>
  )
}

function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-green-100 p-8">
      <h1 className="text-4xl font-bold text-green-800 mb-4">
        🌱 Crop Yield & Farmer Advisory
      </h1>
      <p className="text-lg text-green-600">
        AI-powered crop yield prediction and farmer advisory platform
      </p>
      <div className="mt-8 grid grid-cols-2 gap-4 max-w-md">
        <Link to="/dashboard" className="group bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700 transition">
          <span className="group-hover/underline">Go to Dashboard</span>
        </Link>
        <Link to="/chat" className="group bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 transition">
          <span className="group-hover/underline">Chat with Advisor</span>
        </Link>
      </div>
    </div>
  )
}

export default App