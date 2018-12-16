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

        self.time_remain = 32.0

        self.persist['active_game_mode'] = 'TIMED'

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button == res.B.CONFIG:
            self.time_remain = 0.0
        if self.time_remain > 30:
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
        self.time_remain -= 1 / res.FPS
        if self.time_remain <= 0 and not self.advance_score:
            self.manager.next_state = "HIGHSCORE"
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        if self.time_remain > 30:
            display_time = 30.0
        elif self.time_remain < 0:
            display_time = 0.0
        else:
            display_time = self.time_remain

        panel.draw.text((2,2), "TIME: {:04.1f}".format(display_time),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((2,12), "BALLS: {}".format(self.balls),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((2,22), "SCORE: {}".format(self.score),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

        if self.time_remain > 30:
            panel.draw.text((2,42), "READY...: {:03.1f}".format(self.time_remain-30),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        elif self.time_remain > 28:
            panel.draw.text((2,42), "GO!",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

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
        #if self.balls in [3,6]:
        #    self.sensor.release_balls()
