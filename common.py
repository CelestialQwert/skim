from PIL import Image, ImageFont
import pygame

pygame.init()

FPS = 20

FONTS = {
    'GameOver': ImageFont.truetype("./fonts/GameCube.ttf", 16),
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
    'B500':   0x0004,
    'B400':   0x0008,
    'B300':   0x0010,
    'B200':   0x0020,
    'B100':   0x0040,
    'BRET':   0x0080, 
    'SELECT': 0x0400,
    'START':  0x0200,
    'ANYBUTTON': 0x0600,
    'CONFIG': 0x0100,
    'SCORED': 0x007F,
    'ANY': 0xFFFF
}

SOUNDS = {
    'START': pygame.mixer.Sound("sounds/great_balls_of_fire.ogg"),
    'OVER9000': pygame.mixer.Sound("sounds/its_over_9000.ogg"),
    'PLACE1': pygame.mixer.Sound("sounds/place_1.ogg"),
    'PLACE2': pygame.mixer.Sound("sounds/place_2.ogg"),
    'PLACE3': pygame.mixer.Sound("sounds/place_3.ogg"),
    'PLACE4': pygame.mixer.Sound("sounds/place_4.ogg"),
    'PLACE5': pygame.mixer.Sound("sounds/place_5.ogg"),
    'SCORE100': pygame.mixer.Sound("sounds/sonic_ring.ogg"),
    'SCORE200': pygame.mixer.Sound("sounds/mario_coin.ogg"),
    'SCORE300': pygame.mixer.Sound("sounds/pac_man_wakka.ogg"),
    'SCORE400': pygame.mixer.Sound("sounds/mega_man_item_get.ogg"),
    'SCORE500': pygame.mixer.Sound("sounds/colossus_roar.ogg"),
    'SCORE1000': pygame.mixer.Sound("sounds/colossus_roar.ogg"),
}

MUSIC = {
    'BK2000': pygame.mixer.Sound("sounds/black_knight_2000.ogg"),
    'SKEEBALL': pygame.mixer.Sound("sounds/skeeball_jingle.ogg"),
    'SF2': pygame.mixer.Sound("sounds/street_fighter_ii.ogg"),
}

MUSIC_KEYS = list(MUSIC.keys())


BALL_COLORS = [
    (255,0,0),
    (255,0,0),
    (255,255,0),
    (255,255,0),
    (0,255,0),
    (0,255,0),
    (0,255,0),
    (0,255,0),
    (0,255,0),
    (0,255,0),
]