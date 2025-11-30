'use client';

import { useState, useRef } from 'react';

interface ImageUploadProps {
  onUpload: (file: File) => void;
  loading: boolean;
}

export default function ImageUpload({ onUpload, loading }: ImageUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);

      // Upload file
      onUpload(file);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      onUpload(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  return (
    <div>
      <div
        className="border-2 border-dashed border-gray-200 rounded-xl p-8 text-center cursor-pointer hover:border-amber-300 transition-colors duration-200 bg-gray-50/50"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="hidden"
          disabled={loading}
        />
        
        {preview ? (
          <div className="space-y-4">
            <img
              src={preview}
              alt="Banana preview"
              className="max-h-64 mx-auto rounded-lg shadow-md border border-gray-200"
            />
            {loading && (
              <div className="text-amber-600 space-y-3">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-2 border-amber-200 border-t-amber-600"></div>
                <p className="mt-2 font-medium text-gray-700">Analyzing banana...</p>
                <p className="text-xs text-gray-500 font-light">This may take a few seconds</p>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-5xl">🍌</div>
            <div>
              <p className="text-base font-medium text-gray-700">
                {loading ? 'Processing...' : 'Tap or click to upload'}
              </p>
              <p className="text-sm text-gray-500 mt-1.5 font-light">
                Upload a photo of your banana
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

