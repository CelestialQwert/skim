from common import *
import time
from game_parent import GameParent
import timer

DOINGHIGHSCORE = True


class BasicSkeeball(GameParent):

    def __init__(self,panel,sensor):
        self.score_filename = 'high_scores/basic.txt'
        GameParent.__init__(self,panel,sensor)
        self.name = 'BASIC'

    def main_loop(self,settings):

        self.start_prep(settings)

        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)

            self.loop_part1()

            if self.balls == 0:
                continue
            
            self.resolve_balls(self.detect_balls())


        self.post_game()
