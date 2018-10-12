from .common import *
from .game_parent import GameParent
from . import timer

DOINGHIGHSCORE = True

#GameParent is pretty much Basic mode
#but we need to change the name 

class BasicSkeeball(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/basic.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'BASIC'

