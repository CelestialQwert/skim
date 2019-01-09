from .speedrun import Speedrun
from . import resources as res
import random
import time

class Speed10k(Speedrun):

    intro_text = [
        "HOW FAST CAN YOU",
        "SCORE 10000 POINTS?",
    ]

    def startup(self):
        super(Speed10k,self).startup()
        self.score = 10000
        self.persist['active_game_mode'] = 'SPEED10K'

    def draw_panel(self,panel):
        panel.clear()
        if self.time_elapsed < 0:
            display_time = 0
        else:
            display_time = self.time_elapsed

        minutes = display_time // (60 * res.FPS)
        seconds = (display_time // res.FPS) % 60
        fraction = round( 100.0 / res.FPS * (display_time % res.FPS))

        panel.draw.text((7, 6), "%01d" % minutes, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
        panel.draw.text((28, 6), "%02d" % seconds, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
        panel.draw.text((63, 6), "%02d" % fraction, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
        panel.draw.rectangle([21, 18, 24, 21],fill=res.COLORS['PURPLE'])
        panel.draw.rectangle([21, 9, 24, 12],fill=res.COLORS['PURPLE'])
        panel.draw.rectangle([56, 21, 59, 24],fill=res.COLORS['PURPLE'])
        panel.draw.text((57,31), "BALLS" ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((66, 41), "%02d" % self.balls,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

        if self.score <= 1000:
            score_color = res.COLORS['RED']
        elif self.score <= 2500:
            score_color = res.COLORS['YELLOW']
        else:
            score_color = res.COLORS['GREEN']

        panel.draw.text((9,31), "SCORE",font=res.FONTS['Medium'],fill=score_color)
        score = self.score if self.score > 0 else 0
        panel.draw.text((9, 41), "%05d" % score,font=res.FONTS['Medium'],fill=score_color)

            

        if self.time_elapsed < 0:
            display_time = self.time_elapsed
            seconds = (-display_time // res.FPS) % 60 + 1
            panel.draw.text((15,54), "READY... {:1}".format(seconds),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        elif self.time_elapsed < 2*res.FPS:
            panel.draw.text((39,54), "GO!",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

        if self.debug:
            for i,num in enumerate(self.ball_scores[-9:]):
                num = str(num)
                t = 4*len(num)
                panel.draw.text((96-t,1+6*i),num,font=res.FONTS['Tiny'],fill=res.COLORS['RED'])
            panel.draw.text((85,57), "{:02}".format(self.returned_balls),font=res.FONTS['Small'],fill=res.COLORS['ORANGE'])
