# PCX to TTF Font Converter

This tool converts PCX spritesheet images into TTF font files. It's particularly useful for converting old game spritesheets into usable fonts.

## Requirements

- Python 3.8 or higher
- Pillow
- FontForge
- NumPy

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Install FontForge:
   - Windows: Download and install from [FontForge's website](https://fontforge.org/en-US/downloads/)
   - Linux: `sudo apt-get install fontforge`
   - macOS: `brew install fontforge`

## Usage

```bash
python src/pcx_to_ttf.py input.pcx output.ttf
```

The tool will:
1. Load the PCX spritesheet
2. Automatically detect character dimensions
3. Extract individual characters
4. Create a TTF font file

## Notes

- The input PCX file should be a spritesheet with characters arranged in a grid
- The tool assumes uniform character sizes and spacing
- Characters will be mapped to ASCII codes starting from space (32)
- The output font will be named "PCXFont"

## Limitations

- Currently only supports monochrome images
- Character detection assumes uniform spacing
- May need manual adjustment for optimal results with some spritesheets 