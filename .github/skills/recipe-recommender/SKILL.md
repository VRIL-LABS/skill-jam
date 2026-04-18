---
name: recipe-recommender
description: Suggests recipes based on available ingredients, dietary restrictions, cuisine preferences, and pantry inventory. Invoke when asked to suggest recipes, find a meal idea, plan meals for the week, use up ingredients, or accommodate dietary needs.
---

# Recipe Recommender

Suggests personalized recipes matched to available ingredients, dietary restrictions, cuisine preferences, skill level, time constraints, and pantry inventory — with full ingredient lists, step-by-step instructions, substitution options, and nutritional information.

## When to Use

- User lists ingredients and asks "what can I make?"
- User wants a recipe that meets dietary needs (vegan, gluten-free, keto, halal, etc.)
- Meal planning for the week needs structured recipe suggestions
- User wants to use up produce or pantry items before they expire
- User asks for a dish from a specific cuisine or for a specific occasion
- A recipe needs to be adapted for a dietary restriction or ingredient substitution
- User wants nutritional information or calorie estimates for a meal

## Process

1. **Gather context**:
   - **Available ingredients**: what the user has on hand (be flexible — assume basic pantry staples are available unless stated otherwise)
   - **Dietary restrictions**: allergies (nuts, shellfish, dairy, gluten), lifestyle (vegan, vegetarian, halal, kosher, keto, low-carb, etc.), dislikes
   - **Cuisine preference**: Italian, Asian, Mexican, Mediterranean, etc., or "anything works"
   - **Meal type**: breakfast, lunch, dinner, snack, dessert, appetizer
   - **Time available**: quick (≤20 min), moderate (20–45 min), weekend cooking (1+ hours)
   - **Skill level**: beginner, intermediate, advanced
   - **Servings**: how many people

2. **Generate recipe candidates**:
   - Identify 3–5 recipe options that best match all constraints
   - Rank by: match completeness (how many required ingredients are already available), dietary compliance, time, and variety (don't suggest five pasta dishes)
   - Note any missing ingredients for each recipe and whether they are essential or optional

3. **Present each recipe with full detail**:
   - Recipe name and cuisine type
   - Active prep time + total cook time
   - Servings
   - Ingredient list with precise quantities (and metric/imperial options)
   - Step-by-step instructions, numbered and clear
   - Plating and serving suggestions
   - Storage and leftover instructions

4. **Add practical guidance**:
   - **Substitutions**: for each potentially unavailable or allergenic ingredient, offer a viable substitute and note any impact on flavor or texture
   - **Make-ahead tips**: which steps can be done in advance
   - **Scaling**: how to adjust quantities for more/fewer servings
   - **Common mistakes**: what to watch out for (over-seasoning, overcooking protein, etc.)

5. **Nutritional information** (when requested or for dietary-specific requests):
   - Estimated per-serving: calories, protein (g), carbohydrates (g), fat (g), fiber (g), sodium (mg)
   - Flag if the recipe is particularly high/low in any macronutrient relevant to the user's goals

6. **Meal planning mode** (when user wants multiple meals):
   - Suggest a balanced weekly plan across meal types
   - Optimize for ingredient reuse (shared pantry items across multiple recipes to reduce waste)
   - Include a consolidated shopping list for any missing ingredients across all planned meals

## Output Format

### Recipe Suggestion
```
## 🍳 Shakshuka (Middle Eastern Eggs in Tomato Sauce)
**Cuisine:** Middle Eastern | **Type:** Breakfast / Brunch / Dinner
**Time:** 10 min prep · 20 min cook · 30 min total
**Servings:** 2 | **Skill:** Beginner

### You Have (✅) / You Need (🛒)
✅ Eggs (4), canned tomatoes, onion, garlic, olive oil, cumin, paprika
🛒 Feta cheese (optional but recommended), fresh parsley, red pepper flakes

### Ingredients
- 2 tbsp olive oil
- 1 medium onion, diced
- 3 cloves garlic, minced
- 1 tsp cumin
- 1 tsp paprika
- ½ tsp red pepper flakes (adjust to taste)
- 1 can (400g / 14oz) crushed tomatoes
- Salt and pepper to taste
- 4 large eggs
- **Garnish:** crumbled feta, fresh parsley, crusty bread for serving

### Instructions
1. Heat olive oil in a large skillet over medium heat. Add onion; cook 5 minutes until softened.
2. Add garlic, cumin, paprika, and red pepper flakes; stir 1 minute until fragrant.
3. Pour in crushed tomatoes; season with salt and pepper. Simmer 8–10 minutes until sauce thickens slightly.
4. Make 4 wells in the sauce; crack an egg into each well. Cover and cook 5–7 minutes until whites are set but yolks are still runny (cook longer for firm yolks).
5. Remove from heat. Top with crumbled feta and fresh parsley. Serve immediately with crusty bread.

### Substitutions
- **No feta?** Goat cheese or skip entirely
- **No canned tomatoes?** Use 4 fresh ripe tomatoes, diced
- **Vegan?** Replace eggs with firm tofu slices — press into the sauce and cook the same way

### Nutritional Info (per serving, without bread)
~320 kcal · Protein: 16g · Carbs: 18g · Fat: 22g · Fiber: 4g
```

## Examples

### Example Input
```
I have chicken breast, garlic, lemon, spinach, olive oil, and pasta. I'm lactose intolerant and need something I can make in 30 minutes.
```

### Example Output
```
## 🍋 Lemon Garlic Chicken Pasta with Wilted Spinach
**Time:** 30 minutes | **Servings:** 2 | **Lactose-Free:** ✅

Ingredients: pasta (200g), chicken breast (2, thinly sliced), garlic (4 cloves), lemon (1, zest + juice), spinach (2 large handfuls), olive oil (3 tbsp), salt, pepper, chili flakes (optional).

Instructions:
1. Cook pasta per package; reserve ½ cup pasta water before draining.
2. Season chicken with salt and pepper; cook in olive oil over high heat 3–4 min per side. Remove and slice.
3. In the same pan, sauté garlic 1 min. Add spinach; wilt 2 min. Add lemon zest and juice.
4. Add pasta to pan with splash of pasta water; toss to combine. Top with chicken.

Completely lactose-free. Optional: top with toasted pine nuts for crunch.
```

## Boundaries

- Always respect stated dietary restrictions and allergies — do NOT suggest recipes containing allergenic ingredients the user has flagged, even as "optional" additions.
- Nutritional information is an estimate only — actual values vary based on specific ingredients and preparation methods.
- Do NOT suggest recipes that require equipment the user has said they don't have (e.g., a slow cooker if they only have a stovetop).
- For allergy-critical restrictions (e.g., anaphylactic peanut allergy), note that cross-contamination risks in shared kitchens should also be considered.
- When suggesting substitutions for allergenic ingredients, verify the substitute is itself free of the allergen.
