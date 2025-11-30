'use client';

import { Recipe } from '@/data/recipes';

interface RecipeCardProps {
  recipe: Recipe;
}

export default function RecipeCard({ recipe }: RecipeCardProps) {
  const getDifficultyColor = () => {
    switch (recipe.difficulty) {
      case 'beginner': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'intermediate': return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'advanced': return 'bg-rose-50 text-rose-700 border-rose-200';
      default: return 'bg-gray-50 text-gray-700 border-gray-200';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8 hover:shadow-xl transition-shadow duration-300">
      <div className="mb-6">
        <div className="flex items-start justify-between mb-3 gap-4">
          <h3 className="text-xl md:text-2xl font-semibold text-gray-800 tracking-tight leading-tight">{recipe.title}</h3>
          <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getDifficultyColor()} whitespace-nowrap flex-shrink-0`}>
            {recipe.difficulty}
          </span>
        </div>
        <div className="flex flex-wrap gap-4 text-sm text-gray-500 mb-3 font-light">
          <span className="flex items-center gap-1.5">
            <span className="text-gray-400">⏱️</span> Prep: {recipe.prepTime}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="text-gray-400">🔥</span> Cook: {recipe.cookTime}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="text-gray-400">🍞</span> Serves: {recipe.servings}
          </span>
        </div>
        {recipe.source && (
          <p className="text-xs text-gray-400 font-light">
            Source: <a href={recipe.source} target="_blank" rel="noopener noreferrer" className="text-amber-600 hover:text-amber-700 underline decoration-amber-300 hover:decoration-amber-400 transition-colors">{recipe.source}</a>
          </p>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h4 className="font-medium text-gray-800 mb-3 text-sm uppercase tracking-wide">Ingredients</h4>
          <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 leading-relaxed">
            {recipe.ingredients.map((ingredient, idx) => (
              <li key={idx} className="pl-2">{ingredient}</li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="font-medium text-gray-800 mb-3 text-sm uppercase tracking-wide">Instructions</h4>
          <ol className="list-decimal list-inside space-y-3 text-sm text-gray-600 leading-relaxed">
            {recipe.instructions.map((instruction, idx) => (
              <li key={idx} className="pl-2">{instruction}</li>
            ))}
          </ol>
        </div>
      </div>

      {recipe.tips && recipe.tips.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-100">
          <h4 className="font-medium text-gray-800 mb-3 text-sm uppercase tracking-wide">💡 Tips</h4>
          <ul className="list-disc list-inside space-y-2 text-sm text-gray-600 leading-relaxed">
            {recipe.tips.map((tip, idx) => (
              <li key={idx} className="pl-2">{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

