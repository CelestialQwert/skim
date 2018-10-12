from .common import *
from PIL import Image, ImageFont, ImageDraw
import sys
import pygame
import platform
import time

REAL = 0
EMULATED = 1
BOTH = 2

pygame.init()

class Panel():

    def __init__(self,scale=6):

        if platform.system() != 'Windows':
            self.init_real_panel()
            self.buffer_canvas = Image.new('RGBA',(192,32))
            self.real_panel = True
            self.emulated_panel = False
            print('Hello LED panel!')
        else:
            self.init_emulated_panel(scale)
            self.real_panel = False
            self.emulated_panel = True
            print("Hello emulated panel!")

        self.canvas = Image.new('RGBA',(96,64))
        self.draw = ImageDraw.Draw(self.canvas)
        self.paste = self.canvas.paste

    def old_init(self,which_panel=REAL,scale=6):
        #if Windows is detected, force emulated panel only
        if platform.system() == 'Windows':
            which_panel = EMULATED
        if which_panel not in [REAL,EMULATED,BOTH]:
                raise ValueError('Argument must be panel.REAL (0), panel.EMULATED (1), or panel.BOTH (2)')
        if which_panel != REAL:
            self.emulated_panel = True
            self.init_emulated_panel(scale)
        else:
            self.emulated_panel = False
        
        if which_panel != EMULATED:
            self.real_panel = True
            self.init_real_panel()
        else:
            self.real_panel = False

        self.buffer_canvas = Image.new('RGBA',(192,32))
        self.canvas = Image.new('RGBA',(96,64))
        self.draw = ImageDraw.Draw(self.canvas)
        self.paste = self.canvas.paste

    def init_real_panel(self):
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.chain_length = 6
        self.options.parallel = 1
        self.options.brightness = 50
        #self.options.show_refresh_rate = 1
        self.options.pwm_bits = 11
        self.gpio_slowdown = 2
        self.options.pwm_lsb_nanoseconds = 130
        #self.options.disable_hardware_pulsing = True
        self.options.hardware_mapping = 'adafruit-hat-pwm'
        self.no_drop_privs = True
        self.matrix = RGBMatrix(options = self.options)
        #print('real panel loaded, waiting 5 seconds to drop root...')
        #time.sleep(5)

    def init_emulated_panel(self,scale):
        self.e_size = tuple([x*scale for x in (96,64)])
        self.emu_panel = pygame.display.set_mode(self.e_size)


    def update(self):
        if self.real_panel:
            top = self.canvas.crop((0,0,96,32))
            bottom = self.canvas.crop((0,32,96,64))
            self.buffer_canvas.paste(top,(0,0))
            self.buffer_canvas.paste(bottom,(96,0))
            self.matrix.SetImage(self.buffer_canvas.convert('RGB'))
        if self.emulated_panel:
            data = self.canvas.resize(self.e_size).tobytes()
            mode = self.canvas.mode
            pyg_canvas = pygame.image.fromstring(data,self.e_size,mode)
            self.emu_panel.fill((0,0,0))
            self.emu_panel.blit(pyg_canvas,(0,0))
            pygame.display.update()

    def paste(self,image,coords):
        self.canvas.paste(image,coords)

    def clear(self):
        self.draw.rectangle((0,0,96,64),fill=(0,0,0))

    def fill(self,color):
        self.draw.rectangle((0,0,96,64),fill=color)