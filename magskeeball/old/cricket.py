from .common import *
from .game_parent import GameParent
from . import timer
import time

COLOR_MATRIX = [COLORS.BLUE,COLORS.RED]
COLOR_PLAYER = [COLORS.GREEN,COLORS.MAGENTA]
NAME_PLAYER = ['P1','P2']

class Player():
    def __init__(self,num=0):
        self.num = num
        self.hits = [0]*5
        self.target_scores = [0]*5
        self.ball_scores = []
        self.score = 0
        self.score_buffer = 0
        self.target_buffers = [0]*5

class Cricket(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/cricket.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'CRICKET'

    def main_loop(self,settings):

        self.p1 = Player(1)
        self.p2 = Player(2)
        self.running = True
        self.start_prep(settings)

        while self.running:
            self.do_turn(self.p1,self.p2)
            time.sleep(2)
            self.sensor.update_buttons() #blocks balls rolled during pause from counting
            if self.running:
                self.do_turn(self.p2,self.p1)
                time.sleep(2)
                self.sensor.update_buttons()

        self.clock.ticks = 0
        wait_ticks = 20*20
        while self.clock.ticks < wait_ticks:
            self.clock.tick(20)
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['ANYBUTTON']):
                self.clock.ticks = wait_ticks


    def do_turn(self,player,opponent):
        self.balls = 3

        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)
            # if self.clock.ticks % 2:
            #     print('tick')
            # else:
            #     print('tock')
            # print(self.balls,self.advance_score)

            if self.advance_score:
                if player.score_buffer > 0:
                    player.score += 100
                    player.score_buffer -= 100
                    for i in range(len(player.target_buffers)):
                        if player.target_buffers[i] > 0:
                            player.target_buffers[i] -= 100
                            player.target_scores[i] += 100
                    if player.score_buffer == 0:
                        self.advance_score = False

            if self.sensor.is_pressed(BUTTON['CONFIG']):
                self.balls = 0
                self.running = False

            if self.balls == 0:
                self.draw_score(player.num)
                continue
            
            hit = self.detect_balls()
            if self.sensor.is_pressed(BUTTON['SELECT']):
                if self.sensor.is_pressed(BUTTON['START']):
                    self.balls = 0
                    self.running = False
                else:
                    self.balls -= 1

            if hit:
                self.balls -= 1
                player.ball_scores.append(hit)
                idx = -hit // 100
                player.hits[idx] += 1
                if player.hits[idx] > 3 and opponent.hits[idx] < 3:
                    player.score_buffer += hit
                    player.target_buffers[idx] += hit
                    self.advance_score = True

                if min(player.hits) >= 3 and (min(opponent.hits) >= 3 or player.score > opponent.score):
                    self.balls = 0
                    self.running = False


            self.draw_score(player.num)

    def draw_score(self,active_player=1):
        a = active_player - 1
        self.panel.clear()

        self.panel.draw.text((3,2), "P1",font=FONTS['Medium'],fill=COLORS.GREEN)
        self.panel.draw.text((18,2), '{: >4}'.format(str(self.p1.score//10)),font=FONTS['Medium'],fill=COLORS.GREEN)

        self.panel.draw.text((55,2), "P2",font=FONTS['Medium'],fill=COLORS.MAGENTA)
        self.panel.draw.text((70,2), '{: >4}'.format(str(self.p2.score//10)),font=FONTS['Medium'],fill=COLORS.MAGENTA)

        for x,p in enumerate([self.p1,self.p2]):
            for y in range(5):
                posx = 32+26*x
                posy = 13+8*y
                if p.hits[y-5] > 0:
                    self.panel.draw.ellipse((posx,posy,posx+6,posy+6),outline=COLORS.WHITE)
                if p.hits[y-5] > 1:
                    self.panel.draw.line((posx+5,posy+1,posx+1,posy+5),fill=COLORS.WHITE)
                if p.hits[y-5] > 2:
                    self.panel.draw.line((posx+1,posy+1,posx+5,posy+5),fill=COLORS.WHITE)

                num = p.target_scores[y-5]//10
                if num != 0:
                    txt = str(num)
                    l = len(txt)
                    self.panel.draw.text((11+6*(3-l)+58*x,12+8*y), str(txt),font=FONTS['Medium'],fill=COLOR_MATRIX[x])

        for i,txt in enumerate([50,40,30,20,10]):
            self.panel.draw.text((43,12+8*i), str(txt),font=FONTS['Medium'],fill=COLORS.YELLOW)

        if self.running:
            self.panel.draw.text((3,54), "{} BALL LEFT: {}".format(NAME_PLAYER[a],self.balls),font=FONTS['Medium'],fill=COLOR_PLAYER[a])
        else:
            if self.p1.score > self.p2.score:
                self.panel.draw.text((9,54), "PLAYER 1 WIN!",font=FONTS['Medium'],fill=COLORS.GREEN)
            if self.p1.score < self.p2.score:
                self.panel.draw.text((9,54), "PLAYER 2 WIN!",font=FONTS['Medium'],fill=COLORS.MAGENTA)
            if self.p1.score == self.p2.score:
                self.panel.draw.text((18,54), "TIED GAME!",font=FONTS['Medium'],fill=COLORS.WHITE)

        self.panel.update()
