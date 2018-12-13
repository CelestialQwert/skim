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
            self.start_song = res.TARGET_SFX['TARGET_INTRO']
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
        title = '{} MODE'.format(self.mode_name)
        x = 48 - 3*len(title)
        panel.draw.text((x,1), title, font=res.FONTS['Medium'], fill=res.COLORS['PURPLE'])
        for i,line in enumerate(self.intro_text):
            panel.draw.text((1,15+8*i), line, font=res.FONTS['Small'], fill=res.COLORS['YELLOW'])
            if self.ticks > (3*res.FPS):
                panel.draw.text((15,48), "PRESS START",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

        
