'use client';

interface PredictionResultProps {
  days: number;
}

export default function PredictionResult({ days }: PredictionResultProps) {
  const getEmoji = () => {
    if (days <= 2) return '🍞';
    if (days <= 4) return '🍌';
    if (days <= 7) return '🍌';
    return '🍌';
  };

  const getMessage = () => {
    if (days === 0) return 'Your banana is ready to bake now!';
    if (days === 1) return 'Your banana will be bake-ready tomorrow!';
    return `Your banana will be bake-ready in ${days} days!`;
  };

  const getProgress = () => {
    // Assuming 14 days total, calculate progress
    const progress = Math.min(100, ((14 - days) / 14) * 100);
    return progress;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="text-center space-y-4">
        <div className="text-6xl">{getEmoji()}</div>
        <h2 className="text-3xl font-bold text-orange-600">
          {getMessage()}
        </h2>
        <div className="mt-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Ripeness Progress</span>
            <span>{Math.round(getProgress())}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-gradient-to-r from-yellow-400 to-orange-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${getProgress()}%` }}
            ></div>
          </div>
        </div>
        <p className="text-gray-600 mt-4">
          Days until bake-ready: <span className="font-bold text-orange-600">{days}</span>
        </p>
      </div>
    </div>
  );
}

