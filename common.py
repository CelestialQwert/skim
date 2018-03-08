from PIL import Image, ImageFont

FPS = 20

FONTS = {
    'GameOver': ImageFont.truetype("fonts/GameCube.ttf", 16),
    'Tiny': ImageFont.load('fonts/4x6.pil'),
    'Small': ImageFont.load('fonts/5x7.pil'),
    'Medium': ImageFont.load('fonts/6x10.pil'),
    'Digital14': ImageFont.load('fonts/digital-14.pil'),
    'Digital16': ImageFont.load('fonts/digital-16.pil')
}

IMAGES = {
    'MainLogo' : Image.open('imgs/combined-logo.png')
}

BUTTON = { 
    'B1000L': 0x0001,
    'B1000R': 0x0002,
    'B500': 0x0004,
    'B400': 0x0008,
    'B300': 0x0010,
    'B200': 0x0020,
    'B100': 0x0040,
    'BRET': 0x0080, 
    'SELECT': 0x0400,
    'START': 0x0200,
    'ANYBUTTON': 0x600,
    'CONFIG': 0x800,
    'SCORED': 0x007F,
    'ANY': 0xFFFF
}
   