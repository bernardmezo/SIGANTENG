'use client'

import { useState } from 'react'

export default function ChatPage() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'ai' }[]>([])

  const handleSendMessage = async () => {
    if (input.trim() === '') return

    const userMessage = { text: input, sender: 'user' as const }
    setMessages((prev) => [...prev, userMessage])
    setInput('')

    // Simulate AI response
    const aiResponse = { text: `AI received: ${input}`, sender: 'ai' as const }
    setMessages((prev) => [...prev, aiResponse])
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow p-4">
        <h1 className="text-xl font-bold text-gray-900 dark:text-white">AI Assistant Chat</h1>
      </header>
      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs p-3 rounded-lg ${msg.sender === 'user'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-300 text-gray-900 dark:bg-gray-700 dark:text-white'}
              `}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </main>
      <footer className="bg-white dark:bg-gray-800 p-4 flex items-center">
        <input
          type="text"
          className="flex-1 border border-gray-300 dark:border-gray-700 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSendMessage()
            }
          }}
        />
        <button
          className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onClick={handleSendMessage}
        >
          Send
        </button>
      </footer>
    </div>
  )
}
