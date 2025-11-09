'use client'

import { useState } from 'react'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  onSendAudio: (audioBlob: Blob) => void
  onSendImage: (imageFile: File) => void
}

export default function ChatInput({ onSendMessage, onSendAudio, onSendImage }: ChatInputProps) {
  const [textInput, setTextInput] = useState('')

  const handleTextSend = () => {
    if (textInput.trim()) {
      onSendMessage(textInput)
      setTextInput('')
    }
  }

  const handleAudioRecordingComplete = (audioBlob: Blob) => {
    onSendAudio(audioBlob)
  }

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      onSendImage(event.target.files[0])
    }
  }

  return (
    <div className="flex items-center p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <input
        type="text"
        className="flex-1 p-2 border rounded-lg dark:bg-gray-700 dark:text-white dark:border-gray-600"
        placeholder="Type a message..."
        value={textInput}
        onChange={(e) => setTextInput(e.target.value)}
        onKeyPress={(e) => {
          if (e.key === 'Enter') {
            handleTextSend()
          }
        }}
      />
      <button
        onClick={handleTextSend}
        className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
      >
        Send Text
      </button>
      {/* <AudioRecorder onRecordingComplete={handleAudioRecordingComplete} /> */}
      <label className="ml-2 px-4 py-2 bg-green-500 text-white rounded-lg cursor-pointer hover:bg-green-600">
        Upload Image
        <input type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
      </label>
    </div>
  )
}
