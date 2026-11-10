import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Chatbot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState('en')
  const [supportedLangs, setSupportedLangs] = useState(['en', 'te', 'hi'])

  useEffect(() => {
    fetchSupportedLangs()
  }, [])

  const fetchSupportedLangs = async () => {
    try {
      const res = await axios.get('/api/chat/languages')
      setSupportedLangs(res.data.languages)
    } catch (err) {
      console.error('Error fetching languages:', err)
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    setMessages(prev => [...prev, { role: 'user', content: input }])
    setInput('')
    setLoading(true)

    try {
      const res = await axios.post('/api/chat/ask', {
        question: input,
        crop_type: null,
        farmer_language: language,
      })
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.answer }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }])
      console.error(err)
    }
    setLoading(false)
  }

  const changeLanguage = (lang) => setLanguage(lang)

  return (
    <div className="min-h-screen p-4">
      <Container>
        <Header>
          <h2 className="text-3xl font-bold text-gray-900">
            💬 AI Farmer Advisory Chatbot
          </h2>
        </Header>

        {/* Chat Messages */}
        <div className="bg-white rounded-xl shadow mb-8 h-96 overflow-y-auto border border-gray-200">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={msg.role === 'user'
                ? 'bg-blue-100 px-4 py-3 rounded-r-xl mx-auto max-w-xl'
                : 'bg-gray-100 px-4 py-3 rounded-l-xl mx-auto max-w-xl'}
            >
              <p className="text-sm">{msg.content}</p>
            </div>
          ))}
          {!messages.length && (
            <p className="text-gray-500 text-center py-12">
              Ask me about your crop, soil, or farming practices
            </p>
          )}
        </div>

        {/* Language Selector */}
        {supportedLangs.length > 0 && (
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Language
            </label>
            <div className="flex gap-2">
              {supportedLangs.map((lang) => (
                <button
                  key={lang}
                  onClick={changeLanguage}
                  className={`px-3 py-1 rounded text-sm ${
                    language === lang
                      ? 'bg-blue-600 text-white font-medium'
                      : 'text-gray-600 hover:bg-gray-100'}
                  `}
                >
                  {lang === 'en' ? 'English' : lang === 'te' ? 'Telugu' : 'Hindi'}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat Input */}
        <div className="bg-white rounded-xl shadow p-4 border border-gray-200">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
              placeholder="Type your farming question..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-green-500"
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              className="bg-green-600 text-white px-5 py-2 rounded hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>

          {loading && (
            <p className="text-center text-sm text-gray-500 mt-2">
              Getting advisory guidance...
            </p>
          )}
        </div>
      </Container>
    </div>
  )
}

export default Chatbot