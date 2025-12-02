'use client';

import { useState } from 'react';
import ImageUpload from '@/components/ImageUpload';
import PredictionResult from '@/components/PredictionResult';
import RecipesSection from '@/components/RecipesSection';

export default function Home() {
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePrediction = async (file: File) => {
    setLoading(true);
    setError(null);
    setPrediction(null);
    
    // Optimize: Resize large images client-side before upload (reduces upload time)
    const maxSize = 1000;
    let processedFile = file;
    
    if (file.size > 500000) { // If larger than 500KB, resize
      try {
        const image = await new Promise<HTMLImageElement>((resolve, reject) => {
          const img = new Image();
          img.onload = () => resolve(img);
          img.onerror = reject;
          img.src = URL.createObjectURL(file);
        });
        
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        if (!ctx) throw new Error('Canvas not supported');
        
        const ratio = Math.min(maxSize / image.width, maxSize / image.height);
        canvas.width = image.width * ratio;
        canvas.height = image.height * ratio;
        
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
        
        // Wait for blob conversion
        const blob = await new Promise<Blob | null>((resolve) => {
          canvas.toBlob((b) => resolve(b), file.type, 0.9);
        });
        
        if (blob) {
          processedFile = new File([blob], file.name, { type: file.type });
        }
      } catch (e) {
        console.warn('Image resize failed, using original:', e);
      }
    }

    try {
      const formData = new FormData();
      formData.append('file', processedFile);

      // Use environment variable for API URL, fallback based on environment
      let apiUrl = process.env.NEXT_PUBLIC_API_URL || 
        (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
          ? 'http://localhost:8000' 
          : '/api');
      
      // Remove trailing slash to avoid double slashes
      apiUrl = apiUrl.replace(/\/$/, '');
      
      console.log('Sending request to:', `${apiUrl}/predict`);
      
      const response = await fetch(`${apiUrl}/predict`, {
        method: 'POST',
        body: formData,
        // Add timeout to detect if request hangs
        signal: AbortSignal.timeout(60000), // 60 second timeout
      });

      // Get response as text first to handle empty or non-JSON responses
      const responseText = await response.text();
      console.log('API Response Status:', response.status);
      console.log('API Response Text:', responseText);

      if (!response.ok) {
        // Try to parse as JSON, fallback to text
        let errorData;
        try {
          errorData = JSON.parse(responseText);
        } catch {
          errorData = { 
            detail: `HTTP ${response.status}: ${response.statusText}. Response: ${responseText.substring(0, 200)}` 
          };
        }
        throw new Error(errorData.detail || errorData.message || 'Prediction failed');
      }

      // Parse JSON response
      let data;
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        console.error('Failed to parse JSON:', e, 'Response:', responseText);
        throw new Error(`Invalid response from API. Status: ${response.status}. Response: ${responseText.substring(0, 200)}`);
      }

      if (data.days_until_bake_ready === undefined && data.days_until_bake_ready !== 0) {
        console.error('API response missing days_until_bake_ready:', data);
        throw new Error('API response missing required field: days_until_bake_ready');
      }

      setPrediction(data.days_until_bake_ready);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-semibold text-amber-700 mb-3 tracking-tight">
            Banana Oracle 🍌
          </h1>
          <p className="text-base md:text-lg text-gray-600 font-light">
            Upload a banana photo to predict when it will be ready to bake!
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8 mb-8">
          <div className="mb-8 pb-8 border-b border-gray-100">
            <h2 className="text-xl md:text-2xl font-semibold text-gray-800 mb-2 text-center">
              Example Photo
            </h2>
            <p className="text-sm text-gray-500 mb-6 text-center font-light">
              Take a photo similar to this example for best results
            </p>
            <div className="flex justify-center">
              <div className="relative max-w-48">
                <img
                  src="/example-banana.jpeg"
                  alt="Example banana photo"
                  className="rounded-lg shadow-md border border-gray-200 w-full h-auto"
                />
                <div className="absolute -top-2 -right-2 bg-amber-500 text-white text-xs font-medium px-2.5 py-1 rounded-full shadow-sm">
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
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-6 shadow-sm">
            <div className="flex flex-col items-center text-center gap-2">
              <div className="text-2xl">⚠️</div>
              <h3 className="font-semibold text-red-800">Oops!</h3>
              <p className="text-red-700 text-sm leading-relaxed">{error}</p>
            </div>
          </div>
        )}

        {prediction !== null && (
          <PredictionResult days={prediction} />
        )}

        <RecipesSection />

        <div className="mt-12 text-center text-xs text-gray-400 font-light">
          <p>Built with ResNet18 • Fine-tuned on hand collected banana ripeness data</p>
        </div>
      </div>
    </main>
  );
}

