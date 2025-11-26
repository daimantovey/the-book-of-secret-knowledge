# Recipe LLM - AI-Powered Recipe & Cooking Assistant

A powerful large language model application that can provide recipes, cooking instructions, and answer any culinary question for virtually any dish ever made.

## Features

- **Universal Recipe Access**: Get detailed recipes for any dish from any cuisine
- **Cooking Guidance**: Ask questions about cooking techniques, substitutions, and tips
- **Multiple LLM Backends**: Support for OpenAI, Anthropic Claude, and local models
- **Web Interface**: Easy-to-use web UI for interactive recipe discovery
- **CLI Tool**: Command-line interface for quick recipe lookups
- **Smart Context**: Remembers conversation history for follow-up questions
- **Dietary Adaptations**: Get recipes adapted for dietary restrictions
- **Ingredient Substitutions**: Find alternatives for missing ingredients
- **Cooking Time Estimates**: Accurate preparation and cooking time information
- **Nutritional Information**: Get nutritional breakdowns (when available)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or navigate to this directory:
```bash
cd recipe-llm
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your API keys (choose one or more):

For OpenAI:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

For Anthropic Claude:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

For local models (Ollama):
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2
```

## Quick Start

### Web Interface

Launch the web application:
```bash
python src/web_app.py
```

Then open your browser to `http://localhost:5000`

### Command Line Interface

Get a recipe:
```bash
python src/cli.py "How do I make authentic Italian carbonara?"
```

Ask a cooking question:
```bash
python src/cli.py "What can I substitute for eggs in baking?"
```

Get a recipe with dietary restrictions:
```bash
python src/cli.py "Give me a vegan lasagna recipe"
```

## Usage Examples

### Using the Python API

```python
from src.recipe_llm import RecipeLLM

# Initialize with your preferred backend
llm = RecipeLLM(provider="openai")  # or "anthropic", "ollama"

# Get a recipe
recipe = llm.get_recipe("Beef Wellington")
print(recipe)

# Ask a cooking question
answer = llm.ask("How do I make perfect risotto?")
print(answer)

# Get recipe with specific requirements
vegan_recipe = llm.get_recipe(
    "chocolate cake",
    dietary_restrictions=["vegan", "gluten-free"]
)
print(vegan_recipe)
```

### Advanced Features

```python
# Get ingredient substitutions
substitution = llm.get_substitution("buttermilk")

# Get cooking technique explanations
technique = llm.explain_technique("sous vide")

# Scale recipes
scaled_recipe = llm.scale_recipe("classic pancakes", servings=12)

# Convert measurements
converted = llm.convert_measurement("2 cups flour", to_unit="grams")
```

## Configuration

Edit `config.yaml` to customize:

```yaml
default_provider: "openai"  # openai, anthropic, or ollama
temperature: 0.7
max_tokens: 2000
conversation_history: true
save_recipes: true
output_format: "markdown"  # markdown or json
```

## Supported LLM Providers

### OpenAI (GPT-4, GPT-3.5)
- Excellent for detailed recipes and cooking knowledge
- Requires API key from OpenAI
- Cost: Pay per token

### Anthropic Claude
- Great for nuanced cooking advice and adaptations
- Requires API key from Anthropic
- Cost: Pay per token

### Local Models (Ollama)
- Run completely offline
- Free to use
- Supports: Llama 2, Mistral, and others
- Requires local installation

## Example Queries

The Recipe LLM can handle queries like:

- "Give me a traditional Japanese ramen recipe"
- "How do I make croissants from scratch?"
- "What's a good substitute for heavy cream?"
- "Explain the difference between sautéing and pan-frying"
- "Give me a 30-minute weeknight dinner recipe"
- "How do I make vegan sushi?"
- "What's the best way to cook a ribeye steak?"
- "Give me a recipe for gluten-free bread"
- "How do I make homemade pasta?"
- "What can I make with chicken, rice, and broccoli?"

## Features in Detail

### Recipe Generation
The LLM provides comprehensive recipes including:
- Complete ingredient lists with measurements
- Step-by-step instructions
- Preparation and cooking times
- Serving sizes
- Difficulty level
- Tips and variations

### Cooking Q&A
Ask any cooking-related question:
- Techniques and methods
- Ingredient information
- Food safety
- Kitchen equipment
- Meal planning
- And more!

### Dietary Adaptations
Automatically adapt recipes for:
- Vegan/Vegetarian
- Gluten-free
- Dairy-free
- Keto/Low-carb
- Paleo
- Allergies

## API Reference

See [docs/API.md](docs/API.md) for complete API documentation.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - See LICENSE.md for details

## Troubleshooting

### "No API key found"
Make sure you've set the appropriate environment variable for your chosen provider.

### "Rate limit exceeded"
If using paid APIs, you may need to upgrade your plan or wait before making more requests.

### "Model not found" (Ollama)
Make sure you've pulled the model: `ollama pull llama2`

## Credits

Built with:
- OpenAI GPT-4 / GPT-3.5
- Anthropic Claude
- Ollama for local models
- Flask for web interface
- Rich for beautiful CLI output

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Note**: This application uses AI to generate recipes and cooking advice. While generally accurate, always use common sense and food safety practices when cooking.
