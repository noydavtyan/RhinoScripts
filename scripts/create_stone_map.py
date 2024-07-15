import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont

def get_logo_path():
    """Read the configuration file and return the Python path."""
    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("LOGO_PATH="):
                return line.strip().split('=')[1]
    return None

def draw_rounded_rectangle(draw, position, border_radius, fill, width=0):
    x0, y0, x1, y1 = position
    draw.rectangle([(x0, y0 + border_radius), (x1, y1 - border_radius)], fill=fill)
    draw.rectangle([(x0 + border_radius, y0), (x1 - border_radius, y1)], fill=fill)
    draw.pieslice([(x0, y0), (x0 + 2 * border_radius, y0 + 2 * border_radius)], 180, 270, fill=fill)
    draw.pieslice([(x1 - 2 * border_radius, y0), (x1, y0 + 2 * border_radius)], 270, 360, fill=fill)
    draw.pieslice([(x0, y1 - 2 * border_radius), (x0 + 2 * border_radius, y1)], 90, 180, fill=fill)
    draw.pieslice([(x1 - 2 * border_radius, y1 - 2 * border_radius), (x1, y1)], 0, 90, fill=fill)

def main():
    # Load a mesh
    current_directory = sys.argv[1].replace("\\\\", "/").replace("\\", "/").replace("\"","")
    file_name = sys.argv[2]
    gem_data = sys.argv[3]
    if gem_data == "":
        return
    create_stone_map_image(gem_data, current_directory)

def create_stone_map_image(formatted_data, current_directory):

    # Image setup
    img_width, img_height = 400, 300
    img = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load and resize logo
    logo_path = get_logo_path()
    logo = Image.open(logo_path).convert("RGBA")
    logo_aspect_ratio = logo.width / logo.height
    logo_height = 40
    logo_width = int(logo_aspect_ratio * logo_height)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    # Define fonts
    try:
        header_font = ImageFont.truetype("arialbd.ttf", 18)  # Bold and larger for headers
        regular_font = ImageFont.truetype("arial.ttf", 15)   # Regular for entries
    except IOError:
        header_font = ImageFont.load_default()
        regular_font = ImageFont.load_default()

    # Define table layout
    start_x, start_y, line_height, column_width = 10, 10, 25, 225

    # Draw rounded rectangle as table background
    border_radius = 15
    draw_rounded_rectangle(draw, [5, 5, img_width - 5, img_height - 5], border_radius, (255, 255, 255, 255))
    #Draw headers
    draw.text((start_x, start_y), "Stone Map", fill=(0,0,0), font=header_font)
    # Draw headers and gem data
    draw.text((start_x, start_y), formatted_data, fill=(0,0,0), font=regular_font)
    start_y += line_height

    # Paste the logo in the bottom-right corner
    img.paste(logo, (img.width - logo_width, img.height - logo_height), logo)

    # Convert to RGB and save the image
    final_img = img.convert("RGB")
    img_path = os.path.join(current_directory, "STONE_MAP.png")
    final_img.save(img_path, "PNG")
    print(f"Image saved to {img_path}")

if __name__ == '__main__':
    main()
