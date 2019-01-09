from .state import GameMode
from . import resources as res
import random
import time


class Speedrun(GameMode):

    has_high_scores = True
    intro_text = [
        "HOW FAST CAN YOU",
        "SCORE 5000 POINTS?"
    ]

    def startup(self):
        self.score = 5000
        self.score_buffer = 0
        self.advance_score = False

        self.balls = 0
        self.returned_balls = 0
        self.ball_scores = []
        self.countdown_time = 3
        
        self.debug = self.settings['debug']

        self.time_elapsed = -self.countdown_time*res.FPS
        self.timeout = self.settings['timeout']*res.FPS
        self.time_last_ball = self.time_elapsed

        self.persist['active_game_mode'] = 'SPEEDRUN'

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button == res.B.CONFIG:
            self.time_elapsed = 600*res.FPS - 2
        if self.time_elapsed < 0:
            return
        if event.down and event.button in res.POINTS:
            self.add_score(res.POINTS[event.button])
            self.last_sound = res.SOUNDS[event.button.name].play()
        if event.down and event.button == res.B.RETURN:
            self.returned_balls+=1
            if self.returned_balls > self.balls:
                self.add_score(0)
                res.SOUNDS['MISS'].play()
        

    def update(self):

        if self.time_elapsed == -self.countdown_time*res.FPS:
            res.SOUNDS['READY'].play()
        elif self.time_elapsed == -res.FPS//4: #the sound clip has a delay so this syncs it up
            res.SOUNDS['GO'].play()

        if self.advance_score:
            if self.score_buffer > 0:
                self.score -= 100
                self.score_buffer -= 100
        if self.score_buffer == 0:
            self.advance_score = False

        if (self.time_elapsed - self.time_last_ball) > self.timeout:
            self.time_elapsed = 600*res.FPS - 2

        if self.score <= 0:
            if not self.advance_score:
                self.manager.next_state = "HIGHSCORE"
                self.done = True
        else:
            self.time_elapsed += 1

        

        if self.time_elapsed >= 599*res.FPS:
            self.manager.next_state = "HIGHSCORE"
            self.done = True

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

        if self.score <= 500:
            score_color = res.COLORS['RED']
        elif self.score <= 1500:
            score_color = res.COLORS['YELLOW']
        else:
            score_color = res.COLORS['GREEN']

        panel.draw.text((9,31), "SCORE",font=res.FONTS['Medium'],fill=score_color)
        score = self.score if self.score > 0 else 0
        panel.draw.text((12, 41), "%04d" % score,font=res.FONTS['Medium'],fill=score_color)

            

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

    def cleanup(self):
        if self.last_sound:
            self.last_sound.stop()
        res.TARGET_SFX['COMPLETE'].play()
        print("Pausing for 2 seconds")
        time.sleep(2)
        self.persist['last_score'] = self.time_elapsed
        return

    def add_score(self,score):
        self.score_buffer += score
        self.ball_scores.append(score)
        self.balls+=1
        self.advance_score = True
        self.time_last_ball = self.time_elapsed

