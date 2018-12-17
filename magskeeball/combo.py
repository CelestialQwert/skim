from .basic_skeeball import BasicSkeeball
from . import resources as res
import random
import colorsys

COMBO_COLORS = [
    res.COLORS['WHITE'],
    res.COLORS['BLUE'],
    res.COLORS['GREEN'],
    res.COLORS['ORANGE'],
    res.COLORS['MAGENTA'],
]

class Combo(BasicSkeeball):

    intro_text = [
        "HIT THE SAME TARGET",
        "TO BUILD A COMBO",
        "AND GET MASSIVE",
        "POINTS!"
    ]

    def startup(self):
        super(Combo,self).startup()
        print("Special Mode: Combo")
        self.persist['active_game_mode'] = 'COMBO'
        self.combo = 0
        self.ball_scores = ['0']
        self.just_scored = False


    def update(self):
        super(Combo,self).update()
        if self.advance_score and self.score == 9100:
            res.SOUNDS['OVER9000'].play()
        if self.just_scored and (self.ticks - self.ticks_last_ball) >= 2*res.FPS:
                self.just_scored = False
            

    def add_score(self,score):
        self.ball_scores.append(score)
        self.balls-=1
        self.just_scored = True
        if self.ball_scores[-1] == self.ball_scores[-2]:
            self.combo += 1
            self.combo = min(self.combo, self.ball_scores[-1]//100, 5)
        else:
            self.combo = 1
        if self.ball_scores[-1] == 0:
            self.combo = 0
            self.just_scored = False
        self.score_buffer += self.combo * self.ball_scores[-1]
        self.advance_score = True
        #if self.balls in [3,6]:
        #    self.sensor.release_balls()
        self.ticks_last_ball = self.ticks

    def draw_panel(self,panel):  
        panel.clear()
        d = 6 if self.debug else 0
        score_x = 17 if self.score < 10000 else 4#1
        panel.draw.text((score_x, 4), "%04d" % self.score ,font=res.FONTS['Digital16'],fill=res.COLORS['PURPLE'])
        panel.draw.text((31, 31), "%d" % self.balls,font=res.FONTS['Digital14'],fill=res.BALL_COLORS[self.balls])
        panel.draw.text((5,31), "BALL" ,font=res.FONTS['Medium'],fill=res.BALL_COLORS[self.balls])
        panel.draw.text((5,41), "LEFT" ,font=res.FONTS['Medium'],fill=res.BALL_COLORS[self.balls])

        if self.combo == 5:
            colour = tuple(int(255*i) for i in colorsys.hsv_to_rgb((self.ticks*18)%360/360,1,1))
        else:
            colour = COMBO_COLORS[self.combo]
        #if self.ball_scores[-1] == '0':
        #    self.combo = 0
        ballscore_x = 63-3*len(str(self.ball_scores[-1]))
        panel.draw.text((80,31), str(self.combo) ,font=res.FONTS['Digital14'],fill=colour)
        panel.draw.text((ballscore_x,41),str(self.ball_scores[-1]) ,font=res.FONTS['Medium'],fill=colour)
        panel.draw.text((48,31), "CHAIN" ,font=res.FONTS['Medium'],fill=colour)


        if self.just_scored:
            text = '{} x {}'.format(self.ball_scores[-1],self.combo)
            panel.draw.text((27,53), text ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

        if self.debug:
            for i,num in enumerate(self.ball_scores):
                num = str(num)
                t = 4*len(num)
                panel.draw.text((96-t,1+6*i),num,font=res.FONTS['Tiny'],fill=res.COLORS['RED'])
            panel.draw.text((90,57), "%d" % self.returned_balls,font=res.FONTS['Small'],fill=res.COLORS['ORANGE'])


