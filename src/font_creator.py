"""
Module for creating and manipulating TrueType fonts.
"""
from typing import List
import numpy as np
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.ttLib.tables._n_a_m_e import NameRecord
from fontTools.misc.textTools import bytechr
from fontTools.ttLib.tables.O_S_2f_2 import Panose

class FontCreator:
    """Handles creation and manipulation of TrueType fonts."""
    
    def __init__(self, characters: List[np.ndarray], char_width: int, char_height: int):
        """
        Initialize the font creator with character data.
        
        Args:
            characters: List of character images as numpy arrays
            char_width: Width of each character
            char_height: Height of each character
        """
        self.characters = characters
        self.char_width = 8  # Fixed 8x8 grid
        self.char_height = 8  # Fixed 8x8 grid
        self.units_per_em = 1024  # Standard value
        self.scale = self.units_per_em // 8  # Scale factor to convert 8x8 grid to font units
        self.font = None
        self.glyph_names = None
        
    def create_font(self) -> TTFont:
        """
        Create a new TTF font with the provided characters.
        
        Returns:
            TTFont: The created font object
        """
        print("\nStep 4: Creating font...")
        
        # Create a new font
        print("Initializing new TTFont object...")
        self.font = TTFont()
        
        # Create glyph names including space and .notdef
        print("Creating glyph order...")
        self.glyph_names = ['.notdef']  # Start with .notdef
        for i in range(len(self.characters)):
            self.glyph_names.append(f'glyph{i+1:05d}')
        # Add space character to glyph order
        self.glyph_names.append(f'glyph{len(self.characters)+1:05d}')
        
        # Set the glyph order
        print(f"Setting glyph order with {len(self.glyph_names)} glyphs...")
        self.font.setGlyphOrder(self.glyph_names)
        
        # Initialize required tables
        print("Initializing required tables...")
        self._create_head_table()
        self._create_hhea_table()
        self._create_maxp_table()
        self._create_os2_table()
        self._create_hmtx_table()
        self._create_name_table()
        self._create_cmap_table()
        self._create_post_table()
        self._create_glyf_table()  # Initialize glyf table first
        
        # Create glyphs
        self._create_glyphs()
        
        return self.font
    
    def _create_head_table(self):
        """Create and initialize the head table."""
        print("Creating head table...")
        head = newTable('head')
        head.tableVersion = 1.0
        head.fontRevision = 1.0
        head.checkSumAdjustment = 0
        head.magicNumber = 0x5F0F3CF5
        head.flags = 0
        head.unitsPerEm = self.units_per_em
        head.created = 3543565422  # Current time
        head.modified = 3543565422
        head.xMin = 0
        head.yMin = 0
        head.xMax = self.char_width * self.scale
        head.yMax = self.char_height * self.scale
        head.macStyle = 0
        head.lowestRecPPEM = 8
        head.fontDirectionHint = 2
        head.indexToLocFormat = 0
        head.glyphDataFormat = 0
        self.font['head'] = head
    
    def _create_hhea_table(self):
        """Create and initialize the hhea table."""
        print("Creating hhea table...")
        hhea = newTable('hhea')
        hhea.tableVersion = 0x00010000
        hhea.ascent = self.char_height * self.scale
        hhea.descent = 0
        hhea.lineGap = self.scale  # One pixel gap
        hhea.advanceWidthMax = self.char_width * self.scale
        hhea.minLeftSideBearing = 0
        hhea.minRightSideBearing = 0
        hhea.xMaxExtent = self.char_width * self.scale
        hhea.caretSlopeRise = 1
        hhea.caretSlopeRun = 0
        hhea.caretOffset = 0
        hhea.reserved0 = 0
        hhea.reserved1 = 0
        hhea.reserved2 = 0
        hhea.reserved3 = 0
        hhea.metricDataFormat = 0
        hhea.numberOfHMetrics = len(self.glyph_names)  # Include all glyphs including space
        self.font['hhea'] = hhea
    
    def _create_maxp_table(self):
        """Create and initialize the maxp table."""
        print("Creating maxp table...")
        maxp = newTable('maxp')
        maxp.tableVersion = 0x00010000
        maxp.numGlyphs = len(self.glyph_names)  # Include all glyphs including space
        maxp.maxPoints = 4  # Rectangle for each pixel
        maxp.maxContours = 1  # One contour per pixel
        maxp.maxCompositePoints = 0
        maxp.maxCompositeContours = 0
        maxp.maxZones = 1
        maxp.maxTwilightPoints = 0
        maxp.maxStorage = 0
        maxp.maxFunctionDefs = 0
        maxp.maxInstructionDefs = 0
        maxp.maxStackElements = 0
        maxp.maxSizeOfInstructions = 0
        maxp.maxComponentElements = 0
        maxp.maxComponentDepth = 0
        self.font['maxp'] = maxp
    
    def _create_os2_table(self):
        """Create and initialize the OS/2 table."""
        print("Creating OS/2 table...")
        os2 = newTable('OS/2')
        os2.version = 4
        os2.xAvgCharWidth = self.char_width * self.scale
        os2.usWeightClass = 400
        os2.usWidthClass = 5
        os2.fsType = 0
        os2.ySubscriptXSize = self.char_width * self.scale
        os2.ySubscriptYSize = self.char_height * self.scale
        os2.ySubscriptXOffset = 0
        os2.ySubscriptYOffset = 0
        os2.ySuperscriptXSize = self.char_width * self.scale
        os2.ySuperscriptYSize = self.char_height * self.scale
        os2.ySuperscriptXOffset = 0
        os2.ySuperscriptYOffset = self.char_height * self.scale
        os2.yStrikeoutSize = self.scale  # One pixel
        os2.yStrikeoutPosition = 4 * self.scale  # Middle of height
        os2.sFamilyClass = 0
        
        # Create Panose object
        os2.panose = Panose()
        os2.panose.bFamilyType = 0
        os2.panose.bSerifStyle = 0
        os2.panose.bWeight = 0
        os2.panose.bProportion = 0
        os2.panose.bContrast = 0
        os2.panose.bStrokeVariation = 0
        os2.panose.bArmStyle = 0
        os2.panose.bLetterForm = 0
        os2.panose.bMidline = 0
        os2.panose.bXHeight = 0
        
        os2.ulUnicodeRange1 = 1  # Basic Latin
        os2.ulUnicodeRange2 = 0
        os2.ulUnicodeRange3 = 0
        os2.ulUnicodeRange4 = 0
        os2.achVendID = 'NONE'
        os2.fsSelection = 0
        os2.usFirstCharIndex = 32  # Space
        os2.usLastCharIndex = 32 + len(self.characters)
        os2.sTypoAscender = self.char_height * self.scale
        os2.sTypoDescender = 0
        os2.sTypoLineGap = self.scale  # One pixel gap
        os2.usWinAscent = self.char_height * self.scale
        os2.usWinDescent = 0
        os2.ulCodePageRange1 = 0x00000001  # Latin 1
        os2.ulCodePageRange2 = 0
        os2.sxHeight = self.char_height * self.scale
        os2.sCapHeight = self.char_height * self.scale
        os2.usDefaultChar = 0
        os2.usBreakChar = 32  # Space
        os2.usMaxContext = 0
        self.font['OS/2'] = os2
    
    def _create_hmtx_table(self):
        """Create and initialize the hmtx table."""
        print("Creating hmtx table...")
        hmtx = newTable('hmtx')
        hmtx.metrics = {}
        self.font['hmtx'] = hmtx
    
    def _create_name_table(self):
        """Create and initialize the name table."""
        print("Creating name table...")
        name = newTable('name')
        name.names = []
        
        # Convert tuples to NameRecord objects
        name_strings = [
            (1, 'PCXFont'),  # family name
            (2, 'Regular'),  # style name
            (3, 'PCXFont-Regular'),  # unique ID
            (4, 'PCXFont Regular'),  # full name
            (5, 'Version 1.0'),  # version
            (6, 'PCXFont-Regular')  # postscript name
        ]
        
        for nameID, string in name_strings:
            record = NameRecord()
            record.platformID = 3  # Windows
            record.platEncID = 1   # Unicode
            record.langID = 0x409  # English (US)
            record.nameID = nameID
            record.string = string.encode('utf-16be')
            name.names.append(record)
        
        self.font['name'] = name
    
    def _create_cmap_table(self):
        """Create and initialize the cmap table."""
        print("Creating cmap table...")
        # Create the cmap table first
        self.font['cmap'] = newTable('cmap')
        cmap = self.font['cmap']
        cmap.tableVersion = 0
        
        # Create format 4 subtable (Unicode)
        format4 = CmapSubtable.newSubtable(4)
        format4.platformID = 3  # Windows
        format4.platEncID = 1   # Unicode
        format4.language = 0
        
        # Initialize empty cmap
        format4.cmap = {}
        
        # Add .notdef mapping
        format4.cmap[0] = '.notdef'
        
        # Add to cmap table
        cmap.tables = [format4]
    
    def _create_post_table(self):
        """Create and initialize the post table."""
        print("Creating post table...")
        post = newTable('post')
        post.formatType = 3.0  # No glyph names, just indices
        post.italicAngle = 0
        post.underlinePosition = -1
        post.underlineThickness = 1
        post.isFixedPitch = 1
        post.minMemType42 = 0
        post.maxMemType42 = 0
        post.minMemType1 = 0
        post.maxMemType1 = 0
        self.font['post'] = post
    
    def _create_glyf_table(self):
        """Create and initialize the glyf table."""
        print("Creating glyf table...")
        self.font['glyf'] = newTable('glyf')
        self.font['glyf'].glyphs = {}  # Initialize the glyphs dictionary
        self.font['loca'] = newTable('loca')  # Also create the loca table
    
    def _create_glyphs(self):
        """Create glyphs for each character."""
        print("\nStep 5: Creating glyphs...")
        print(f"Processing {len(self.characters)} characters...")
        
        def is_background(pixel):
            """Helper to check if a pixel is the salmon background color (#9F5B53)."""
            bg_r, bg_g, bg_b = 0x9F, 0x5B, 0x53
            r, g, b = pixel[0], pixel[1], pixel[2]
            return r == bg_r and g == bg_g and b == bg_b
        
        # Create .notdef glyph first
        pen = TTGlyphPen(self.font)
        pen.moveTo((0, 0))
        pen.lineTo((self.char_width * self.scale, 0))
        pen.lineTo((self.char_width * self.scale, self.char_height * self.scale))
        pen.lineTo((0, self.char_height * self.scale))
        pen.closePath()
        self.font['glyf'].glyphs['.notdef'] = pen.glyph()  # Use .glyphs dictionary
        self.font['hmtx'].metrics['.notdef'] = (self.char_width * self.scale, 0)
        
        # Create glyphs
        for i, char_img in enumerate(self.characters):
            print(f"\nProcessing character {i+1}/{len(self.characters)}...")
            pen = TTGlyphPen(self.font)
            
            # Process each pixel in the character
            height, width = char_img.shape[:2]
            has_pixels = False
            pixel_count = 0
            
            # For each pixel that isn't background, create a solid square
            for y in range(height):
                for x in range(width):
                    if not is_background(char_img[y, x]):
                        has_pixels = True
                        pixel_count += 1
                        # Scale coordinates to font units
                        x0 = x * self.scale
                        y0 = (7 - y) * self.scale  # Flip Y coordinates
                        x1 = (x + 1) * self.scale
                        y1 = (8 - y) * self.scale  # Flip Y coordinates
                        
                        # Draw a solid square for this pixel
                        pen.moveTo((x0, y0))
                        pen.lineTo((x1, y0))
                        pen.lineTo((x1, y1))
                        pen.lineTo((x0, y1))
                        pen.closePath()
            
            # Add the glyph to the font
            glyph_name = f'glyph{i+1:05d}'
            
            # If no pixels were drawn, create an empty glyph
            if not has_pixels:
                pen = TTGlyphPen(self.font)
                pen.moveTo((0, 0))
                pen.lineTo((0, 0))
                pen.closePath()
                print(f"  Empty glyph (no pixels)")
            else:
                print(f"  Found {pixel_count} pixels")
            
            self.font['glyf'].glyphs[glyph_name] = pen.glyph()  # Use .glyphs dictionary
            
            # Set character width
            self.font['hmtx'].metrics[glyph_name] = (self.char_width * self.scale, 0)
            
            # Simple sequential mapping starting from ASCII 33 (!)
            # Skip ASCII 32 (space) as it's special
            base_ascii = 33 + i - 1  # Base ASCII value
            original_pos = base_ascii + 32  # Convert back to original position
            
            # For letters (a-z), use the base ASCII value
            if base_ascii >= ord('a') and base_ascii <= ord('z'):
                ascii_value = base_ascii
            # For special characters, subtract 32 to get the correct mapping
            else:
                ascii_value = base_ascii - 32
            
            # If this is one of our original non-standard characters (32-63),
            # map it to positions after '=' (61)
            if original_pos >= 32 and original_pos <= 63:
                # Map to positions starting at 62 (right after '=')
                ascii_value = 62 + (original_pos - 32)
            
            # Add to cmap subtable
            self.font['cmap'].tables[0].cmap[ascii_value] = glyph_name
            print(f"  Primary mapping to ASCII {ascii_value} ({chr(ascii_value)})")
            
            # If this is a lowercase letter (a-z), also map it to uppercase (A-Z)
            if ascii_value >= ord('a') and ascii_value <= ord('z'):
                uppercase_ascii = ascii_value - 32  # Convert to uppercase ASCII
                self.font['cmap'].tables[0].cmap[uppercase_ascii] = glyph_name
                print(f"  Also mapping to uppercase ASCII {uppercase_ascii} ({chr(uppercase_ascii)})")
            
            # For all characters beyond '=' (ASCII 61), map them to extended ASCII
            if original_pos > 61:
                extended_ascii = ascii_value + 128  # Map to extended ASCII range
                self.font['cmap'].tables[0].cmap[extended_ascii] = glyph_name
                print(f"  Also mapping to extended ASCII {extended_ascii}")
                
                # Also map to Private Use Area as a backup
                private_use_code = 0xE000 + (original_pos - 32)
                self.font['cmap'].tables[0].cmap[private_use_code] = glyph_name
                print(f"  Also mapping to Private Use Area U+{private_use_code:04X}")
            
        # Add space character at the end
        space_glyph = f'glyph{len(self.characters)+1:05d}'
        pen = TTGlyphPen(self.font)
        pen.moveTo((0, 0))
        pen.lineTo((0, 0))
        pen.closePath()
        self.font['glyf'].glyphs[space_glyph] = pen.glyph()
        self.font['hmtx'].metrics[space_glyph] = (self.char_width * self.scale, 0)
        self.font['cmap'].tables[0].cmap[32] = space_glyph  # ASCII 32 is space
        print("\nAdded space character (ASCII 32)")
    
    def save_font(self, output_path: str):
        """
        Save the font to a file.
        
        Args:
            output_path: Path where the font should be saved
        """
        if self.font is None:
            raise ValueError("Font not created. Call create_font() first.")
            
        print("\nStep 6: Saving font...")
        self.font.save(output_path)
        print(f"Font saved to {output_path}") 