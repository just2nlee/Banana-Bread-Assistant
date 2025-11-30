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
    <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
      <div className="text-center space-y-5">
        <div className="text-5xl">{getEmoji()}</div>
        <h2 className="text-2xl md:text-3xl font-semibold text-amber-700 tracking-tight">
          {getMessage()}
        </h2>
        <div className="mt-8">
          <div className="flex justify-between text-sm text-gray-500 mb-3 font-medium">
            <span>Ripeness Progress</span>
            <span>{Math.round(getProgress())}%</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
            <div
              className="bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600 h-2.5 rounded-full transition-all duration-700 ease-out"
              style={{ width: `${getProgress()}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
}

