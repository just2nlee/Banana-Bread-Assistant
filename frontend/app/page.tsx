'use client';

import { useState } from 'react';
import ImageUpload from '@/components/ImageUpload';
import PredictionResult from '@/components/PredictionResult';

export default function Home() {
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = async (file: File) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Use environment variable for API URL, fallback to localhost
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed');
      }

      const data = await response.json();
      setPrediction(data.days_until_bake_ready);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-orange-600 mb-2">
            🍌 Banana Bread Assistant
          </h1>
          <p className="text-lg text-gray-600">
            Upload a banana photo to predict when it will be bake-ready!
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="mb-6 pb-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-700 mb-3 text-center">
              Example Photo
            </h2>
            <p className="text-sm text-gray-500 mb-4 text-center">
              Take a photo similar to this example for best results
            </p>
            <div className="flex justify-center">
              <div className="relative max-w-48">
                <img
                  src="/example-banana.jpg"
                  alt="Example banana photo"
                  className="rounded-lg shadow-md border-2 border-orange-200 w-full h-auto"
                />
                <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                  Example
                </div>
              </div>
            </div>
          </div>
          <ImageUpload 
            onUpload={handlePrediction} 
            loading={loading}
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">Error: {error}</p>
          </div>
        )}

        {prediction !== null && (
          <PredictionResult days={prediction} />
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Built with ResNet18 • Fine-tuned on banana ripeness data</p>
        </div>
      </div>
    </main>
  );
}

