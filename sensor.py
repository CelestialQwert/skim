from common import *
import sys
import pygame
import struct
import platform

ARDUINO = 0
EMULATED = 1
BOTH = 2

#pygame.init()

class Sensor():

    def __init__(self,which_sensor=EMULATED):
        self.buttons = 0
        self.buttons_held = 0
        self.hold_time = 0*[16]
        if which_sensor not in [ARDUINO,EMULATED,BOTH]:
                raise ValueError('Argument must be sensor.ARDUINO (0), sensor.EMULATED (1), or sensor.BOTH (2)')

        if which_sensor != EMULATED:
            self.arduino = True
            self.init_arduino()
        else:
            self.arduino = False

        if which_sensor != ARDUINO:
            self.emulated_sensors = True
            self.init_emulated_sensor()
        else:
            self.emulated_sensors = False

    def init_arduino(self):
        import serial
        if platform.system() == 'Windows':
            port = 'COM3'
        else:
            port = '/dev/ttyACM0'
        print('Hello arduino!')
        self.serial = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=.1,
            rtscts=False,
            dsrdtr=False
        )

    def init_emulated_sensor(self):
        pygame.init()
        print("Hello emulated sensors!")
        self.EMUBUTTON = {
            pygame.K_1: 'B100',
            pygame.K_2: 'B200',
            pygame.K_3: 'B300',
            pygame.K_4: 'B400',
            pygame.K_5: 'B500',
            pygame.K_6: 'B1000L',
            pygame.K_7: 'B1000R',
            pygame.K_0: 'BRET',
            pygame.K_RSHIFT: 'SELECT',
            pygame.K_RETURN: 'START',
            pygame.K_TAB: 'CONFIG'
        }
        self.button_panel = pygame.display.set_mode((320,240))
        font = pygame.font.Font('fonts/DroidSans.ttf',16)
        text = font.render('Click here to capture keyboard presses', True, (255,255,255))
        self.button_panel.blit(text,(5,5))
        pygame.display.update()


    def release_balls(self):
        if self.arduino:
            self.serial.write(b"R\n")

    def is_pressed(self,button):
        return self.buttons & button
        #bitwise and

    def update_buttons(self):
        ard_buttons = 0
        ard_buttons_held = 0
        if self.arduino:
            self.serial.write(bytes('B','ascii'))
            buttons = self.serial.read(2)
            if buttons != None and buttons != b'':
                ard_buttons = int.from_bytes(buttons,byteorder='little')
            held_buttons = self.serial.read(2)
            if held_buttons != None and held_buttons != b'':
                ard_buttons_held = int.from_bytes(held_buttons,byteorder='little')

        emu_buttons = 0
        emu_buttons_held = 0
        if self.emulated_sensors:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key in self.EMUBUTTON.keys():
                    button = self.EMUBUTTON[event.key]
                    emu_buttons += BUTTON[button]
            keys_pressed = pygame.key.get_pressed()
            for key in self.EMUBUTTON:
                if keys_pressed[key]:
                    button = self.EMUBUTTON[key]
                    emu_buttons_held += BUTTON[button]

        #bitwise or on both sets of buttons
        self.buttons = ard_buttons | emu_buttons
        self.buttons_held = ard_buttons_held | emu_buttons_held

        if self.buttons != 0 or self.buttons_held != 0:
            print(self.buttons,self.buttons_held)
