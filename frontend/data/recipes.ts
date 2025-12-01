export interface Recipe {
  id: string;
  title: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  prepTime: string;
  cookTime: string;
  servings: string;
  ingredients: string[];
  instructions: string[];
  tips?: string[];
  source?: string;
}

export const recipes: Recipe[] = [
  {
    id: 'beginner',
    title: 'Classic Beginner Banana Bread',
    difficulty: 'beginner',
    prepTime: '15 minutes',
    cookTime: '60 minutes',
    servings: '1 loaf (8-10 slices)',
    ingredients: [
      '3 ripe bananas, mashed',
      '1/3 cup melted butter',
      '1 cup sugar',
      '1 egg, beaten',
      '1 tsp vanilla extract',
      '1 tsp baking soda',
      'Pinch of salt',
      '1 1/2 cups all-purpose flour'
    ],
    instructions: [
      'Preheat oven to 350°F (175°C). Grease a 9x5 inch loaf pan.',
      'In a large bowl, mash the bananas with a fork until smooth.',
      'Stir the melted butter into the mashed bananas.',
      'Mix in the sugar, egg, and vanilla extract.',
      'Sprinkle the baking soda and salt over the mixture and stir in.',
      'Add the flour last and mix until just combined (do not overmix).',
      'Pour batter into the prepared loaf pan.',
      'Bake for 60 minutes, or until a toothpick inserted into the center comes out clean.',
      'Let cool in pan for 10 minutes, then turn out onto a wire rack to cool completely.'
    ],
    tips: [
      'Use very ripe bananas with brown spots for best flavor.',
      'Don\'t overmix the batter - a few lumps are okay.',
      'Check doneness at 55 minutes - ovens vary.'
    ]
  },
  {
    id: 'chocolate',
    title: 'Chocolate Banana Bread',
    difficulty: 'intermediate',
    prepTime: '10 minutes',
    cookTime: '45 minutes',
    servings: '1 loaf',
    ingredients: [
      '2 cups mashed banana',
      '2 1/2 tsp pure vanilla extract',
      '1 tbsp white vinegar',
      '1/4 cup oil or milk of choice',
      '3/4 cup pure maple syrup or honey',
      '1 3/4 cup flour (white, spelt, oat, or gluten free)',
      '1/2 cup unsweetened cocoa powder',
      '2 tbsp Dutch cocoa powder or additional unsweetened cocoa powder',
      '1 tsp baking soda',
      '3/4 tsp salt',
      '3/4 tsp baking powder',
      '1/2 cup mini chocolate chips (optional)'
    ],
    instructions: [
      'Preheat your oven to 350°F. Grease a 9×5 inch loaf pan or line it with parchment paper.',
      'Whisk the mashed banana, sweetener (maple syrup or honey), pure vanilla extract, vinegar, and oil or milk of choice in a large mixing bowl.',
      'In a separate bowl, stir the flour, cocoa powder, baking soda, baking powder, salt, and optional mini chocolate chips together.',
      'Combine the wet ingredients and dry ingredients until just evenly mixed.',
      'Spread the batter evenly into the loaf pan.',
      'For presentation, sprinkle more chocolate chips on top and press down into the top of the chocolate loaf.',
      'Place the pan on the oven\'s center rack, and bake for 45 minutes. Turn off the oven but do not open the door at all. Let the chocolate banana bread sit an additional 10 minutes in the closed oven.',
      'Remove from the oven. If it still looks under-baked, turn the oven back on and continue to cook until a toothpick inserted into the center comes out mostly clean.',
      'Let the banana bread cool before loosely covering it, leaving a space for air and moisture to escape. For best results, let it sit overnight - the taste and texture are even better the next day!'
    ],
    tips: [
      'This recipe can be made low fat, high fiber, egg free, gluten free, oil free, completely vegan, and refined sugar free.',
      'Leftover banana bread is fine to leave out overnight on the counter. Store in the fridge after a day for up to 4-5 days.',
      'Slice and freeze the loaf for up to three months. Place parchment between layers so slices don\'t stick together.',
      'Tastes even better the next day!'
    ],
    source: 'https://chocolatecoveredkatie.com/dark-chocolate-banana-bread/'
  },
  {
    id: 'healthy-chocolate',
    title: 'Healthy Chocolate Banana Bread',
    difficulty: 'intermediate',
    prepTime: '15 minutes',
    cookTime: '45-60 minutes',
    servings: '1-2 loaves (depending on pan size)',
    ingredients: [
      '1 egg',
      '1/2 cup sweetener of choice (brown sugar, maple syrup, or honey)',
      '2/3 cup unsweetened applesauce',
      '1 teaspoon vanilla',
      '2 cups mashed very ripe brown bananas (about 6 bananas)',
      '2 cups flour (all-purpose gluten free mix, all-purpose flour, or whole wheat)',
      '1 teaspoon baking soda',
      '1 teaspoon baking powder',
      '1 teaspoon salt',
      '1/2 cup dark cocoa powder',
      '1 cup chocolate chips'
    ],
    instructions: [
      'Preheat oven to 350°F. Grease a 10 inch bread pan or two 8 inch bread pans.',
      'Whisk together the egg, sugar (or maple syrup/honey), applesauce, vanilla, and bananas in a large bowl.',
      'In a separate bowl, mix the dry ingredients: flour, baking soda, baking powder, salt, and cocoa powder.',
      'Add the dry ingredients to the wet ingredients and mix just until combined.',
      'Stir in the chocolate chips (you can also save some to sprinkle on the top before you bake!).',
      'Pour the batter into the prepared pan(s).',
      'Bake 45 minutes for two 8-inch loaves or 1 hour for one 10-inch loaf. Cook until a toothpick comes out clean or with a few crumbs attached, or even a little gooier if you want it to be more like a gooey brownie!'
    ],
    tips: [
      'No butter or oil needed - the applesauce and bananas provide all the moisture!',
      'Very little added sugar - mostly sweetened from the bananas.',
      'Can be made into muffins instead of a loaf - makes about 20 muffins.',
      'Can also be baked in an 8x8 pan for about 50 minutes at 350°F.',
      'Can be frozen once baked for later enjoyment.'
    ],
    source: 'https://www.yammiesnoshery.com/2019/01/secretly-healthy-chocolate-banana-bread.html'
  }
];

