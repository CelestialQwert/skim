import sys
import pygame
import time
import json

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
from .speedrun import Speedrun
from .timed import Timed
from .dummy import Dummy
from .game_menu import GameMenu

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
                "SPEEDRUN": Speedrun(manager=self),
                "TIMED": Timed(manager=self),
                "DUMMY": Dummy(manager=self),
                "GAMEMENU": GameMenu(manager=self),
            }
            self.game_modes = ['BASIC','TARGET','COMBO','SPEEDRUN','TIMED']
            self.selectable_modes = self.game_modes + ['DUMMY','GAMEMENU']

            self.has_high_scores = {}
            for game_mode in self.selectable_modes:
                self.has_high_scores[game_mode] = self.states[game_mode].has_high_scores
            self.has_high_scores['SETTINGS'] = False

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

        self.persist['hs_game_hist'] = ['BASIC']
        self.persist['active_game_mode'] = 'DUMMY'

        self.last_state = ''
        self.next_state = ''

        try:
            with open('high_scores/game_log.txt','r') as game_log_file:
                self.game_log = json.loads(game_log_file.read())
        except:
            print('loading game log failed, remaking')
            self.game_log = {}
            for game in self.game_modes:
                self.game_log[game] = 0
            with open('high_scores/game_log.txt','w') as game_log_file:
                game_log_file.write(json.dumps(self.game_log))

        self.high_scores = self.states['HIGHSCORE'].load_all_high_scores()
        #lol mutable
        temp_settings = self.states['SETTINGS'].load_settings()
        for key,value in temp_settings.items():
            self.settings[key] = value

        self.global_ticks = 0
        self.sensor.set_repeat(0,0)

    def handle_events(self):
        for event in self.sensor.get_events():
            if isinstance(event,sensor.InputEvent):
                print('Tick {}, Handling InputEvent, button = {}, down = {}'.format(self.global_ticks,event.button,event.down))
            else:
                print('Tick {},Handling event'.format(self.global_ticks),type(event))
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
        print('Ending old state',self.state_name)
        #clear events to prevent buffering
        #sleep prevents weird bug where an extra buttonup and buttondown event are generated
        time.sleep(1/res.FPS)
        self.sensor.get_events()
        time.sleep(1/res.FPS)
        #switch to new state
        self.last_state = self.state_name
        self.state_name = self.next_state
        if self.state_name in self.game_modes:
            self.game_log[self.state_name] += 1
            with open('high_scores/game_log.txt','w') as game_log_file:
                game_log_file.write(json.dumps(self.game_log))

        self.next_state = ''
        self.state = self.states[self.state_name]
        #startup new state
        print('Starting new state',self.state_name)
        self.state.startup()

    def main_loop(self):
        self.state.startup()
        while not self.done:
            self.global_ticks += 1
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
