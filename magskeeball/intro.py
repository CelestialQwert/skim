from .state import State
from . import resources as res
import random

class Intro(State):

    #def __init__(self,manager):
    #    super(Dummy,self).__init__(manager)

    def startup(self):
        self.mode_name = self.persist['active_game_mode']
        self.manager.next_state = self.mode_name
        self.mode = self.manager.states[self.mode_name]
        self.intro_text = self.mode.intro_text
        self.ticks = 0
        if self.mode_name == 'TARGET':
            self.start_song = res.GAME_MUSIC['TARGET_INTRO']
        else:
            self.start_song = res.START_MUSIC[random.choice(res.START_MUSIC_KEYS)]
        self.start_song.play()


    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button in [res.B.START,res.B.SELECT] and event.down:
            self.done = True

    def update(self):
        self.ticks += 1
        if self.ticks > 10*res.FPS:
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        for i,line in enumerate(self.intro_text):
            panel.draw.text((1,1), '{} MODE'.format(self.mode_name), font=res.FONTS['Small'], fill=res.COLORS['WHITE'])
            panel.draw.text((1,12+8*i), line, font=res.FONTS['Small'], fill=res.COLORS['WHITE'])
        
