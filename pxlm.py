import argparse
from PIL import Image

def validate_pxlm(filepath):
    """
    Validate and correct a `.pxlm` file.
    Automatically calculates width and height.
    """
    corrected_lines = []
    width = None

    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Validate pixel rows
    for i, line in enumerate(lines):
        row = line.strip().split()
        if i == 0:  # Set width based on the first row
            width = len(row)
        elif len(row) != width:
            raise ValueError(f"Inconsistent row width at line {i + 1}. Expected {width}, got {len(row)}.")

        # Replace missing pixels with black
        corrected_row = [px if len(px) == 6 else "000000" for px in row]
        corrected_lines.append(" ".join(corrected_row))

    height = len(corrected_lines)

    # Save corrected version
    corrected_file = filepath.replace(".pxlm", "_corrected.pxlm")
    with open(corrected_file, 'w') as file:
        file.write("\n".join(corrected_lines) + "\n")

    print(f"File validated and corrected: {corrected_file}")
    print(f"Width: {width}, Height: {height}")

def image_to_pxlm(image_path, output_pxlm):
    """
    Convert PNG/JPEG/JPG/WebP to .pxlm format.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Ensure RGB mode
        width, height = img.size
        pixels = []

        # Extract pixel data
        for y in range(height):
            row = []
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                hex_color = f"{r:02X}{g:02X}{b:02X}"
                row.append(hex_color)
            pixels.append(" ".join(row))
        
        # Save as .pxlm
        with open(output_pxlm, 'w') as file:
            file.write("\n".join(pixels) + "\n")

    print(f"Image converted to .pxlm: {output_pxlm}")

def pxlm_to_image(pxlm_path, output_image):
    """
    Convert .pxlm to PNG format.
    """
    with open(pxlm_path, 'r') as file:
        lines = file.readlines()

    # Detect width and height
    width = len(lines[0].strip().split())
    height = len(lines)

    # Read pixel data
    pixels = []
    for line in lines:
        row = line.strip().split()
        pixels.extend([(int(px[:2], 16), int(px[2:4], 16), int(px[4:], 16)) for px in row])

    # Create image
    img = Image.new("RGB", (width, height))
    img.putdata(pixels)
    img.save(output_image)
    print(f".pxlm converted to image: {output_image}")

def main():
    parser = argparse.ArgumentParser(description="Pixel Matrix Language (PXLM) File Operations")
    
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for validating a .pxlm file
    validate_parser = subparsers.add_parser("validate", help="Validate and correct a .pxlm file")
    validate_parser.add_argument("filepath", help="Path to the .pxlm file to validate")

    # Subparser for converting an image to .pxlm
    image_to_pxlm_parser = subparsers.add_parser("image_to_pxlm", help="Convert an image (PNG, JPEG, etc.) to .pxlm format")
    image_to_pxlm_parser.add_argument("image_path", help="Path to the image file")
    image_to_pxlm_parser.add_argument("output_pxlm", help="Path to save the output .pxlm file")

    # Subparser for converting a .pxlm file to an image
    pxlm_to_image_parser = subparsers.add_parser("pxlm_to_image", help="Convert a .pxlm file to an image (PNG, JPEG, etc.)")
    pxlm_to_image_parser.add_argument("pxlm_path", help="Path to the .pxlm file")
    pxlm_to_image_parser.add_argument("output_image", help="Path to save the output image file")

    args = parser.parse_args()

    if args.command == "validate":
        validate_pxlm(args.filepath)
    elif args.command == "image_to_pxlm":
        image_to_pxlm(args.image_path, args.output_pxlm)
    elif args.command == "pxlm_to_image":
        pxlm_to_image(args.pxlm_path, args.output_image)
    else:
        print("Invalid command. Use -h for help.")

if __name__ == "__main__":
    main()
