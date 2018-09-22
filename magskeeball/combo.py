from common import *
import time
from game_parent import GameParent
import random
import timer
import colorsys

COMBO_COLORS = [
    COLORS.WHITE,
    COLORS.BLUE,
    COLORS.GREEN,
    COLORS.ORANGE,
    COLORS.MAGENTA,
]

class Combo(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/combo.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'COMBO'


    def draw_score(self):  
        self.panel.clear()
        d = 6 if self.show_ball_scores else 0
        score_x = 17 if self.score < 10000 else 4#1
        self.panel.draw.text((score_x-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=COLORS.PURPLE)
        self.panel.draw.text((31-d, 31), "%d" % self.balls,font=FONTS['Digital14'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((5-d,31), "BALL" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((5-d,41), "LEFT" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])

        if self.combo == 5:
            colour = tuple(int(255*i) for i in colorsys.hsv_to_rgb((self.clock.ticks*18)%360/360,1,1))
        else:
            colour = COMBO_COLORS[self.combo]
        #if self.ball_scores[-1] == '0':
        #    self.combo = 0
        ballscore_x = 63-3*len(str(self.ball_scores[-1]))
        self.panel.draw.text((80-d,31), str(self.combo) ,font=FONTS['Digital14'],fill=colour)
        self.panel.draw.text((ballscore_x-d,41),str(self.ball_scores[-1]) ,font=FONTS['Medium'],fill=colour)
        self.panel.draw.text((48-d,31), "CHAIN" ,font=FONTS['Medium'],fill=colour)

        if self.just_scored:
            text = '{} x {}'.format(self.ball_scores[-1],self.combo)
            self.panel.draw.text((27-d,53), text ,font=FONTS['Medium'],fill=COLORS.WHITE)

        self.panel.update()

    def main_loop(self,settings):
        self.combo = 0
        self.bonus_time = time.time()
        self.just_scored = False

        self.settings = settings
        self.score = 0
        self.score_buffer = 0
        self.balls = 9
        self.ball_scores = ['0']
        self.show_ball_scores = False
        self.advance_score = False

        self.sensor.release_balls()

        self.draw_score()
        SOUNDS['START'].play()

        self.clock = timer.Timer()

        self.clock = timer.Timer()
        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)

            self.loop_part1()

            if self.advance_score and self.score == 9100:
                SOUNDS['OVER9000'].play()

            if self.just_scored and self.clock.ticks > 2*20:
                    self.just_scored = False

            if self.balls == 0:
                continue

            hit = self.detect_balls()

            if hit:
                self.just_scored = True
                self.ball_scores.append(hit)
                self.balls-=1
                self.advance_score = True
                if self.balls in [3,6]:
                    self.sensor.release_balls()
                self.clock.ticks = 0
                if self.ball_scores[-1] == self.ball_scores[-2]:
                    self.combo += 1
                    self.combo = min(self.combo, int(self.ball_scores[-1])//100, 5)
                else:
                    self.combo = 1
                self.score_buffer += self.combo * int(self.ball_scores[-1])

        self.post_game()