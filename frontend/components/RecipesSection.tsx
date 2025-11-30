'use client';

import { recipes } from '@/data/recipes';
import RecipeCard from './RecipeCard';

export default function RecipesSection() {
  return (
    <div className="mt-12 space-y-8">
      <div className="text-center mb-10">
        <h2 className="text-3xl md:text-4xl font-semibold text-amber-700 tracking-tight mb-2">
          🍞 Banana Bread Recipes
        </h2>
        <p className="text-sm text-gray-500 font-light">Choose your favorite recipe to get started</p>
      </div>
      <div className="space-y-8">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
}

