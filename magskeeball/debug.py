from .state import GameMode
from . import resources as res
import random
import time


class Debug(GameMode):

    intro_text = [
        "DEBUG MODE"
    ]

    def startup(self):
        self.score = 0
        self.score_buffer = 0
        self.advance_score = False

        self.balls = 0
        self.returned_balls = 0
        self.ball_scores = []

        self.debug = self.settings['debug']

        self.ticks = 0

        self.persist['active_game_mode'] = 'DEBUG'

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button in [res.B.CONFIG,res.B.START,res.B.SELECT]:
            self.done = True
            self.manager.next_state = "GAMEOVER"
        if event.down and event.button in res.POINTS:
            self.add_score(res.POINTS[event.button])
            res.SOUNDS[event.button.name].play()
        if event.down and event.button == res.B.RETURN:
            self.returned_balls+=1
            if self.returned_balls > self.balls:
                self.add_score(0)
                res.SOUNDS['MISS'].play()
        

    def update(self):
        if self.advance_score and self.score == 9100:
            res.SOUNDS['OVER9000'].play()

        if self.advance_score:
            if self.score_buffer > 0:
                self.score += 100
                self.score_buffer -= 100
        if self.score_buffer == 0:
            self.advance_score = False
        self.ticks += 1


    def draw_panel(self,panel):
        panel.clear()

        score_x = 17 if self.score < 10000 else 4
        panel.draw.text((score_x, 4), "%04d" % self.score ,font=res.FONTS['Digital16'],fill=res.COLORS['PURPLE'])
            
        panel.draw.text((47,31), "BALLS" ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((53, 41), "{:03d}".format(self.balls),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

        panel.draw.text((7,31), "TIME",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((7, 41), "{:04d}".format(self.ticks),font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])



        for i,num in enumerate(self.ball_scores[-9:]):
            num = str(num)
            t = 4*len(num)
            panel.draw.text((96-t,1+6*i),num,font=res.FONTS['Tiny'],fill=res.COLORS['RED'])
        panel.draw.text((85,57), "{:02}".format(self.returned_balls),font=res.FONTS['Small'],fill=res.COLORS['ORANGE'])

        if self.done:
            panel.draw.text((15,54), "EXITING...",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])



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
