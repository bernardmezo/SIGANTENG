import React from 'react'

interface ChatMessageProps {
  message: { text: string; sender: 'user' | 'ai'; type?: 'text' | 'image' | 'audio' }
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow ${isUser
          ? 'bg-blue-500 text-white'
          : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}
        `}
      >
        {message.type === 'image' && message.text.startsWith('blob:') ? (
          // Assuming message.text is a blob URL for the image
          <img src={message.text} alt="User uploaded" className="max-w-full h-auto rounded-md" />
        ) : message.type === 'audio' && message.text.startsWith('blob:') ? (
          // Assuming message.text is a blob URL for the audio
          <audio controls src={message.text} className="w-full" />
        ) : (
          <p>{message.text}</p>
        )}
      </div>
    </div>
  )
}
