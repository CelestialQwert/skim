from common import *
import time
from game_parent import GameParent
import random
import timer


class Combo(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/combo.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'COMBO'


    def draw_score(self):  
        self.panel.clear()
        d = 6 if self.show_ball_scores else 0
        score_x = 17 if self.score < 10000 else 4#1
        self.panel.draw.text((score_x-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=(100,0,255))
        self.panel.draw.text((31-d, 31), "%d" % self.balls,font=FONTS['Digital14'],fill=(0,255,50))
        self.panel.draw.text((5-d,31), "BALL" ,font=FONTS['Medium'],fill=(0,255,50))
        self.panel.draw.text((5-d,41), "LEFT" ,font=FONTS['Medium'],fill=(0,255,50))
        self.panel.draw.text((48-d,31), "CHAIN" ,font=FONTS['Medium'],fill=(255,255,0))

        if self.ball_scores[-1] == '0':
            self.combo = 0
        ballscore_x = 63-3*len(self.ball_scores[-1])
        self.panel.draw.text((80-d,31), str(self.combo) ,font=FONTS['Digital14'],fill=(255,255,0))
        self.panel.draw.text((ballscore_x-d,41),self.ball_scores[-1] ,font=FONTS['Medium'],fill=(255,255,0))
        if self.just_scored:
            text = '{} x {}'.format(self.ball_scores[-1],self.combo)
            self.panel.draw.text((27-d,53), text ,font=FONTS['Medium'],fill=(255,255,255))


        
        self.panel.update()

    def main_loop(self,settings):
        self.score = 0
        self.score_buffer = 0
        self.balls = 9
        self.ball_scores = ['0']
        self.combo = 1
        self.show_ball_scores = False
        self.advance_score = False
        self.bonus_time = time.time()
        self.just_scored = False
        self.bonus = ['B100','B200','B200','B300','B300','B300','B400','B400','B500']
        random.shuffle(self.bonus)

        self.sensor.release_balls()

        #self.draw_score()

        self.clock = timer.Timer()
        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)

            self.sensor.update_buttons()

            if self.advance_score:
                if self.score_buffer > 0:
                    self.score += 100
                    self.score_buffer -= 100
                else:
                    self.advance_score = False

            if self.clock.ticks > settings['timeout']*20 or self.sensor.is_pressed(BUTTON['CONFIG']):
                self.balls = 0

            self.draw_score()

            if self.just_scored and self.clock.ticks > 2*20:
                    self.just_scored = False

            if self.balls == 0:
                continue

            if self.sensor.is_pressed(BUTTON['B1000L']) or self.sensor.is_pressed(BUTTON['B1000R']):
                self.ball_scores.append('1000')
            if self.sensor.is_pressed(BUTTON['B500']):
                self.ball_scores.append('500')
            if self.sensor.is_pressed(BUTTON['B400']):
                self.ball_scores.append('400')
            if self.sensor.is_pressed(BUTTON['B300']):
                self.ball_scores.append('300')
            if self.sensor.is_pressed(BUTTON['B200']):
                self.ball_scores.append('200')
            if self.sensor.is_pressed(BUTTON['B100']):
                self.ball_scores.append('100')

            if self.sensor.is_pressed(BUTTON['SCORED']):
                self.just_scored = True
                self.balls-=1
                if self.ball_scores[-1] == self.ball_scores[-2]:
                    self.combo += 1
                    self.combo = min(self.combo, int(self.ball_scores[-1])//100, 5)
                else:
                    self.combo = 1
                self.score_buffer += self.combo * int(self.ball_scores[-1])
                self.advance_score = True
                if self.balls in [3,6]:
                    self.sensor.release_balls()
                self.clock.ticks = 0

            if self.sensor.is_pressed(BUTTON['SELECT']):
                self.sensor.release_balls()


        time.sleep(1)

        if settings['do_hi_scores']:
            self.check_high_score()


        self.panel.clear()
        self.panel.draw.text((8, 27), "GAME",font=FONTS['GameOver'],fill=(255,0,0))
        self.panel.draw.text((14, 41), "OVER",font=FONTS['GameOver'],fill=(255,0,0))
        score_x = 17 if self.score < 10000 else 4#1
        self.panel.draw.text((score_x, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=(255,200,10))
        self.panel.update()
        
        self.clock.ticks = 0
        wait_ticks = 100 if settings['do_hi_scores'] else 200
        while self.clock.ticks < wait_ticks:
            self.clock.tick(20)
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['ANYBUTTON']):
                self.clock.ticks = wait_ticks