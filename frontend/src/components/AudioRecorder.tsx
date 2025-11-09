'use client'

import { useState, useRef } from 'react'

interface AudioRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void
}

export default function AudioRecorder({ onRecordingComplete }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        onRecordingComplete(audioBlob)
        audioChunksRef.current = []
      }
      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error accessing microphone:', error)
      alert('Could not access microphone. Please ensure it is connected and permissions are granted.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`px-4 py-2 rounded-lg text-white ${isRecording ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
      >
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      {isRecording && <span className="text-red-500">Recording...</span>}
    </div>
  )
}
