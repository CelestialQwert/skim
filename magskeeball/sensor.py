from . import resources as res
from .findserial import find_serial_ports
from pkg_resources import resource_filename
import sys
import pygame
import serial
import time
import os

Button = res.Button
B = res.Button

KEYMAP = {
    pygame.K_1: B.B100,
    pygame.K_2: B.B200,
    pygame.K_3: B.B300,
    pygame.K_4: B.B400,
    pygame.K_5: B.B500,
    pygame.K_6: B.B1000R,
    pygame.K_7: B.B1000L,
    pygame.K_0: B.RETURN,
    pygame.K_TAB: B.CONFIG,
    pygame.K_RSHIFT: B.SELECT,
    pygame.K_RETURN: B.START
}

NUM_BUTTONS = len(Button)

ARDUINODOWN = pygame.USEREVENT + 1
ARDUINOUP = pygame.USEREVENT + 2

pygame.init()

class InputEvent:
    def __init__(self, button, down):
        self.button = button
        self.down = down
        self.up = not down

class Sensor:

    def __init__(self,force_keyboard = False):
        self.arduino_buttons = [False]*NUM_BUTTONS
        self.keyboard_buttons = [False]*NUM_BUTTONS
        self.buttons = [0]*NUM_BUTTONS

        self.delay = 20
        self.interval = 3

        try:
            self.init_arduino()
            self.arduino = True
            print('Hello arduino!')
        except:
            print('Setup of Arduino FAILED')
            self.arduino = False

        #keyboard input requires a window to capture key presses
        #so either running on Windows or though SSH
        #When running on actual Skeeball Pi, it's assumed the Arduino will be present
        #But this can be overridden with force_keyboard
        if sys.platform.startswith('win') or ('SSH_CONNECTION' in os.environ) or force_keyboard:
            try:
                self.init_keyboard()
                self.keyboard = True
                print('Hello keyboard!')
            except:
                print('Setup of keyboard FAILED')
                self.keyboard = False
        else:
            print('Keyboard not set up')
            self.keyboard = False

        if not(self.arduino) and not(self.keyboard):
            raise RuntimeError('No sensors are setup properly!')

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

    def init_keyboard(self):
        self.button_panel = pygame.display.set_mode((320,240))
        font = pygame.font.Font(resource_filename('magskeeball','fonts/DroidSans.ttf'),16)
        text = font.render('Click here to capture keyboard presses', True, (255,255,255))
        self.button_panel.blit(text,(5,5))
        pygame.display.update()


    def release_balls(self):
        if self.arduino:
            self.serial.write(bytes('R','ascii'))

    def get_arduino_buttons(self):
        self.serial.write(bytes('B','ascii'))
        arduino_data = self.serial.read(4)
        if arduino_data != None and arduino_data != b'':
            arduino_buttons = int.from_bytes(arduino_data,byteorder='little')
            return [arduino_buttons & 2**i for i in range(NUM_BUTTONS)]
        else:
            return [0]*NUM_BUTTONS

    def update_arduino(self):
        new_arduino = self.get_arduino_buttons()
        if max(new_arduino) > 0:
            print(new_arduino)
        for i,(pressed,held) in enumerate(zip(new_arduino,self.arduino_buttons)):
            if pressed and not held:
                ev = pygame.event.Event(ARDUINODOWN,button=B(i))
                pygame.event.post(ev)
            elif held and not pressed:
                ev = pygame.event.Event(ARDUINOUP,button=B(i))
                pygame.event.post(ev)
        self.arduino_buttons = new_arduino

    def get_events(self):

        #create secondary event queue
        if self.arduino:
            self.update_arduino()
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.KEYDOWN,pygame.KEYUP] and event.key in KEYMAP:
                buttondown = (event.type == pygame.KEYDOWN)
                button = KEYMAP[event.key]
                events.append(InputEvent(button,buttondown))
                self.keyboard_buttons[button.value] = buttondown
            if event.type in [ARDUINODOWN,ARDUINOUP]:
                buttondown = event.type == ARDUINODOWN
                events.append(InputEvent(event.button,buttondown))
                #self.arduino_buttons[event.button] = buttondown

        #combine button lists and track hold time
        bothbuttons = [1 if any(x) else 0 for x in zip(self.keyboard_buttons,self.arduino_buttons)]
        self.buttons = [hold_time+1 if held else 0 for hold_time,held in zip(self.buttons,bothbuttons)]

        if self.delay != 0 and self.interval != 0:
            for i,holdtime in enumerate(self.buttons):
                if holdtime-self.delay >= 0 and (holdtime-self.delay)%self.interval == 0:
                    events.append(InputEvent(B(i),True))

        return events

    def set_repeat(self,delay,interval):
        self.delay = delay
        self.interval = interval
        #reset hold times
        self.buttons = [1 if i else 0 for i in self.buttons]

    def get_repeat(self):
        return (self.delay,self.interval)

def main():
    clock = pygame.time.Clock()
    i=0
    sensor = Sensor()
    while True:
        for event in sensor.get_events():
            if event.down:
                print("Button pressed!",event.button)
        if not(i%10):
            print(sensor.buttons)
        i += 1
        clock.tick(20)
