import sys
import pygame
import PIL
from . import panel 
from .common import *

pygame.init()

class Manager():

    def __init__(self):

        self.done = False
        self.panel = panel.Panel()
        self.clock = pygame.time.Clock()
        self.fps = 20

        self.states = {
            "INTRO": Intro(),
            "DUMMYGAME": DummyGame()
        }

        self.state_name = 'INTRO'
        self.state = self.states[self.state_name]
        self.last_state = None

    def handle_events(self):
        for event in pygame.event.get():
            self.state.handle_event(event)

    def flip_state(self):            
        #shutdown old state
        persist = self.state.cleanup()
        self.state.done = False
        #switch to new state
        self.last_state = self.state_name
        self.state_name = self.state.next_state
        self.state = self.states[self.state_name]
        #startup new state
        self.state.startup(persist)

    def update(self,dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw_panel(self):
        self.state.draw_panel(self.panel)
        self.panel.update()

    def main_loop(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.handle_events()
            self.update(dt)
            self.draw_panel()
        pygame.quit()

class State():

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}

    def startup(self,persist):
        self.persist = persist

    def handle_event(self,event):
        if event.type == pygame.QUIT:
            self.quit = True

    def update(self,dt):
        pass

    def draw_panel(self):
        pass

    def cleanup(self):
        return self.persist

class Intro(State):

    def __init__(self):
        super(Intro,self).__init__()
        self.persist["screen_color"] = "black"
        self.next_state = "DUMMYGAME"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            self.persist["screen_color"] = COLORS['YELLOW']
            self.done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.persist["screen_color"] = COLORS['CYAN']
            self.done = True

    def draw_panel(self, panel):
        panel.clear()
        panel.draw.text((16,16), "Intro WOOO",font=FONTS['Medium'],fill=COLORS['RED'])


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
        if self.screen_color == COLORS['CYAN']:
            self.text = "Mouseclick"
        elif self.screen_color == COLORS['YELLOW']:
            self.text = "Keypress"
        
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


if __name__ == "__main__":
    
    game = Manager()
    game.main_loop()