#!/usr/bin/env python3
"""
Example usage of Recipe LLM
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from recipe_llm import RecipeLLM


def example_basic_recipe():
    """Example: Get a basic recipe."""
    print("="*80)
    print("Example 1: Basic Recipe Request")
    print("="*80 + "\n")

    # Note: Make sure to set OPENAI_API_KEY or use provider='ollama'
    llm = RecipeLLM(provider="openai")

    recipe = llm.get_recipe("chocolate chip cookies")
    print(recipe)


def example_dietary_restrictions():
    """Example: Get a recipe with dietary restrictions."""
    print("\n" + "="*80)
    print("Example 2: Recipe with Dietary Restrictions")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai")

    recipe = llm.get_recipe(
        "lasagna",
        dietary_restrictions=["vegan", "gluten-free"],
        servings=6
    )
    print(recipe)


def example_cooking_questions():
    """Example: Ask cooking questions."""
    print("\n" + "="*80)
    print("Example 3: Cooking Questions")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai")

    questions = [
        "What's the difference between baking soda and baking powder?",
        "How do I know when my steak is medium-rare?",
        "What can I substitute for heavy cream in a recipe?"
    ]

    for question in questions:
        print(f"\nQ: {question}")
        answer = llm.ask(question)
        print(f"A: {answer}\n")
        print("-" * 80)


def example_ingredient_substitution():
    """Example: Get ingredient substitutions."""
    print("\n" + "="*80)
    print("Example 4: Ingredient Substitutions")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai")

    substitution = llm.get_substitution("eggs", "in baking")
    print(substitution)


def example_technique_explanation():
    """Example: Explain a cooking technique."""
    print("\n" + "="*80)
    print("Example 5: Cooking Technique Explanation")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai")

    technique = llm.explain_technique("sous vide")
    print(technique)


def example_recipe_from_ingredients():
    """Example: Get recipe suggestions from available ingredients."""
    print("\n" + "="*80)
    print("Example 6: Recipe from Available Ingredients")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai")

    suggestions = llm.suggest_recipe(
        ingredients=["chicken breast", "rice", "broccoli", "garlic", "soy sauce"],
        restrictions=["quick", "30 minutes or less"]
    )
    print(suggestions)


def example_conversation_history():
    """Example: Using conversation history for follow-up questions."""
    print("\n" + "="*80)
    print("Example 7: Conversation with History")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai", conversation_history=True)

    # First question
    print("Q: Can you give me a recipe for Thai green curry?")
    response1 = llm.ask("Can you give me a recipe for Thai green curry?")
    print(f"A: {response1}\n")

    # Follow-up question (uses context from first question)
    print("Q: Can you make it vegetarian?")
    response2 = llm.ask("Can you make it vegetarian?")
    print(f"A: {response2}\n")

    # Another follow-up
    print("Q: What can I substitute for coconut milk?")
    response3 = llm.ask("What can I substitute for coconut milk?")
    print(f"A: {response3}\n")


def example_save_conversation():
    """Example: Save and load conversation history."""
    print("\n" + "="*80)
    print("Example 8: Save and Load Conversation")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai", conversation_history=True)

    # Have a conversation
    llm.ask("What's your best recipe for homemade pizza?")
    llm.ask("How do I make the dough from scratch?")

    # Save the conversation
    llm.save_conversation("pizza_conversation.json")
    print("Conversation saved to pizza_conversation.json")

    # Create a new instance and load the conversation
    llm2 = RecipeLLM(provider="openai", conversation_history=True)
    llm2.load_conversation("pizza_conversation.json")
    print("Conversation loaded!")

    # Continue the conversation
    response = llm2.ask("What temperature should I bake it at?")
    print(f"\nContinuing conversation:\nA: {response}")


def example_multiple_providers():
    """Example: Compare responses from different providers."""
    print("\n" + "="*80)
    print("Example 9: Multiple Providers Comparison")
    print("="*80 + "\n")

    question = "What's the secret to making perfect French macarons?"

    providers = ["openai", "anthropic"]

    for provider in providers:
        try:
            print(f"\n--- {provider.upper()} ---")
            llm = RecipeLLM(provider=provider)
            response = llm.ask(question)
            print(response)
            print("\n" + "-"*80)
        except Exception as e:
            print(f"Error with {provider}: {e}")


def example_scale_recipe():
    """Example: Scale a recipe to different serving sizes."""
    print("\n" + "="*80)
    print("Example 10: Scale Recipe")
    print("="*80 + "\n")

    llm = RecipeLLM(provider="openai")

    recipe = llm.scale_recipe("pancakes", servings=12)
    print(recipe)


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("RECIPE LLM - USAGE EXAMPLES")
    print("="*80)
    print("\nNote: Make sure to set your API key before running:")
    print("  export OPENAI_API_KEY='your-key-here'")
    print("  export ANTHROPIC_API_KEY='your-key-here'")
    print("\nOr use Ollama for local models (no API key needed)")
    print("="*80 + "\n")

    try:
        # Run a basic example to test
        example_basic_recipe()

        # Uncomment to run more examples:
        # example_dietary_restrictions()
        # example_cooking_questions()
        # example_ingredient_substitution()
        # example_technique_explanation()
        # example_recipe_from_ingredients()
        # example_conversation_history()
        # example_save_conversation()
        # example_scale_recipe()

        print("\n" + "="*80)
        print("Examples completed successfully!")
        print("Uncomment other examples in main() to try more features.")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure to:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your API key: export OPENAI_API_KEY='your-key'")
        print("3. Or use Ollama: RecipeLLM(provider='ollama')")


if __name__ == '__main__':
    main()
