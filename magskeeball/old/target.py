from .common import *
from .game_parent import GameParent
from . import timer
import time
import random

DOINGHIGHSCORE = True

class Target(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/target.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'TARGET'

    def draw_score(self):  
        self.panel.clear()
        d = 6 if self.show_ball_scores else 0
        self.panel.draw.text((34-d, 31), "%d" % self.balls,font=FONTS['Digital14'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((17-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=COLORS.PURPLE)
        self.panel.draw.text((8-d,31), "BALL" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((8-d,41), "LEFT" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((52-d,31), "TARGET" ,font=FONTS['Medium'],fill=COLORS.YELLOW)
        if self.balls > 0:
            self.panel.draw.text((61-d,41), str(self.bonus[9-self.balls]) ,font=FONTS['Medium'],fill=COLORS.YELLOW)
        if self.got_bonus == 'yes':
            self.panel.draw.text((16-d,53), "BONUS! 1000" ,font=FONTS['Medium'],fill=COLORS.WHITE)
        if self.got_bonus == 'no':
            self.panel.draw.text((27-d,53), "MISSED!" ,font=FONTS['Medium'],fill=COLORS.WHITE)
        #self.panel.draw.text((0,0), str(self.clock.ticks) ,font=FONTS['Tiny'],fill=(255,0,0))
        if self.show_ball_scores:
            for i,(num,b) in enumerate(zip(self.ball_scores,self.ball_bonuses)):
                t=4 if num == '1000' else 0
                color = COLORS.WHITE if b else COLORS.RED
                self.panel.draw.text((84-t,1+6*i),num,font=FONTS['Tiny'],fill=color)
        
        self.panel.update()

    def main_loop(self,settings):

        self.ball_bonuses= []
        self.bonus_time = time.time()
        self.got_bonus = 'idle'
        self.bonus = [100,200,200,300,300,300,400,400,500]
        random.shuffle(self.bonus)

        self.start_prep(settings)

        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)

            if self.got_bonus != 'idle':
                if self.clock.ticks > 2*20:
                    self.got_bonus = 'idle'            

            self.loop_part1() 

            if self.balls == 0:
                continue           

            hit = self.detect_balls()

            if hit:
                self.ball_scores.append(hit)
                self.balls-=1
                self.advance_score = True
                if self.balls in [3,6]:
                    self.sensor.release_balls()
                self.clock.ticks = 0
                if self.ball_scores[-1] == self.bonus[8-self.balls]:
                    self.score_buffer += 1000
                    self.got_bonus = 'yes'
                    self.ball_bonuses.append(True)
                else:
                    self.score_buffer += hit
                    self.got_bonus = 'no'
                    self.ball_bonuses.append(False)


        self.post_game()