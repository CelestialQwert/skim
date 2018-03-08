from common import *
import time
from game_parent import GameParent
import random
import timer

DOINGHIGHSCORE = True

class Target(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/target.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'TARGET'

    def draw_score(self):  
        self.panel.clear()
        d = 6 if self.show_ball_scores else 0
        self.panel.draw.text((34-d, 31), "%d" % self.balls,font=FONTS['Digital14'],fill=(0,255,50))
        self.panel.draw.text((17-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=(100,0,255))
        self.panel.draw.text((8-d,31), "BALL" ,font=FONTS['Medium'],fill=(0,255,50))
        self.panel.draw.text((8-d,41), "LEFT" ,font=FONTS['Medium'],fill=(0,255,50))
        self.panel.draw.text((52-d,31), "TARGET" ,font=FONTS['Medium'],fill=(255,255,0))
        if self.balls > 0:
            self.panel.draw.text((61-d,41), self.bonus[9-self.balls][1:] ,font=FONTS['Medium'],fill=(255,255,0))
        if self.got_bonus == 'yes':
            self.panel.draw.text((16-d,53), "BONUS! 1000" ,font=FONTS['Medium'],fill=(255,255,255))
        if self.got_bonus == 'no':
            self.panel.draw.text((27-d,53), "MISSED!" ,font=FONTS['Medium'],fill=(255,255,255))
        #self.panel.draw.text((0,0), str(self.clock.ticks) ,font=FONTS['Tiny'],fill=(255,0,0))
        if self.show_ball_scores:
            for i,(num,b) in enumerate(zip(self.ball_scores,self.ball_bonuses)):
                t=4 if num == '1000' else 0
                color = (255,255,255) if b else (255,0,0)
                self.panel.draw.text((84-t,1+6*i),num,font=FONTS['Tiny'],fill=color)
        
        self.panel.update()

    def main_loop(self,settings):
        self.score = 0
        self.score_buffer = 0
        self.balls = 9
        self.ball_scores = []
        self.ball_bonuses= []
        self.show_ball_scores = False
        self.advance_score = False
        self.bonus_time = time.time()
        self.got_bonus = 'idle'
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

            if self.got_bonus != 'idle':
                if self.clock.ticks > 2*20:
                    self.got_bonus = 'idle'

            if self.balls == 0:
                continue

            if self.sensor.is_pressed(BUTTON[self.bonus[9-self.balls]]):
                self.score_buffer += 1000
                self.got_bonus = 'yes'
                self.ball_scores.append(self.bonus[9-self.balls][1:])
                self.ball_bonuses.append(True)

            else:
                if self.sensor.is_pressed(BUTTON['B1000L']) or self.sensor.is_pressed(BUTTON['B1000R']):
                    self.score_buffer += 1000
                    self.ball_scores.append('1000')
                if self.sensor.is_pressed(BUTTON['B500']):
                    self.score_buffer += 500
                    self.ball_scores.append('500')
                if self.sensor.is_pressed(BUTTON['B400']):
                    self.score_buffer += 400
                    self.ball_scores.append('400')
                if self.sensor.is_pressed(BUTTON['B300']):
                    self.score_buffer += 300
                    self.ball_scores.append('300')
                if self.sensor.is_pressed(BUTTON['B200']):
                    self.score_buffer += 200
                    self.ball_scores.append('200')
                if self.sensor.is_pressed(BUTTON['B100']):
                    self.score_buffer += 100
                    self.ball_scores.append('100')

                if self.sensor.is_pressed(BUTTON['SCORED']):
                    self.got_bonus = 'no'
                    self.ball_bonuses.append(False)

            if self.sensor.is_pressed(BUTTON['SCORED']):
                self.balls-=1
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
        self.panel.draw.text((17, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=(255,200,10))
        self.panel.update()
        
        self.clock.ticks = 0
        wait_ticks = 100 if settings['do_hi_scores'] else 200
        while self.clock.ticks < wait_ticks:
            self.clock.tick(20)
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['ANYBUTTON']):
                self.clock.ticks = wait_ticks