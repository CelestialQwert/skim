from .state import State,GameMode
from . import resources as res
import random

class GameMenu(GameMode):

    #def __init__(self,manager):
    #    super(Dummy,self).__init__(manager)

    def startup(self):
        self.game_modes = self.manager.game_modes
        for bangame in ['DUMMY','GAMEMENU']:
            if bangame in self.game_modes:
                self.game_modes.remove(bangame)
        self.game_position = len(self.game_modes)-1
        self.next_game()
        self.ticks = 0
        self.locked = False
        self.lock_time = 9999999

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if not self.locked:
            if event.button == res.B.SELECT and event.down:
                self.next_game()
            if event.button == res.B.START and event.down:
                self.manager.next_state = self.mode_name
                self.persist['active_game_mode'] = self.mode_name
                self.locked = True
                self.lock_time = self.ticks
                if self.mode_name == 'TARGET':
                    self.start_song = res.TARGET_SFX['TARGET_INTRO']
                else:
                    self.start_song = res.START_MUSIC[random.choice(res.START_MUSIC_KEYS)]
                self.start_song.play()
        else:
            if event.button in [res.B.START,res.B.SELECT] and event.down:
                self.done = True


    def update(self):
        self.ticks += 1
        if self.ticks > self.lock_time + 3*res.FPS:
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        title = '{} MODE'.format(self.mode_name)
        x = 48 - 3*len(title)
        panel.draw.text((x,1), title, font=res.FONTS['Medium'], fill=res.COLORS['PURPLE'])
        for i,line in enumerate(self.intro_text):
            panel.draw.text((1,13+8*i), line, font=res.FONTS['Small'], fill=res.COLORS['YELLOW'])
        if not self.locked:
            panel.draw.text((20,49), "SELECT MODE" ,font=res.FONTS['Small'],fill=res.COLORS['WHITE'])
            if self.ticks % (3*res.FPS) < 1.5*res.FPS:
                panel.draw.text((10,56), "YELLOW = CHANGE" ,font=res.FONTS['Small'],fill=res.COLORS['WHITE'])
            else:
                panel.draw.text((20,56), "RED = START" ,font=res.FONTS['Small'],fill=res.COLORS['WHITE'])

    def next_game(self):
            self.game_position = (self.game_position + 1) % len(self.game_modes)
            self.mode_name = self.game_modes[self.game_position]
            self.mode = self.manager.states[self.mode_name]
            self.intro_text = self.mode.intro_text
            print('Switching to mode {} {}'.format(self.game_position,self.mode_name))

        
