# Recipe LLM API Documentation

## Table of Contents

- [RecipeLLM Class](#recipellm-class)
- [Initialization](#initialization)
- [Methods](#methods)
- [Examples](#examples)
- [Error Handling](#error-handling)

## RecipeLLM Class

The main class for interacting with recipe and cooking assistance LLMs.

### Initialization

```python
from recipe_llm import RecipeLLM

llm = RecipeLLM(
    provider="openai",           # LLM provider: "openai", "anthropic", "ollama"
    model=None,                  # Specific model (optional, uses default)
    api_key=None,                # API key (optional, reads from env)
    temperature=0.7,             # Response randomness (0.0-1.0)
    max_tokens=2000,             # Maximum response length
    conversation_history=True    # Maintain conversation context
)
```

#### Parameters

- **provider** (str): LLM provider to use
  - `"openai"`: OpenAI GPT models
  - `"anthropic"`: Anthropic Claude models
  - `"ollama"`: Local models via Ollama

- **model** (str, optional): Specific model to use
  - Default for OpenAI: `"gpt-4-turbo-preview"`
  - Default for Anthropic: `"claude-3-5-sonnet-20241022"`
  - Default for Ollama: `"llama2"`

- **api_key** (str, optional): API key for the provider
  - If not provided, reads from environment variables:
    - `OPENAI_API_KEY` for OpenAI
    - `ANTHROPIC_API_KEY` for Anthropic
    - Not needed for Ollama

- **temperature** (float): Controls randomness in responses
  - Range: 0.0 to 1.0
  - Lower values = more focused and deterministic
  - Higher values = more creative and varied

- **max_tokens** (int): Maximum length of generated responses
  - Default: 2000

- **conversation_history** (bool): Whether to maintain conversation context
  - Default: True
  - Allows for follow-up questions

## Methods

### ask(question: str) -> str

Ask any cooking or recipe-related question.

```python
response = llm.ask("How do I make risotto?")
```

**Parameters:**
- `question` (str): The question to ask

**Returns:**
- `str`: The LLM's response

**Example:**
```python
answer = llm.ask("What's the difference between sautéing and pan-frying?")
print(answer)
```

---

### get_recipe(dish_name, dietary_restrictions=None, servings=None, cuisine=None) -> str

Get a detailed recipe for a specific dish.

```python
recipe = llm.get_recipe(
    "carbonara",
    dietary_restrictions=["vegetarian"],
    servings=4,
    cuisine="Italian"
)
```

**Parameters:**
- `dish_name` (str): Name of the dish
- `dietary_restrictions` (list[str], optional): Dietary requirements
  - Examples: `["vegan"]`, `["gluten-free", "dairy-free"]`
- `servings` (int, optional): Number of servings
- `cuisine` (str, optional): Cuisine type
  - Examples: `"Italian"`, `"Japanese"`, `"Mexican"`

**Returns:**
- `str`: Detailed recipe with ingredients and instructions

**Example:**
```python
recipe = llm.get_recipe(
    "chocolate cake",
    dietary_restrictions=["vegan", "gluten-free"],
    servings=8
)
```

---

### get_substitution(ingredient, context=None) -> str

Get ingredient substitution suggestions.

```python
substitution = llm.get_substitution("buttermilk", "in baking")
```

**Parameters:**
- `ingredient` (str): The ingredient to substitute
- `context` (str, optional): Usage context
  - Examples: `"in baking"`, `"for vegan cooking"`

**Returns:**
- `str`: Substitution suggestions with ratios

**Example:**
```python
sub = llm.get_substitution("eggs", "in baking")
```

---

### explain_technique(technique: str) -> str

Get a detailed explanation of a cooking technique.

```python
explanation = llm.explain_technique("sous vide")
```

**Parameters:**
- `technique` (str): The cooking technique to explain

**Returns:**
- `str`: Detailed explanation of the technique

**Example:**
```python
info = llm.explain_technique("braising")
```

---

### scale_recipe(dish_name, servings) -> str

Get a recipe scaled to a specific number of servings.

```python
recipe = llm.scale_recipe("pancakes", servings=12)
```

**Parameters:**
- `dish_name` (str): Name of the dish
- `servings` (int): Desired number of servings

**Returns:**
- `str`: Recipe with scaled measurements

---

### convert_measurement(measurement, to_unit) -> str

Convert a cooking measurement.

```python
conversion = llm.convert_measurement("2 cups flour", "grams")
```

**Parameters:**
- `measurement` (str): The measurement to convert
- `to_unit` (str): Target unit

**Returns:**
- `str`: Converted measurement

**Example:**
```python
result = llm.convert_measurement("1 tablespoon", "milliliters")
```

---

### suggest_recipe(ingredients, restrictions=None) -> str

Suggest recipes based on available ingredients.

```python
suggestions = llm.suggest_recipe(
    ingredients=["chicken", "rice", "broccoli"],
    restrictions=["quick", "30 minutes"]
)
```

**Parameters:**
- `ingredients` (list[str]): Available ingredients
- `restrictions` (list[str], optional): Dietary or time restrictions

**Returns:**
- `str`: Recipe suggestions

---

### clear_history()

Clear the conversation history.

```python
llm.clear_history()
```

---

### save_conversation(filepath: str)

Save conversation history to a file.

```python
llm.save_conversation("my_conversation.json")
```

**Parameters:**
- `filepath` (str): Path to save the conversation

---

### load_conversation(filepath: str)

Load conversation history from a file.

```python
llm.load_conversation("my_conversation.json")
```

**Parameters:**
- `filepath` (str): Path to load the conversation from

## Examples

### Basic Usage

```python
from recipe_llm import RecipeLLM

# Initialize
llm = RecipeLLM(provider="openai")

# Get a recipe
recipe = llm.get_recipe("spaghetti carbonara")
print(recipe)

# Ask a question
answer = llm.ask("How do I properly cook rice?")
print(answer)
```

### With Dietary Restrictions

```python
llm = RecipeLLM(provider="openai")

# Vegan and gluten-free recipe
recipe = llm.get_recipe(
    "pizza",
    dietary_restrictions=["vegan", "gluten-free"],
    servings=4
)
print(recipe)
```

### Conversation with Context

```python
llm = RecipeLLM(provider="openai", conversation_history=True)

# First question
llm.ask("Can you give me a recipe for pad thai?")

# Follow-up (uses context)
llm.ask("Can you make it vegetarian?")

# Another follow-up
llm.ask("What can I use instead of fish sauce?")
```

### Using Different Providers

```python
# OpenAI
openai_llm = RecipeLLM(provider="openai")

# Anthropic Claude
claude_llm = RecipeLLM(provider="anthropic")

# Local Ollama
ollama_llm = RecipeLLM(provider="ollama")
```

### Saving Conversations

```python
llm = RecipeLLM(provider="openai", conversation_history=True)

# Have a conversation
llm.ask("How do I make bread?")
llm.ask("What about sourdough?")

# Save it
llm.save_conversation("bread_conversation.json")

# Later, load and continue
llm2 = RecipeLLM(provider="openai")
llm2.load_conversation("bread_conversation.json")
llm2.ask("Can I add herbs to the dough?")
```

## Error Handling

### Common Errors

```python
from recipe_llm import RecipeLLM

try:
    llm = RecipeLLM(provider="openai")
    recipe = llm.get_recipe("lasagna")
except ValueError as e:
    # Missing API key or invalid provider
    print(f"Configuration error: {e}")
except ImportError as e:
    # Missing required package
    print(f"Install required package: {e}")
except Exception as e:
    # Other errors (API errors, network issues, etc.)
    print(f"Error: {e}")
```

### Best Practices

1. **Always set API keys**:
   ```bash
   export OPENAI_API_KEY='your-key'
   export ANTHROPIC_API_KEY='your-key'
   ```

2. **Use try-except blocks** for production code

3. **Clear history** when starting new topics:
   ```python
   llm.clear_history()
   ```

4. **Save important conversations**:
   ```python
   llm.save_conversation("important_recipe.json")
   ```

5. **Use appropriate temperature**:
   - Lower (0.3-0.5) for precise recipes
   - Higher (0.7-0.9) for creative suggestions

## Provider-Specific Notes

### OpenAI
- Requires API key from https://platform.openai.com
- Best for detailed recipes and explanations
- Supports GPT-4 and GPT-3.5-turbo
- Pay per token

### Anthropic Claude
- Requires API key from https://console.anthropic.com
- Excellent for nuanced cooking advice
- Very good at adaptations and substitutions
- Pay per token

### Ollama
- Free and runs locally
- No API key required
- Install from https://ollama.ai
- Pull models: `ollama pull llama2`
- Slower than cloud APIs but private

## Rate Limits

Be aware of rate limits for paid APIs:
- OpenAI: Varies by plan
- Anthropic: Varies by plan
- Ollama: No rate limits (local)

Use appropriate delays between requests if making many calls.

## Support

For issues or questions:
- Check the main README.md
- Review examples in `examples/`
- Open an issue on GitHub
