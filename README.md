# WARNING: AI GENERATED CODE 

This project was a personal experiment to explore the current state of LLM-based IDE's. Specifically, Cursor and Python were used. Total time to complete was roughly 1.5 hours. I estimate that this project would have taken me personally 3-5 days, as someone who has no prior knowledge in creating fonts but does have experience working with Python.

From the outset I did NOT expect to get a working result, so I have to admit I am surprised with that. Although, this code is not maintainable by me what-so-ever. I know absolutely nothing more about TTF than I did when I started, and I didn't read a single line of this program. I have no idea how it works (aside from intuition and having been the one to describe what to build).

It was an informative experience, but god help us all if this becomes the status quo. More or less a miserable experience.

From:
![image](https://github.com/user-attachments/assets/b21e65c7-b1c7-423c-b9cb-7b97675328ed)

To:
![image](https://github.com/user-attachments/assets/c35cc511-23be-483b-96ef-7f6ddb28f8ea)


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
