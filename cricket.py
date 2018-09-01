from common import *
import time
from game_parent import GameParent
import timer

class Cricket(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/cricket.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'CRICKET'
        self.running = True

    def main_loop(self,settings):

        self.start_prep(settings)

        self.draw_cricket()

        while self.running:
            self.detect_stop()
        
    def detect_stop(self):
        self.clock.tick(20)
        self.sensor.update_buttons()

        if self.sensor.is_pressed(BUTTON['CONFIG']):
            self.running = False
        if self.sensor.is_pressed(BUTTON['ANYBUTTON']):
            self.running = False


    def draw_cricket(self):
        self.panel.draw.rectangle([(0, 0), (96, 64)],fill=(0,0,0))
        self.panel.draw.text((3,0), "P1",font=FONTS['Small'],fill=(0,255,0))
        self.panel.draw.text((55,0), "P2",font=FONTS['Small'],fill=(0,255,0))
        self.panel.draw.text((18,0), "2500",font=FONTS['Small'],fill=(0,0,255))
        self.panel.draw.text((70,0), "2500",font=FONTS['Small'],fill=(0,0,255))

        self.panel.draw.text((3,52), "P1 BALLS: 2",font=FONTS['Small'],fill=(255,255,0))
        i=0
        for x in range(2):
            for y in range(5):
                posx = 32+26*x
                posy = 13+8*y
                self.panel.draw.ellipse((posx,posy,posx+6,posy+6),outline=(255,255,255))
                if i%2==0:
                    self.panel.draw.line((posx+5,posy+1,posx+1,posy+5),fill=(255,255,255))
                if i%4==0:
                    self.panel.draw.line((posx+1,posy+1,posx+5,posy+5),fill=(255,255,255))
                i=i+1

        for i,txt in enumerate([50,40,30,20,10]):
            self.panel.draw.text((43,10+8*i), str(txt),font=FONTS['Small'],fill=(255,0,0))

        for i,txt in enumerate([550,120,90,60,30]):
            txt = str(txt)
            l = len(txt)
            self.panel.draw.text((11+6*(3-l),10+8*i), str(txt),font=FONTS['Small'],fill=(255,0,255))
            self.panel.draw.text((69+6*(3-l),10+8*i), str(txt),font=FONTS['Small'],fill=(255,0,255))


        self.panel.update()