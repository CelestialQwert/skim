from .state import GameMode
from . import resources as res
import random
import time


class Timed(GameMode):

    has_high_scores = True
    intro_text = [
        "SCORE AS MANY",
        "POINTS AS POSSIBLE",
        "IN 30 SECONDS!"
    ]

    def startup(self):
        self.score = 0
        self.score_buffer = 0
        self.advance_score = False

        self.balls = 0
        self.returned_balls = 0
        self.ball_scores = []
        self.countdown_time = 3

        self.time_remain = (30+self.countdown_time)*res.FPS

        self.persist['active_game_mode'] = 'TIMED'

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button == res.B.CONFIG:
            self.time_remain = 0
        if self.time_remain > 30*res.FPS:
            return
        if event.down and event.button in res.POINTS:
            self.add_score(res.POINTS[event.button])
            res.SOUNDS[event.button.name].play()
        if event.down and event.button == res.B.RETURN:
            self.returned_balls+=1
            if self.returned_balls > self.balls:
                self.add_score(0)
                res.SOUNDS['MISS'].play()
        

    def update(self):
        if self.advance_score:
            if self.score_buffer > 0:
                self.score += 100
                self.score_buffer -= 100
        if self.score_buffer == 0:
            self.advance_score = False
        self.time_remain -= 1
        if self.time_remain <= 0 and not self.advance_score:
            self.manager.next_state = "HIGHSCORE"
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        if self.time_remain > 30*res.FPS:
            display_time = 30*res.FPS
        elif self.time_remain < 0:
            display_time = 0
        else:
            display_time = self.time_remain

        seconds = (display_time // res.FPS) % 60
        fraction = round( 100.0 / res.FPS * (display_time % res.FPS))

        score_x = 17 if self.score < 10000 else 4
        panel.draw.text((score_x, 4), "%04d" % self.score ,font=res.FONTS['Digital16'],fill=res.COLORS['PURPLE'])
            
        panel.draw.text((57,31), "BALLS" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        panel.draw.text((66, 41), "%02d" % self.balls,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        panel.draw.text((12,31), "TIME",font=res.FONTS['Medium'],fill=res.COLORS['GREEN'])
        panel.draw.text((9, 41), "{:02}.{:02}".format(seconds,fraction),font=res.FONTS['Medium'],fill=res.COLORS['GREEN'])

        if self.time_remain > 30*res.FPS:
            display_time = self.time_remain - 30*res.FPS
            seconds = (display_time // res.FPS) % 60 + 1
            panel.draw.text((15,54), "READY... {:1}".format(seconds),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        elif self.time_remain > 28*res.FPS:
            panel.draw.text((39,54), "GO!",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

    def cleanup(self):
        print("Pausing for 1 seconds")
        time.sleep(1)
        self.persist['last_score'] = self.score
        return

    def add_score(self,score):
        self.score_buffer += score
        self.ball_scores.append(score)
        self.balls+=1
        self.advance_score = True
