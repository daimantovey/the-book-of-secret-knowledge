#!/usr/bin/env python3
"""
Command-line interface for Recipe LLM
"""

import sys
import argparse
from recipe_llm import RecipeLLM


try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def print_response(response: str, use_rich: bool = True):
    """Print response with formatting."""
    if use_rich and RICH_AVAILABLE:
        console = Console()
        md = Markdown(response)
        console.print(Panel(md, title="Recipe LLM Response", border_style="green"))
    else:
        print("\n" + "="*80)
        print(response)
        print("="*80 + "\n")


def interactive_mode(provider: str = "openai"):
    """Run in interactive mode."""
    if RICH_AVAILABLE:
        console = Console()
        console.print("\n[bold green]Recipe LLM - Interactive Mode[/bold green]")
        console.print("[yellow]Type 'exit' or 'quit' to exit[/yellow]")
        console.print("[yellow]Type 'clear' to clear conversation history[/yellow]\n")
    else:
        print("\nRecipe LLM - Interactive Mode")
        print("Type 'exit' or 'quit' to exit")
        print("Type 'clear' to clear conversation history\n")

    try:
        llm = RecipeLLM(provider=provider)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        print("\nMake sure to set your API key:")
        print(f"  export OPENAI_API_KEY='your-key'")
        print(f"  export ANTHROPIC_API_KEY='your-key'")
        print("\nOr use Ollama for local models:")
        print(f"  python {sys.argv[0]} --provider ollama")
        sys.exit(1)

    while True:
        try:
            if RICH_AVAILABLE:
                question = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            else:
                question = input("\nYou: ").strip()

            if not question:
                continue

            if question.lower() in ['exit', 'quit', 'q']:
                if RICH_AVAILABLE:
                    console.print("[yellow]Goodbye![/yellow]")
                else:
                    print("Goodbye!")
                break

            if question.lower() == 'clear':
                llm.clear_history()
                if RICH_AVAILABLE:
                    console.print("[yellow]Conversation history cleared![/yellow]")
                else:
                    print("Conversation history cleared!")
                continue

            # Get response
            response = llm.ask(question)
            print_response(response, RICH_AVAILABLE)

        except KeyboardInterrupt:
            if RICH_AVAILABLE:
                console.print("\n[yellow]Goodbye![/yellow]")
            else:
                print("\nGoodbye!")
            break
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Recipe LLM - AI-powered recipe and cooking assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ask a question
  %(prog)s "How do I make carbonara?"

  # Get a recipe
  %(prog)s "Give me a recipe for chocolate cake"

  # Interactive mode
  %(prog)s --interactive

  # Use a different provider
  %(prog)s --provider anthropic "What's a good vegan substitute for eggs?"

  # Use local models
  %(prog)s --provider ollama --interactive
        """
    )

    parser.add_argument(
        'question',
        nargs='*',
        help='Question to ask (if not in interactive mode)'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    parser.add_argument(
        '-p', '--provider',
        choices=['openai', 'anthropic', 'ollama'],
        default='openai',
        help='LLM provider to use (default: openai)'
    )

    parser.add_argument(
        '-m', '--model',
        help='Specific model to use'
    )

    parser.add_argument(
        '--recipe',
        help='Get a recipe for a specific dish'
    )

    parser.add_argument(
        '--servings',
        type=int,
        help='Number of servings (use with --recipe)'
    )

    parser.add_argument(
        '--dietary',
        nargs='+',
        help='Dietary restrictions (use with --recipe, e.g., --dietary vegan gluten-free)'
    )

    parser.add_argument(
        '--cuisine',
        help='Cuisine type (use with --recipe)'
    )

    parser.add_argument(
        '--substitute',
        help='Get substitution suggestions for an ingredient'
    )

    parser.add_argument(
        '--technique',
        help='Explain a cooking technique'
    )

    parser.add_argument(
        '--no-rich',
        action='store_true',
        help='Disable rich text formatting'
    )

    args = parser.parse_args()

    use_rich = RICH_AVAILABLE and not args.no_rich

    # Interactive mode
    if args.interactive:
        interactive_mode(args.provider)
        return

    # Initialize LLM
    try:
        llm = RecipeLLM(provider=args.provider, model=args.model)
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        print("\nMake sure to set your API key:")
        print(f"  export OPENAI_API_KEY='your-key'")
        print(f"  export ANTHROPIC_API_KEY='your-key'")
        print("\nOr use Ollama for local models:")
        print(f"  python {sys.argv[0]} --provider ollama")
        sys.exit(1)

    try:
        # Recipe mode
        if args.recipe:
            response = llm.get_recipe(
                args.recipe,
                dietary_restrictions=args.dietary,
                servings=args.servings,
                cuisine=args.cuisine
            )
            print_response(response, use_rich)

        # Substitution mode
        elif args.substitute:
            response = llm.get_substitution(args.substitute)
            print_response(response, use_rich)

        # Technique mode
        elif args.technique:
            response = llm.explain_technique(args.technique)
            print_response(response, use_rich)

        # Question mode
        elif args.question:
            question = ' '.join(args.question)
            response = llm.ask(question)
            print_response(response, use_rich)

        else:
            parser.print_help()

    except Exception as e:
        if use_rich and RICH_AVAILABLE:
            console = Console()
            console.print(f"[red]Error: {e}[/red]")
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
