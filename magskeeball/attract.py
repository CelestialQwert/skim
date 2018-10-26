from .state import State
from . import resources as res
import random


HISCORE_COLORS = [
    res.COLORS['BLUE'],
    res.COLORS['RED'],
    res.COLORS['YELLOW'],
    res.COLORS['GREEN'],
    res.COLORS['PINK'],
]

class Attract(State):

    def startup(self):
        self.ticks = 0
        self.red_game = self.settings['red_game']
        self.yellow_game = self.settings['yellow_game']
        self.high_scores = self.manager.high_scores

    def handle_event(self,event):
        if event.button == res.B.START and event.down:
            self.manager.next_state = self.red_game
            self.done = True
        elif event.button == res.B.SELECT and event.down:
            self.manager.next_state = self.yellow_game
            self.done = True

    def update(self):
        self.ticks += 1
        if self.ticks % (120*res.FPS) == 13:
            #play jingle once every 2 minutes if idle
            self.attract_song = res.ATTRACT_MUSIC[random.choice(res.ATTRACT_MUSIC_KEYS)]
            self.attract_song.play()
            print("playing song", self.attract_song)

    def draw_panel(self,panel):
        panel.clear()

        if self.ticks % (4*res.FPS) < (1*res.FPS) or not(self.settings['save_high_scores']):
            self.draw_logo(panel)
        else:
            self.draw_high_scores(panel,self.red_game)
            # if self.ticks % (40*res.FPS) < (20*res.FPS):
            #     self.draw_high_scores(panel,self.red_game)
            # else:
            #     self.draw_high_scores(panel,self.red_game)

        if self.ticks % (2*res.FPS) < (1.5*res.FPS):
            panel.draw.text((15,54), "PRESS START",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

    def draw_logo(self,panel):
        panel.paste(res.IMAGES['MainLogo'],(0,5))
        
    def draw_high_scores(self,panel,game):
        title_text = 'HI SCORES - {}'.format(game)
        x = int(48-len(title_text)*2.5)+1
        panel.draw.text((x,2),title_text,font=res.FONTS['Small'],fill=res.COLORS['WHITE'])

        for i,(name,score) in enumerate(self.high_scores[game]):
            if self.high_scores[game][0][1] > 9999:
                panel.draw.text((5+8*i,(i+1)*9),'{} {:5d}'.format(name,score),font=res.FONTS['Medium'],fill=HISCORE_COLORS[i])
            else:
                panel.draw.text((8+8*i,(i+1)*9),'{} {:4d}'.format(name,score),font=res.FONTS['Medium'],fill=HISCORE_COLORS[i])

        # self.panel.draw.text((24,10),'{} {}'.format(name,score),font=FONTS['Medium'],fill=HISCORE_COLORS[0])
        # for i in [1,2,3,4]:
        #     (name,score) = game.high_scores[i]
        #     self.panel.draw.text((28,i*8+12),'{} {}'.format(name,score),font=FONTS['Small'],fill=HISCORE_COLORS[i])

    def cleanup(self):
        self.attract_song.stop()