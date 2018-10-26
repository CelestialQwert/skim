from . import manager


def run():
    
    game = manager.Manager()
    game.main_loop()

if __name__ == "__main__":
    run()