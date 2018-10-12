import sys
import pygame
from . import panel
from . import sensor
from . import manager
from . import basic_skeeball
from .common import *


def run():

    states = {
            "BASIC": basic_skeeball.BasicSkeeball(),
        }
    starting_state = 'BASIC'
    
    game = manager.Manager(states,starting_state)
    game.main_loop()

if __name__ == "__main__":
    run()