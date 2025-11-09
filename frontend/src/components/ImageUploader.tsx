'use client'

import { useState } from 'react'

interface ImageUploaderProps {
  onImageUpload: (file: File) => void
}

export default function ImageUploader({ onImageUpload }: ImageUploaderProps) {
  const [selectedImage, setSelectedImage] = useState<File | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedImage(event.target.files[0])
    }
  }

  const handleUploadClick = () => {
    if (selectedImage) {
      onImageUpload(selectedImage)
      setSelectedImage(null) // Clear selection after upload
    }
  }

  return (
    <div className="flex flex-col items-center space-y-2 p-4 border rounded-lg">
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {selectedImage && (
        <div className="text-sm text-gray-600 dark:text-gray-300">
          Selected: {selectedImage.name}
        </div>
      )}
      <button
        onClick={handleUploadClick}
        disabled={!selectedImage}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
      >
        Upload Image
      </button>
    </div>
  )
}
