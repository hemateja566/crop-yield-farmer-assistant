import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Advisory() {
  const [advice, setAdvice] = useState(null)
  const [loading, setLoading] = useState(true)
  const [question, setQuestion] = useState('')
  const [cropType, setCropType] = useState('rice')
  const [language, setLanguage] = useState('en')

  useEffect(() => {
    fetchInitialAdvice()
  }, [])

  const fetchInitialAdvice = async () => {
    try {
      const res = await axios.get('/api/chat/knowledge-base/status')
      // Just initialize - set loading state
      setLoading(false)
    } catch (err) {
      console.error('Error:', err)
      setLoading(false)
    }
  }

  const getAdvice = async () => {
    if (!question.trim()) return

    setLoading(true)
    try {
      const res = await axios.post('/api/chat/ask', {
        question,
        crop_type: cropType,
        farmer_language: language,
      })
      setAdvice(res.data)
    } catch (err) {
      console.error('Error getting advice:', err)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen p-4">
      <Container>
        <Header>
          <h2 className="text-3xl font-bold text-gray-900">
            🧑‍🌾 Crop Advisory
          </h2>
        </Header>

        {/* Crop Selection */}
        <div className="bg-white rounded-xl shadow p-6 mb-8 border border-gray-200 mb-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Select Crop for Targeted Advice
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => setCropType('rice')}
              className={`px-4 py-2 rounded text-sm ${
                cropType === 'rice' ? 'bg-green-600 text-white font-medium' : 'text-gray-600 hover:bg-gray-100'}
              `}
            >
              Rice / Paddy
            </button>
            <button
              onClick={() => setCropType('wheat')}
              className={`px-4 py-2 rounded text-sm ${
                cropType === 'wheat' ? 'bg-green-600 text-white font-medium' : 'text-gray-600 hover:bg-gray-100'}
              `}
            >
              Wheat
            </button>
          </div>
          <div className="mt-3">
            <button
              onClick={() => setCropType('maize')}
              className="px-4 py-2 rounded text-sm text-gray-600 hover:bg-gray-100"
            >
              Maize / Corn
            </button>
          </div>
        </div>

        {/* Farmer Question Form */}
        <div className="bg-white rounded-xl shadow p-6 mb-8 border border-gray-200">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Ask Your Question
          </h3>

          <div className="grid grid-cols-2 gap-3 mb-4">
            <select
              value={cropType}
              onChange={e => setCropType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
            >
              <option value="rice">Rice / Paddy</option>
              <option value="wheat">Wheat</option>
              <option value="maize">Maize / Corn</option>
            </select>

            <select
              value={language}
              onChange={e => setLanguage(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
            >
              <option value="en">English</option>
              <option value="te">Telugu</option>
              <option value="hi">Hindi</option>
            </select>
          </div>

          <textarea
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Describe your crop issue or ask for advice..."
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500 resize-hg"
            disabled={loading}
          ></textarea>
        </div>

        {/* Generate Advice Button */}
        <button
          onClick={getAdvice}
          className="w-full bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700 font-medium transition disabled:opacity-50 disabled:cursor-not-letter-spacing"
          disabled={loading || !question.trim()}
        >
          {loading ? 'Getting advice...' : 'Generate Advisory'}
        </button>

        {/* Advice Result */}
        {advice && (
          <div className="bg-white rounded-xl shadow p-8 border-green-100 mb-8">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              💡 Advisory Guidance
            </h3>

            <p className="text-base text-gray-700 leading-relaxed">
              {advice.answer}
            </p>

            {advice.sources && advice.sources.length > 0 && (
              <div className="mt-6 pt-4 border-t border-green-200">
                <p className="text-sm text-gray-500 mb-2">Sources Referenced:</p>
                {advice.sources.map((src, idx) => (
                  <div
                    key={idx}
                    className="bg-gray-50 p-3 rounded text-xs text-gray-600"
                  >
                    {src.content}
                  </div>
                ))}
              </div>
            )}

            <div className="mt-6 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-500">
                Original question: "{question}"
              </p>
            </div>
          </div>
        )}

        {/* No advice yet */}
        {!advice && loading && (
          <p className="text-gray-500 text-center py-8">Ask a question above to get advisory guidance</p>
        )}
      </Container>
    </div>
  )
}

export default Advisory