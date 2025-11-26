#!/usr/bin/env python3
"""
Generate app icons for Recipe LLM PWA
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available. Install with: pip install Pillow")

import os


def create_icon(size, output_path):
    """Create a simple app icon."""
    # Create a new image with purple gradient background
    img = Image.new('RGB', (size, size), color='#667eea')
    draw = ImageDraw.Draw(img)

    # Draw a gradient effect
    for i in range(size):
        # Calculate color for gradient
        ratio = i / size
        r = int(102 + (118 - 102) * ratio)  # 667eea to 764ba2
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)
        color = (r, g, b)
        draw.line([(0, i), (size, i)], fill=color)

    # Draw a chef hat emoji or symbol
    try:
        # Try to use emoji or symbol
        font_size = size // 2
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # Draw chef hat emoji or text
        text = "🍳"

        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Center the text
        x = (size - text_width) // 2
        y = (size - text_height) // 2

        draw.text((x, y), text, fill='white', font=font)
    except Exception as e:
        # Fallback: draw a simple circle
        padding = size // 4
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill='white',
            outline='#667eea',
            width=size // 20
        )

        # Draw a smaller circle inside
        padding2 = size // 3
        draw.ellipse(
            [padding2, padding2, size - padding2, size - padding2],
            fill='#667eea'
        )

    # Save the image
    img.save(output_path, 'PNG')
    print(f"Created icon: {output_path} ({size}x{size})")


def main():
    """Generate all icon sizes."""
    if not PIL_AVAILABLE:
        print("\nERROR: Pillow (PIL) is required to generate icons.")
        print("Install it with: pip install Pillow")
        print("\nAlternatively, you can:")
        print("1. Use an online icon generator: https://www.pwabuilder.com/imageGenerator")
        print("2. Create icons manually using image editing software")
        print("3. Use the placeholder icons (they may not look perfect)")
        return

    # Icon sizes for PWA
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]

    # Create icons directory
    icons_dir = os.path.join(os.path.dirname(__file__), 'static', 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    print("\nGenerating Recipe LLM icons...")
    print("="*60)

    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
        create_icon(size, output_path)

    print("="*60)
    print(f"\nAll icons generated successfully in: {icons_dir}")
    print("\nYou can now:")
    print("1. Run the web app: python src/web_app.py")
    print("2. Install the PWA on your iPhone!")
    print("\nNote: For better looking icons, consider using a professional")
    print("icon generator like https://www.pwabuilder.com/imageGenerator")


if __name__ == '__main__':
    main()
