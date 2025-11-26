"""
Main Recipe LLM class for interacting with various LLM providers
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime


class RecipeLLM:
    """
    A unified interface for recipe and cooking assistance using various LLM providers.

    Supports:
    - OpenAI (GPT-4, GPT-3.5-turbo)
    - Anthropic Claude
    - Ollama (local models)
    """

    SYSTEM_PROMPT = """You are an expert chef and culinary advisor with extensive knowledge of cuisines from around the world. You have expertise in:

- Traditional and modern cooking techniques
- Recipes from every culture and cuisine
- Ingredient substitutions and adaptations
- Dietary restrictions and allergies
- Food science and chemistry
- Kitchen equipment and tools
- Meal planning and preparation
- Food safety and storage

When providing recipes, always include:
1. Complete ingredient list with measurements
2. Step-by-step instructions
3. Preparation time and cooking time
4. Serving size
5. Difficulty level
6. Any helpful tips or variations

Be detailed, accurate, and helpful. If you're unsure about something, say so and provide the best general guidance you can."""

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        conversation_history: bool = True
    ):
        """
        Initialize the Recipe LLM.

        Args:
            provider: LLM provider ("openai", "anthropic", "ollama")
            model: Specific model to use (defaults to best available)
            api_key: API key (if not set in environment)
            temperature: Response randomness (0.0-1.0)
            max_tokens: Maximum response length
            conversation_history: Whether to maintain conversation context
        """
        self.provider = provider.lower()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = conversation_history
        self.history: List[Dict[str, str]] = []

        # Set up provider-specific configuration
        if self.provider == "openai":
            self._setup_openai(model, api_key)
        elif self.provider == "anthropic":
            self._setup_anthropic(model, api_key)
        elif self.provider == "ollama":
            self._setup_ollama(model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _setup_openai(self, model: Optional[str], api_key: Optional[str]):
        """Set up OpenAI provider."""
        try:
            import openai
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")

        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model or "gpt-4-turbo-preview"

    def _setup_anthropic(self, model: Optional[str], api_key: Optional[str]):
        """Set up Anthropic Claude provider."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable.")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model or "claude-3-5-sonnet-20241022"

    def _setup_ollama(self, model: Optional[str]):
        """Set up Ollama for local models."""
        try:
            import ollama
        except ImportError:
            raise ImportError("Ollama package not installed. Run: pip install ollama")

        self.client = ollama
        self.model = model or "llama2"

    def _call_openai(self, prompt: str) -> str:
        """Make a call to OpenAI API."""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        if self.conversation_history and self.history:
            messages.extend(self.history)

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Make a call to Anthropic Claude API."""
        messages = []

        if self.conversation_history and self.history:
            messages.extend(self.history)

        messages.append({"role": "user", "content": prompt})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.SYSTEM_PROMPT,
            messages=messages
        )

        return response.content[0].text

    def _call_ollama(self, prompt: str) -> str:
        """Make a call to Ollama local model."""
        full_prompt = f"{self.SYSTEM_PROMPT}\n\nUser: {prompt}\n\nAssistant:"

        if self.conversation_history and self.history:
            context = "\n".join([
                f"{msg['role'].capitalize()}: {msg['content']}"
                for msg in self.history
            ])
            full_prompt = f"{self.SYSTEM_PROMPT}\n\n{context}\n\nUser: {prompt}\n\nAssistant:"

        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": full_prompt}],
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        )

        return response['message']['content']

    def ask(self, question: str) -> str:
        """
        Ask any cooking or recipe-related question.

        Args:
            question: The question to ask

        Returns:
            The LLM's response
        """
        if self.provider == "openai":
            response = self._call_openai(question)
        elif self.provider == "anthropic":
            response = self._call_anthropic(question)
        else:  # ollama
            response = self._call_ollama(question)

        if self.conversation_history:
            self.history.append({"role": "user", "content": question})
            self.history.append({"role": "assistant", "content": response})

        return response

    def get_recipe(
        self,
        dish_name: str,
        dietary_restrictions: Optional[List[str]] = None,
        servings: Optional[int] = None,
        cuisine: Optional[str] = None
    ) -> str:
        """
        Get a detailed recipe for a specific dish.

        Args:
            dish_name: Name of the dish
            dietary_restrictions: List of dietary restrictions (e.g., ["vegan", "gluten-free"])
            servings: Number of servings desired
            cuisine: Specific cuisine type (e.g., "Italian", "Japanese")

        Returns:
            Detailed recipe with ingredients and instructions
        """
        prompt = f"Please provide a detailed recipe for {dish_name}"

        if cuisine:
            prompt += f" in the {cuisine} style"

        if dietary_restrictions:
            restrictions = ", ".join(dietary_restrictions)
            prompt += f" that is {restrictions}"

        if servings:
            prompt += f" for {servings} servings"

        prompt += ". Include ingredients, step-by-step instructions, cooking time, and any helpful tips."

        return self.ask(prompt)

    def get_substitution(self, ingredient: str, context: Optional[str] = None) -> str:
        """
        Get ingredient substitution suggestions.

        Args:
            ingredient: The ingredient to substitute
            context: Optional context (e.g., "in baking", "for vegan cooking")

        Returns:
            Substitution suggestions
        """
        prompt = f"What can I substitute for {ingredient}"
        if context:
            prompt += f" {context}"
        prompt += "? Please provide several options with ratios if applicable."

        return self.ask(prompt)

    def explain_technique(self, technique: str) -> str:
        """
        Get an explanation of a cooking technique.

        Args:
            technique: The cooking technique to explain

        Returns:
            Detailed explanation of the technique
        """
        prompt = f"Please explain the cooking technique '{technique}' in detail. Include when to use it, how to do it properly, and any common mistakes to avoid."

        return self.ask(prompt)

    def scale_recipe(self, dish_name: str, servings: int) -> str:
        """
        Get a recipe scaled to a specific number of servings.

        Args:
            dish_name: Name of the dish
            servings: Desired number of servings

        Returns:
            Scaled recipe
        """
        prompt = f"Please provide a recipe for {dish_name} scaled for exactly {servings} servings. Include all measurements adjusted accordingly."

        return self.ask(prompt)

    def convert_measurement(self, measurement: str, to_unit: str) -> str:
        """
        Convert a cooking measurement.

        Args:
            measurement: The measurement to convert (e.g., "2 cups flour")
            to_unit: The unit to convert to (e.g., "grams")

        Returns:
            Converted measurement
        """
        prompt = f"Convert {measurement} to {to_unit}. Provide the exact conversion."

        return self.ask(prompt)

    def suggest_recipe(
        self,
        ingredients: List[str],
        restrictions: Optional[List[str]] = None
    ) -> str:
        """
        Suggest recipes based on available ingredients.

        Args:
            ingredients: List of available ingredients
            restrictions: Optional dietary restrictions

        Returns:
            Recipe suggestions
        """
        ingredients_str = ", ".join(ingredients)
        prompt = f"I have these ingredients: {ingredients_str}. "

        if restrictions:
            restrictions_str = ", ".join(restrictions)
            prompt += f"I need recipes that are {restrictions_str}. "

        prompt += "What dishes can I make? Please suggest 2-3 recipes with brief descriptions."

        return self.ask(prompt)

    def clear_history(self):
        """Clear conversation history."""
        self.history = []

    def save_conversation(self, filepath: str):
        """
        Save conversation history to a file.

        Args:
            filepath: Path to save the conversation
        """
        data = {
            "provider": self.provider,
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
            "history": self.history
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_conversation(self, filepath: str):
        """
        Load conversation history from a file.

        Args:
            filepath: Path to load the conversation from
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.history = data.get("history", [])


if __name__ == "__main__":
    # Example usage
    print("Recipe LLM - Example Usage\n")

    # Initialize with OpenAI (or change to your preferred provider)
    try:
        llm = RecipeLLM(provider="openai")

        print("Getting a recipe for Italian carbonara...\n")
        recipe = llm.get_recipe("carbonara", cuisine="Italian")
        print(recipe)

        print("\n" + "="*80 + "\n")
        print("Asking about egg substitutions...\n")
        substitution = llm.get_substitution("eggs", "in baking")
        print(substitution)

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your API key:")
        print("export OPENAI_API_KEY='your-key-here'")
        print("\nOr use a different provider:")
        print("llm = RecipeLLM(provider='ollama')  # For local models")
