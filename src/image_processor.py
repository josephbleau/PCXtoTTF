"""
Module for processing PCX images and extracting character data.
"""
import numpy as np
from PIL import Image
from typing import Tuple, List

class ImageProcessor:
    """Handles loading and processing of PCX images for font creation."""
    
    def __init__(self, pcx_path: str):
        """
        Initialize the image processor with a PCX file path.
        
        Args:
            pcx_path: Path to the PCX image file
        """
        self.pcx_path = pcx_path
        self.image_array = None
        self.char_width = 8  # Fixed 8x8 characters
        self.char_height = 8
        
    def load_image(self) -> np.ndarray:
        """
        Load the PCX image and convert it to a numpy array.
        
        Returns:
            numpy.ndarray: The image data as a numpy array
            
        Raises:
            IOError: If the image cannot be loaded
        """
        try:
            img = Image.open(self.pcx_path)
            print(f"Image loaded successfully:")
            print(f"Size: {img.size}")
            print(f"Mode: {img.mode}")
            print(f"Format: {img.format}")
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                print("Converting image to RGBA mode...")
                img = img.convert('RGBA')
            
            self.image_array = np.array(img)
            return self.image_array
        except Exception as e:
            raise IOError(f"Error loading PCX image: {e}")
    
    def detect_character_size(self) -> Tuple[int, int]:
        """
        Return the fixed character size.
        
        Returns:
            Tuple[int, int]: (char_width, char_height)
        """
        return self.char_width, self.char_height
    
    def extract_characters(self) -> List[np.ndarray]:
        """
        Extract individual 8x8 characters from the spritesheet.
        Starting from top-left (0,0) and mapping to ASCII values starting at 32 (space).
        
        Returns:
            List[np.ndarray]: List of character images as numpy arrays
        """
        if self.image_array is None:
            raise ValueError("Image not loaded. Call load_image() first.")
            
        # Fixed 16x6 grid of 8x8 characters
        chars_per_row = 16
        chars_per_col = 6
        print(f"Extracting {chars_per_row * chars_per_col} characters in a {chars_per_row}x{chars_per_col} grid")
        
        characters = []
        ascii_value = 32  # Start with space character
        
        for row in range(chars_per_col):
            for col in range(chars_per_row):
                y_start = row * 8
                x_start = col * 8
                char_img = self.image_array[y_start:y_start + 8, x_start:x_start + 8]
                
                # Save debug image for each character with a safe filename
                debug_img = Image.fromarray(char_img)
                debug_img.save(f"debug_char_ascii_{ascii_value:03d}.png")
                
                characters.append(char_img)
                ascii_value += 1
        
        return characters 