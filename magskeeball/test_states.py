from .manager import State
from .common import *
import pygame

class Intro(State):

    def __init__(self):
        super(Intro,self).__init__()
        self.persist["screen_color"] = "black"
        self.next_state = "DUMMYGAME"

    def handle_event(self, event):
        print("Button: {}, Up: {}, Down: {}".format(event.button, event.up, event.down))
        if event.button == B.QUIT:
            self.quit = True
        elif event.up and event.button == Button.START:
            self.persist["screen_color"] = COLORS['RED']
            self.done = True
        elif event.up and event.button == B.SELECT:
            self.persist["screen_color"] = COLORS['YELLOW']
            self.done = True
        elif event.up:
            print('lol')
        print(self.persist)

    def draw_panel(self, panel):
        panel.clear()
        panel.draw.text((16,16), "Intro WOOO",font=FONTS['Medium'],fill=COLORS['GREEN'])


class DummyGame(State):
    def __init__(self):
        super(DummyGame, self).__init__()
        self.rect_loc = (0, 0)
        self.rect_size = (16, 16)
        self.rect_x_velocity = 1
        self.text_loc = (10,10)
        
    def startup(self, persist):
        self.persist = persist
        self.screen_color = self.persist["screen_color"]
        if self.screen_color == COLORS['RED']:
            self.text = "Start Press"
        elif self.screen_color == COLORS['YELLOW']:
            self.text = "Select Press"
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.text_loc = tuple(x // 6 for x in event.pos)
        
    def update(self,dt):
        veloc = (self.rect_x_velocity,0)
        self.rect_loc  = tuple(map(sum, zip(self.rect_loc,veloc)))
        if self.rect_loc[0] > 79 or self.rect_loc[0] < 1:
            self.rect_x_velocity *= -1
                 
    def draw_panel(self, panel):
        panel.fill(self.screen_color)
        panel.draw.rectangle(self.rect_loc+self.rect_size,fill=COLORS['BLACK'])
        panel.draw.text(self.text_loc,self.text,font=FONTS['Medium'],fill=(25,25,25))