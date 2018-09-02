from common import *
import time
from game_parent import GameParent
import timer

class Cricket(GameParent):



    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/cricket.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'CRICKET'

    def main_loop(self,settings):

        self.draw_cricket()

        self.sensor.update_buttons()
        while not self.sensor.is_pressed(BUTTON['ANYBUTTON']):
            self.sensor.update_buttons()

    def draw_cricket(self):
        self.panel.clear()

        self.panel.draw.text((3,2), "P1",font=FONTS['Medium'],fill=COLORS.GREEN)
        self.panel.draw.text((18,2), "2500",font=FONTS['Medium'],fill=COLORS.GREEN)

        self.panel.draw.text((55,2), "P2",font=FONTS['Medium'],fill=COLORS.MAGENTA)
        self.panel.draw.text((70,2), "2500",font=FONTS['Medium'],fill=COLORS.MAGENTA)

        self.panel.draw.text((3,54), "P1 BALLS: 2",font=FONTS['Medium'],fill=COLORS.GREEN)
        i=0
        for x in range(2):
            for y in range(5):
                posx = 32+26*x
                posy = 13+8*y
                self.panel.draw.ellipse((posx,posy,posx+6,posy+6),outline=COLORS.WHITE)
                if i%2==0:
                    self.panel.draw.line((posx+5,posy+1,posx+1,posy+5),fill=COLORS.WHITE)
                if i%4==0:
                    self.panel.draw.line((posx+1,posy+1,posx+5,posy+5),fill=COLORS.WHITE)
                i=i+1

        for i,txt in enumerate([50,40,30,20,10]):
            self.panel.draw.text((43,12+8*i), str(txt),font=FONTS['Medium'],fill=COLORS.YELLOW)

        for i,txt in enumerate([550,120,90,60,30]):
            txt = str(txt)
            l = len(txt)
            self.panel.draw.text((11+6*(3-l),12+8*i), str(txt),font=FONTS['Medium'],fill=COLORS.CYAN)
            self.panel.draw.text((69+6*(3-l),12+8*i), str(txt),font=FONTS['Medium'],fill=COLORS.RED)


        self.panel.update()