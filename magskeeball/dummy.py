from common import *
import time
from game_parent import GameParent


class Dummy(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/dummy.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'DUMMY'


    def main_loop(self,settings):
        self.panel.clear()
        self.panel.draw.text((1,0), 'GAME NOT MADE',font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.draw.text((1,9), 'RED TO QUIT',font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.update()

        self.sensor.update_buttons()
        while not self.sensor.is_pressed(BUTTON['START']):
            self.sensor.update_buttons()