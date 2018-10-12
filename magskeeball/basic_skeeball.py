from .manager import State
from .common import *
import pygame
import random
import time

class BasicSkeeball(State):

    def __init__(self):
        super(BasicSkeeball,self).__init__()
        self.persist["screen_color"] = "black"
        self.next_state = "BASIC"

    def startup(self,persist):
        self.persist = persist
        print("BASIC!")

        self.score = 0
        self.score_buffer = 0
        self.balls = 9
        self.ball_scores = []
        self.show_ball_scores = False
        self.advance_score = False
        #self.draw_panel()
        self.start_song = START_MUSIC[random.choice(START_MUSIC_KEYS)]
        self.start_song.play()
        self.ticks = 0
        self.ticks_last_ball = 0
        self.timeout = 30*20

        #self.sensor.release_balls()

    def handle_event(self,event):
        if event.button == Button.QUIT:
            self.quit = True
        if self.balls == 0:
            return 
        if event.down and event.button in POINTS:
            self.add_score(POINTS[event.button])
            SOUNDS[event.button.name].play()
        if event.button == Button.CONFIG:
            self.balls = 0

    def update(self,dt):
        if self.advance_score:
            if self.score_buffer > 0:
                self.score += 100
                self.score_buffer -= 100
                if self.score_buffer == 0:
                    self.advance_score = False
        self.ticks += 1
        print(self.ticks)
        if (self.ticks - self.ticks_last_ball) >  self.timeout:
            self.balls = 0
        if self.balls == 0 and not self.advance_score:
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        d = 6 if self.show_ball_scores else 0
        panel.draw.text((42-d, 39), "%d" % self.balls,font=FONTS['Digital14'],fill=BALL_COLORS[self.balls])
        panel.draw.text((17-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=COLORS['PURPLE'])
        panel.draw.text((16-d,44), "BALL" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        panel.draw.text((57-d,44), "LEFT" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        if self.show_ball_scores:
            for i,num in enumerate(self.ball_scores):
                t=4 if num == '1000' else 0
                panel.draw.text((84-t,1+6*i),num,font=FONTS['Tiny'],fill=COLORS.RED)

    def cleanup(self):
        print("Pausing for 2 seconds")
        time.sleep(2)
        return self.persist

    def add_score(self,score):
        self.score_buffer += score
        self.ball_scores.append(score)
        self.balls-=1
        self.advance_score = True
        #if self.balls in [3,6]:
        #    self.sensor.release_balls()
        self.ticks_last_ball = self.ticks