# Recipe LLM Quick Start Guide

Get started with Recipe LLM in under 5 minutes!

## Installation

```bash
# 1. Navigate to the recipe-llm directory
cd recipe-llm

# 2. Install dependencies
pip install -r requirements.txt
```

## Setup Your API Key

Choose one of these options:

### Option 1: OpenAI (Recommended for beginners)

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Get your key at: https://platform.openai.com/api-keys

### Option 2: Anthropic Claude

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Get your key at: https://console.anthropic.com/

### Option 3: Ollama (Free, Local)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2
```

No API key needed!

## Quick Examples

### 1. Get a Recipe (Command Line)

```bash
python src/cli.py "How do I make chocolate chip cookies?"
```

### 2. Interactive Mode

```bash
python src/cli.py --interactive
```

Then type your questions:
- "Give me a recipe for lasagna"
- "What can I substitute for eggs?"
- "How do I make perfect rice?"

Type `exit` to quit.

### 3. Web Interface

```bash
python src/web_app.py
```

Open your browser to: http://localhost:5000

### 4. Python Code

```python
from src.recipe_llm import RecipeLLM

# Initialize
llm = RecipeLLM(provider="openai")

# Get a recipe
recipe = llm.get_recipe("carbonara")
print(recipe)

# Ask a question
answer = llm.ask("How do I make risotto?")
print(answer)
```

## Common Use Cases

### Get a Vegan Recipe

```bash
python src/cli.py --recipe "chocolate cake" --dietary vegan
```

### Scale a Recipe

```bash
python src/cli.py --recipe "pancakes" --servings 12
```

### Get Ingredient Substitution

```bash
python src/cli.py --substitute "buttermilk"
```

### Explain a Technique

```bash
python src/cli.py --technique "sous vide"
```

### Use a Different Provider

```bash
# Use Anthropic Claude
python src/cli.py --provider anthropic "Give me a recipe for pad thai"

# Use Ollama (local)
python src/cli.py --provider ollama --interactive
```

## Tips

1. **For detailed recipes**: Ask specifically
   - Good: "Give me a detailed recipe for Italian carbonara"
   - Better: "Give me an authentic Italian carbonara recipe with step-by-step instructions"

2. **For dietary needs**: Be specific
   - "Give me a vegan and gluten-free lasagna recipe"

3. **For quick help**: Use the web interface
   - Visual and easy to use
   - Quick action buttons for common requests

4. **Save recipes**: Redirect output to a file
   ```bash
   python src/cli.py "Recipe for tiramisu" > tiramisu.md
   ```

## Troubleshooting

### "No API key found"
Set your API key:
```bash
export OPENAI_API_KEY='your-key'
```

### "Module not found"
Install dependencies:
```bash
pip install -r requirements.txt
```

### "Connection error"
Check your internet connection and API key.

### Want to use it offline?
Use Ollama:
```bash
python src/cli.py --provider ollama --interactive
```

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [docs/API.md](docs/API.md) for API documentation
- Explore [examples/example_usage.py](examples/example_usage.py) for code examples

## Need Help?

- Check the documentation in `/docs`
- Look at examples in `/examples`
- Open an issue on GitHub

Happy cooking! 🍳👨‍🍳👩‍🍳
