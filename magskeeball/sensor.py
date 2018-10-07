from .common import *
from .findserial import find_serial_ports
from pkg_resources import resource_filename
import sys
import pygame
import struct
import platform
import serial

ARDUINO = 0
EMULATED = 1
BOTH = 2

#pygame.init()


class Sensor():

    def __init__(self,which_sensor=EMULATED):
        self.buttons = 0
        self.buttons_held = 0
        self.hold_time = 0*[16]

        try:
            self.init_arduino()
            self.arduino = True
            print('Hello arduino!')
        except:
            print('Setup of Arduino FAILED')
            self.arduino = False


        if platform.system() == 'Windows':
            self.init_emulated_sensor()
            self.emulated_sensors = True
            print('Hello emulated sensors!')
        else:
            self.emulated_sensors = False

        if not(self.arduino) and not(self.emulated_sensors):
            raise RuntimeError('No sensors are setup properly!')

    def old_init(self,which_sensor=EMULATED):
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
        ports = find_serial_ports()
        if len(ports) > 1:
            print('Found mroe than one port...')
        port = ports[0]
        print("Using port {}".format(port))

        self.serial = serial.Serial(
            port=port,
            baudrate=9600,
            timeout=.1
        )

    def init_emulated_sensor(self):
        pygame.init()
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
        font = pygame.font.Font(resource_filename('magskeeball','fonts/DroidSans.ttf'),16)
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
            buttons = self.serial.read(4)
            if buttons != None and buttons != b'':
                ard_buttons = int.from_bytes(buttons,byteorder='little')
            held_buttons = self.serial.read(4)
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
            print('{0:04x}'.format(self.buttons),'{0:04x}'.format(self.buttons_held))
