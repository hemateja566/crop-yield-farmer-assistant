import React from 'react'

export const Container = ({ children }) => (
  <div className="max-w-7xl mx-auto px-4 py-8">
    {children}
  </div>
)

export const Header = ({ children }) => (
  <header className="mb-8">
    <h1 className="text-2xl font-extrabold text-gray-900">
      🌱 Crop Yield & Farmer Advisory
    </h1>
  </header>
)

export const Nav = ({ children }) => (
  <nav className="mt-4 flex items-center justify-between">
    <div className="flex items-space-y-6 space-x-8">
      {children}
    </div>
  </nav>
)

export const ThemeToggle = () => (
  <button
    className="p-2 rounded hover:bg-gray-100 transition"
    aria-label="Toggle theme"
  >
    🌙
  </button>
)