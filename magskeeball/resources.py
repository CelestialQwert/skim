from PIL import Image, ImageFont
from pkg_resources import resource_filename
import pygame
from enum import Enum

def getfile(path):
    return resource_filename('magskeeball',path)

pygame.mixer.init()

FONTS = {
    'GameOver': ImageFont.truetype(getfile("fonts/GameCube.ttf"), 14),
    'MAGFest': ImageFont.truetype(getfile("fonts/radio_stars.otf"), 15),
    'MAGMini': ImageFont.truetype(getfile("fonts/radio_stars.otf"), 12),
    'Tiny': ImageFont.load(getfile('fonts/4x6.pil')),
    'Small': ImageFont.load(getfile('fonts/5x7.pil')),
    'Medium': ImageFont.load(getfile('fonts/6x10.pil')),
    'Digital14': ImageFont.load(getfile('fonts/digital-14.pil')),
    'Digital16': ImageFont.load(getfile('fonts/digital-16.pil'))
}

IMAGES = {
    'MainLogo' : Image.open(getfile('imgs/combined-logo.png'))
}

SOUNDS = {
    'OVER9000': pygame.mixer.Sound(getfile("sounds/its_over_9000.ogg")),
    'PLACE1': pygame.mixer.Sound(getfile("sounds/place_1.ogg")),
    'PLACE2': pygame.mixer.Sound(getfile("sounds/place_2.ogg")),
    'PLACE3': pygame.mixer.Sound(getfile("sounds/place_3.ogg")),
    'PLACE4': pygame.mixer.Sound(getfile("sounds/place_4.ogg")),
    'PLACE5': pygame.mixer.Sound(getfile("sounds/place_5.ogg")),
    'MISS': pygame.mixer.Sound(getfile("sounds/mario_death.ogg")),
    'B100': pygame.mixer.Sound(getfile("sounds/sonic_ring.ogg")),
    'B200': pygame.mixer.Sound(getfile("sounds/mario_coin.ogg")),
    'B300': pygame.mixer.Sound(getfile("sounds/pac_man_wakka.ogg")),
    'B400': pygame.mixer.Sound(getfile("sounds/mega_man_item_get.ogg")),
    'B500': pygame.mixer.Sound(getfile("sounds/colossus_roar.ogg")),
    'B1000L': pygame.mixer.Sound(getfile("sounds/colossus_roar.ogg")),
    'B1000R': pygame.mixer.Sound(getfile("sounds/colossus_roar.ogg")),
    'READY': pygame.mixer.Sound(getfile("sounds/ready.ogg")),
    'GO': pygame.mixer.Sound(getfile("sounds/go.ogg")),
}

ATTRACT_MUSIC = {
    'BK2000': pygame.mixer.Sound(getfile("sounds/black_knight_2000.ogg")),
    'SKEEBALL': pygame.mixer.Sound(getfile("sounds/skeeball_jingle.ogg")),
    'SF2': pygame.mixer.Sound(getfile("sounds/street_fighter_ii.ogg")),
    'SANIC': pygame.mixer.Sound(getfile("sounds/sonic_title.ogg")),
}

START_MUSIC = {
    'FIRE': pygame.mixer.Sound(getfile("sounds/great_balls_of_fire.ogg")),
    'WRECKING': pygame.mixer.Sound(getfile("sounds/wrecking_ball.ogg")),
    #'STEEL': pygame.mixer.Sound(getfile("sounds/balls_of_steel.ogg")),
    #'BIGBALLS': pygame.mixer.Sound(getfile("sounds/big_balls.ogg")),
}

TARGET_SFX = {
    'TARGET_INTRO': pygame.mixer.Sound(getfile("sounds/break_the_targets.ogg")),
    'TARGET_BG': pygame.mixer.Sound(getfile("sounds/target_theme.ogg")),
    'COMPLETE': pygame.mixer.Sound(getfile("sounds/complete.ogg")),
    'TARGET_HIT': pygame.mixer.Sound(getfile("sounds/target_hit.ogg")),
    'TARGET_MISS': pygame.mixer.Sound(getfile("sounds/target_miss.ogg")),
}

ATTRACT_MUSIC_KEYS = list(ATTRACT_MUSIC.keys())
START_MUSIC_KEYS = list(START_MUSIC.keys())


FPS = 20

#these map to the physical pins on the arduino except QUIT
class Button(Enum):
    QUIT    = 0
    NULL_01 = 1
    B1000L  = 2
    B1000R  = 3
    B500    = 4
    B400    = 5
    B300    = 6
    B200    = 7
    B100    = 8
    RETURN  = 9
    CONFIG  = 10
    START   = 11
    SELECT  = 12
    NULL_13 = 13
    NULL_14 = 14
    NULL_15 = 15
    NULL_16 = 16
    NULL_17 = 17
    NULL_18 = 18
    NULL_19 = 19

B = Button
BUTTON = Button

POINTS = {
    Button.B1000L: 1000,
    Button.B1000R: 1000,
    Button.B500: 500,
    Button.B400: 400,
    Button.B300: 300,
    Button.B200: 200,
    Button.B100: 100,
}

COLORS = {
    'BLACK': (0,0,0),
    'RED': (255,0,0),
    'YELLOW': (255,255,0),
    'GREEN': (0,255,0),
    'CYAN': (0,255,255),
    'BLUE': (50,50,255),
    'MAGENTA': (255,0,255),
    'PINK': (255,150,150),
    'WHITE': (255,255,255),
    'PURPLE': (100,0,255),
    'ORANGE': (255,69,0),
}

BALL_COLORS = [
    COLORS['RED'],
    COLORS['RED'],
    COLORS['YELLOW'],
    COLORS['YELLOW'],
    COLORS['GREEN'],
    COLORS['GREEN'],
    COLORS['GREEN'],
    COLORS['GREEN'],
    COLORS['GREEN'],
    COLORS['GREEN']
]