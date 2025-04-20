"""
Main script for converting PCX spritesheets to TTF fonts.
"""
import sys
import os
from image_processor import ImageProcessor
from font_creator import FontCreator

def convert_pcx_to_ttf(pcx_path: str, output_path: str):
    """
    Convert a PCX spritesheet to a TTF font.
    
    Args:
        pcx_path: Path to the input PCX file
        output_path: Path where the output TTF file should be saved
    """
    print(f"Converting {pcx_path} to {output_path}")
    
    # Process the image
    processor = ImageProcessor(pcx_path)
    processor.load_image()
    char_width, char_height = processor.detect_character_size()
    characters = processor.extract_characters()
    
    # Create the font
    creator = FontCreator(characters, char_width, char_height)
    creator.create_font()
    creator.save_font(output_path)
    
    print("Conversion complete!")

def main():
    """Main entry point for the script."""
    if len(sys.argv) != 3:
        print("Usage: python pcx_to_ttf.py <input.pcx> <output.ttf>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not input_path.lower().endswith('.pcx'):
        print("Input file must be a PCX file")
        sys.exit(1)
    
    if not output_path.lower().endswith('.ttf'):
        print("Output file must be a TTF file")
        sys.exit(1)
    
    convert_pcx_to_ttf(input_path, output_path)

if __name__ == "__main__":
    main() 