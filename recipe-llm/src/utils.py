"""
Utility functions for Recipe LLM
"""

import json
import re
from typing import Dict, List, Any, Optional


def parse_recipe(recipe_text: str) -> Dict[str, Any]:
    """
    Parse a recipe text into structured data.

    Args:
        recipe_text: Raw recipe text from LLM

    Returns:
        Structured recipe dictionary
    """
    recipe = {
        'title': '',
        'ingredients': [],
        'instructions': [],
        'prep_time': '',
        'cook_time': '',
        'servings': '',
        'difficulty': '',
        'tips': []
    }

    lines = recipe_text.split('\n')

    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for section headers
        lower_line = line.lower()

        if 'ingredient' in lower_line:
            current_section = 'ingredients'
        elif 'instruction' in lower_line or 'direction' in lower_line or 'step' in lower_line:
            current_section = 'instructions'
        elif 'tip' in lower_line or 'note' in lower_line:
            current_section = 'tips'
        elif current_section == 'ingredients':
            # Parse ingredient
            if line.startswith('-') or line.startswith('•') or line[0].isdigit():
                ingredient = re.sub(r'^[-•\d.)\s]+', '', line).strip()
                if ingredient:
                    recipe['ingredients'].append(ingredient)
        elif current_section == 'instructions':
            # Parse instruction
            if line.startswith('-') or line.startswith('•') or line[0].isdigit():
                instruction = re.sub(r'^[-•\d.)\s]+', '', line).strip()
                if instruction:
                    recipe['instructions'].append(instruction)
        elif current_section == 'tips':
            # Parse tip
            if line.startswith('-') or line.startswith('•') or line[0].isdigit():
                tip = re.sub(r'^[-•\d.)\s]+', '', line).strip()
                if tip:
                    recipe['tips'].append(tip)

        # Extract metadata
        if 'prep time' in lower_line or 'preparation time' in lower_line:
            recipe['prep_time'] = line.split(':')[-1].strip()
        elif 'cook time' in lower_line or 'cooking time' in lower_line:
            recipe['cook_time'] = line.split(':')[-1].strip()
        elif 'serving' in lower_line:
            recipe['servings'] = line.split(':')[-1].strip()
        elif 'difficulty' in lower_line:
            recipe['difficulty'] = line.split(':')[-1].strip()

    return recipe


def format_recipe_markdown(recipe: Dict[str, Any]) -> str:
    """
    Format a structured recipe as markdown.

    Args:
        recipe: Structured recipe dictionary

    Returns:
        Markdown formatted recipe
    """
    md = []

    if recipe.get('title'):
        md.append(f"# {recipe['title']}\n")

    # Metadata
    metadata = []
    if recipe.get('prep_time'):
        metadata.append(f"**Prep Time:** {recipe['prep_time']}")
    if recipe.get('cook_time'):
        metadata.append(f"**Cook Time:** {recipe['cook_time']}")
    if recipe.get('servings'):
        metadata.append(f"**Servings:** {recipe['servings']}")
    if recipe.get('difficulty'):
        metadata.append(f"**Difficulty:** {recipe['difficulty']}")

    if metadata:
        md.append(' | '.join(metadata) + '\n')

    # Ingredients
    if recipe.get('ingredients'):
        md.append("## Ingredients\n")
        for ingredient in recipe['ingredients']:
            md.append(f"- {ingredient}")
        md.append("")

    # Instructions
    if recipe.get('instructions'):
        md.append("## Instructions\n")
        for i, instruction in enumerate(recipe['instructions'], 1):
            md.append(f"{i}. {instruction}")
        md.append("")

    # Tips
    if recipe.get('tips'):
        md.append("## Tips\n")
        for tip in recipe['tips']:
            md.append(f"- {tip}")
        md.append("")

    return '\n'.join(md)


def save_recipe_to_file(recipe_text: str, filename: str, format: str = 'txt'):
    """
    Save a recipe to a file.

    Args:
        recipe_text: Recipe text to save
        filename: Output filename
        format: Output format ('txt', 'json', 'md')
    """
    if format == 'json':
        recipe = parse_recipe(recipe_text)
        with open(filename, 'w') as f:
            json.dump(recipe, f, indent=2)
    elif format == 'md':
        recipe = parse_recipe(recipe_text)
        markdown = format_recipe_markdown(recipe)
        with open(filename, 'w') as f:
            f.write(markdown)
    else:  # txt
        with open(filename, 'w') as f:
            f.write(recipe_text)


def extract_ingredients(recipe_text: str) -> List[str]:
    """
    Extract ingredients from recipe text.

    Args:
        recipe_text: Recipe text

    Returns:
        List of ingredients
    """
    recipe = parse_recipe(recipe_text)
    return recipe.get('ingredients', [])


def extract_instructions(recipe_text: str) -> List[str]:
    """
    Extract instructions from recipe text.

    Args:
        recipe_text: Recipe text

    Returns:
        List of instructions
    """
    recipe = parse_recipe(recipe_text)
    return recipe.get('instructions', [])


def create_shopping_list(recipes: List[str]) -> List[str]:
    """
    Create a shopping list from multiple recipes.

    Args:
        recipes: List of recipe texts

    Returns:
        Combined ingredient list
    """
    all_ingredients = []

    for recipe in recipes:
        ingredients = extract_ingredients(recipe)
        all_ingredients.extend(ingredients)

    # Remove duplicates while preserving order
    seen = set()
    unique_ingredients = []
    for ingredient in all_ingredients:
        # Normalize for comparison
        normalized = ingredient.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique_ingredients.append(ingredient)

    return unique_ingredients


def estimate_total_time(prep_time: str, cook_time: str) -> Optional[int]:
    """
    Estimate total time in minutes from prep and cook times.

    Args:
        prep_time: Preparation time string (e.g., "15 minutes")
        cook_time: Cooking time string (e.g., "30 minutes")

    Returns:
        Total time in minutes, or None if cannot parse
    """
    def parse_time(time_str: str) -> int:
        """Parse time string to minutes."""
        time_str = time_str.lower()
        minutes = 0

        # Extract hours
        hour_match = re.search(r'(\d+)\s*(?:hour|hr)', time_str)
        if hour_match:
            minutes += int(hour_match.group(1)) * 60

        # Extract minutes
        min_match = re.search(r'(\d+)\s*(?:minute|min)', time_str)
        if min_match:
            minutes += int(min_match.group(1))

        return minutes

    try:
        prep_minutes = parse_time(prep_time)
        cook_minutes = parse_time(cook_time)
        return prep_minutes + cook_minutes
    except:
        return None


def convert_servings(ingredient: str, from_servings: int, to_servings: int) -> str:
    """
    Scale an ingredient amount for different serving sizes.

    Args:
        ingredient: Ingredient string with amount (e.g., "2 cups flour")
        from_servings: Original serving size
        to_servings: Target serving size

    Returns:
        Scaled ingredient string
    """
    if from_servings == to_servings:
        return ingredient

    multiplier = to_servings / from_servings

    # Find numbers in the ingredient
    def replace_number(match):
        number = float(match.group(0))
        scaled = number * multiplier
        # Round to reasonable precision
        if scaled >= 10:
            return str(int(round(scaled)))
        elif scaled >= 1:
            return str(round(scaled, 1))
        else:
            return str(round(scaled, 2))

    return re.sub(r'\d+\.?\d*', replace_number, ingredient)


if __name__ == '__main__':
    # Example usage
    sample_recipe = """
    # Chocolate Chip Cookies

    Prep Time: 15 minutes
    Cook Time: 12 minutes
    Servings: 24 cookies
    Difficulty: Easy

    ## Ingredients
    - 2 cups all-purpose flour
    - 1 teaspoon baking soda
    - 1/2 teaspoon salt
    - 1 cup butter, softened
    - 3/4 cup granulated sugar
    - 3/4 cup packed brown sugar
    - 2 large eggs
    - 2 teaspoons vanilla extract
    - 2 cups chocolate chips

    ## Instructions
    1. Preheat oven to 375°F (190°C)
    2. Mix flour, baking soda, and salt in a bowl
    3. Beat butter and sugars until creamy
    4. Add eggs and vanilla
    5. Gradually blend in flour mixture
    6. Stir in chocolate chips
    7. Drop rounded tablespoons onto ungreased cookie sheets
    8. Bake for 9-11 minutes or until golden brown

    ## Tips
    - Don't overbake - cookies will continue to cook on the pan
    - For chewier cookies, slightly underbake them
    """

    print("Parsing recipe...")
    recipe = parse_recipe(sample_recipe)
    print(json.dumps(recipe, indent=2))

    print("\n\nFormatted Markdown:")
    print(format_recipe_markdown(recipe))
