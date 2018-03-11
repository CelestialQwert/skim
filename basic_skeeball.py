from common import *
import time
from game_parent import GameParent
import timer

DOINGHIGHSCORE = True


class BasicSkeeball(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/basic.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'BASIC'

    def draw_score(self):  
        self.panel.clear()
        d = 6 if self.show_ball_scores else 0
        self.panel.draw.text((42-d, 39), "%d" % self.balls,font=FONTS['Digital14'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((17-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=(100,0,255))
        self.panel.draw.text((16-d,44), "BALL" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((57-d,44), "LEFT" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        if self.show_ball_scores:
            for i,num in enumerate(self.ball_scores):
                t=4 if num == '1000' else 0
                self.panel.draw.text((84-t,1+6*i),num,font=FONTS['Tiny'],fill=(255,0,0))
        self.panel.update()

    def main_loop(self,settings):
        self.score = 0
        self.score_buffer = 0
        self.balls = 9
        self.ball_scores = []
        self.show_ball_scores = False
        self.advance_score = False

        self.sensor.release_balls()

        self.draw_score()

        SOUNDS['START'].play()

        self.clock = timer.Timer()
        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)

            if self.advance_score:
                if self.score_buffer > 0:
                    self.score += 100
                    self.score_buffer -= 100
                else:
                    self.advance_score = False

            if self.clock.ticks > settings['timeout']*20 or self.sensor.is_pressed(BUTTON['CONFIG']):
                self.balls = 0

            self.draw_score()

            if self.balls == 0:
                continue
            
            self.sensor.update_buttons()
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
                self.balls-=1
                self.advance_score = True
                if self.balls in [3,6]:
                    self.sensor.release_balls()
                self.clock.ticks = 0

            if self.sensor.is_pressed(BUTTON['SELECT']):
                self.sensor.release_balls()

            #print("score:{} balls:{}".format(self.score,self.balls))

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
