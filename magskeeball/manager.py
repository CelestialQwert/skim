import sys
import pygame

from . import panel
from . import sensor
from . import resources as res

from .attract import Attract
from .settings import Settings
from .intro import Intro
from .high_scores import HighScore
from .gameover import GameOver
from .basic_skeeball import BasicSkeeball
from .target import Target
from .combo import Combo
from .speed import Speed
from .dummy import Dummy

print('init pygame')
pygame.init()
print('done init pygame')

class Manager():

    def __init__(self,states=None,starting_state=None):

        self.settings = {}
        self.persist = {}

        if states == None:
            self.states = {
                "ATTRACT": Attract(manager=self),
                "SETTINGS": Settings(manager=self),
                "INTRO": Intro(manager=self),
                "HIGHSCORE": HighScore(manager=self),
                "GAMEOVER": GameOver(manager=self),
                "BASIC": BasicSkeeball(manager=self),
                "TARGET": Target(manager=self),
                "COMBO": Combo(manager=self),
                "SPEED": Speed(manager=self),
                "DUMMY": Dummy(manager=self),
            }
            self.game_modes = ['BASIC','TARGET','COMBO','SPEED','DUMMY']

            self.has_high_scores = {}
            for game_mode in self.game_modes:
                self.has_high_scores[game_mode] = self.states[game_mode].has_high_scores
        else:
            self.states = {}
            for state in states:
                self.states[state] = states[state](manager=self)
        #starting state
        self.state_name = starting_state if starting_state != None else 'ATTRACT'

        self.done = False
        self.sensor = sensor.Sensor()
        self.panel = panel.Panel()
        self.clock = pygame.time.Clock()
        self.state = self.states[self.state_name]

        self.settings['red_game'] = 'BASIC'
        self.settings['yellow_game'] = 'DUMMY'
        self.settings['timeout'] = 60
        self.settings['save_high_scores'] = True
        self.settings['debug'] = False

        self.persist['last_color'] = 'none'

        self.last_state = ''
        self.next_state = ''

        self.high_scores = self.states['HIGHSCORE'].load_all_high_scores()
        #lol mutable
        temp_settings = self.states['SETTINGS'].load_settings()
        for key,value in temp_settings.items():
            self.settings[key] = value

    def handle_events(self):
        for event in self.sensor.get_events():
            self.state.handle_event(event)

    def update(self):
        self.state.update()

    def draw_panel(self):
        self.state.draw_panel(self.panel)
        self.panel.update()

    def flip_state(self):            
        #shutdown old state
        self.state.cleanup()
        self.state.done = False
        #clear events to prevent buffering
        self.sensor.get_events()
        #switch to new state
        self.last_state = self.state_name
        self.state_name = self.next_state
        self.next_state = ''
        self.state = self.states[self.state_name]
        #startup new state
        self.state.startup()

    def main_loop(self):
        self.state.startup()
        while not self.done:
            self.clock.tick(res.FPS)
            self.handle_events()
            self.update()
            self.draw_panel()
            if self.state.quit:
                self.done = True
            elif self.state.done:
                self.flip_state()
        self.state.cleanup()
        pygame.quit()



def test():
    from . import test_states

    states = {
            "INTRO": test_states.Intro,
            "DUMMYGAME": test_states.DummyGame
        }
    starting_state = 'INTRO'
    
    game = Manager(states,starting_state)
    game.main_loop()

if __name__ == "__main__":
    test()
