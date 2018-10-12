import sys
import pygame
from . import panel
from . import sensor
from .common import *

print('init pygame')
pygame.init()
print('done init pygame')

class Manager():

    def __init__(self,states,starting_state):

        self.done = False
        self.sensor = sensor.Sensor()
        self.panel = panel.Panel()
        self.clock = pygame.time.Clock()
        self.fps = 20
        self.states = states
        self.state_name = starting_state
        self.state = self.states[self.state_name]
        self.last_state = ''

    def handle_events(self):
        for event in self.sensor.get_events():
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
        persist = {}
        self.state.startup(persist)
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.handle_events()
            self.update(dt)
            self.draw_panel()
        self.state.cleanup()
        pygame.quit()

class State():

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        #self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}

    def startup(self,persist):
        self.persist = persist

    def handle_event(self,event):
        if event.button == Button.QUIT:
            self.quit = True

    def update(self,dt):
        pass

    def draw_panel(self,panel):
        pass

    def cleanup(self):
        return self.persist

def test():
    from . import test_states

    states = {
            "INTRO": test_states.Intro(),
            "DUMMYGAME": test_states.DummyGame()
        }
    starting_state = 'INTRO'
    
    game = Manager(states,starting_state)
    game.main_loop()

if __name__ == "__main__":
    test()
