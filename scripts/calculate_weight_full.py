import trimesh
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont

## READING CONFIG TO GET LOGO_PATH
def get_logo_path():
    """Read the configuration file and return the logo path."""
    bat_config_path = os.environ.get('BAT_CONFIG_PATH')
    with open(bat_config_path, 'r') as file:
        for line in file:
            if line.startswith("LOGO_PATH="):
                return line.strip().split('=')[1]
    return None

# Function to draw rounded rectangle
def draw_rounded_rectangle(draw, position, border_radius, fill):
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

    # Optional delay
    sleep_time = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    time.sleep(sleep_time)

    stl_path = os.path.join(current_directory, file_name + ".stl")
    mesh = trimesh.load_mesh(stl_path, file_type='stl')
    components = mesh.split(only_watertight=False)

    # --- Materials & densities (kg/m^3) ---
    # Note: Actual density varies by color/alloy recipe; these are typical values used in jewelry.
    density_values = {
        "9k Gold":            11200,  # ~11.2 g/cm^3
        "10k Gold":           11570,  # ~11.57 g/cm^3
        "14k Gold":           12600,  # ~12.6 g/cm^3 (mid-range)
        "18k Gold":           15300,  # ~15.3 g/cm^3 (yellow avg)
        "925 Silver":         10490,  # sterling
        "Platinum 950":       21450,  # ~21.45 g/cm^3
        "Palladium 950":      12000,  # ~12.0 g/cm^3
        "Stainless Steel":    8000,  # ~8.0 g/cm^3
        "Titanium":           4430,  # ~4.43 g/cm^3
        "Tungsten":           15600,  # ~15.6 g/cm^3
        "Brass":              8500,  # costume jewelry, findings
        "Bronze":             8800,
    }

    # Initialize totals
    total_weights = {material: 0.0 for material in density_values.keys()}

    # Sum up total volume per material (volume in mm^3; convert to grams)
    # mass(g) = density(kg/m^3) * volume(mm^3) / 1e6
    for component in components:
        volume = component.volume  # assumes mesh units are mm
        for material, density in density_values.items():
            total_weights[material] += (volume * density) / 1_000_000

    # ------- Image/table -------
    # Layout constants
    padding = 10
    header_height = 30
    row_height = 25
    logo_height = 40
    column_width = 170

    num_rows = len(total_weights)
    img_width = 2 * padding + column_width * 2 + 10
    img_height = 2 * padding + header_height + num_rows * row_height + logo_height + 10

    img = Image.new('RGBA', (img_width, img_height), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)

    # Load & resize logo
    logo_path = get_logo_path()
    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_aspect_ratio = logo.width / logo.height
        logo_width = int(logo_aspect_ratio * logo_height)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    else:
        logo = None
        logo_width = 0

    # Fonts
    try:
        header_font = ImageFont.truetype("arialbd.ttf", 18)
        regular_font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        header_font = ImageFont.load_default()
        regular_font = ImageFont.load_default()

    # Table background
    border_radius = 15
    draw_rounded_rectangle(
        d,
        [5, 5, img_width - 5, img_height - 5 - (logo_height + 5)],
        border_radius,
        (255, 255, 255, 255)
    )

    # Headers
    start_x, start_y = padding + 5, padding + 5
    d.text((start_x, start_y), "Material", fill=(0, 0, 0), font=header_font)
    d.text((start_x + column_width, start_y), "Weight (g)", fill=(0, 0, 0), font=header_font)

    # Rows
    y = start_y + header_height
    for material, weight in total_weights.items():
        d.text((start_x, y), material, fill=(0, 0, 0), font=regular_font)
        d.text((start_x + column_width, y), f"{weight:.2f}", fill=(0, 0, 0), font=regular_font)
        y += row_height

    # Logo in bottom-right
    if logo:
        img.paste(logo, (img.width - logo_width, img.height - logo_height), logo)

    # Save
    final_img = img.convert("RGB")
    img_path = os.path.join(current_directory, "WEIGHT.png")
    final_img.save(img_path, "PNG")

    print(f"Image saved to {img_path}")

if __name__ == '__main__':
    main()
