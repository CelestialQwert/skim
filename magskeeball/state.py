class State():

    def __init__(self,manager):
        self.manager = manager
        self.settings = self.manager.settings
        self.persist = self.manager.persist
        self.done = False
        self.quit = False

    def startup(self):
        pass

    def handle_event(self,event):
        if event.button == Button.QUIT:
            self.quit = True

    def update(self):
        pass

    def draw_panel(self,panel):
        pass

    def cleanup(self):
        pass

class GameMode(State):
    has_high_scores = False
    intro_text = [
        "I'M A SKEE-BALL",
        "MODE!",
        "ALLAN PLEASE",
        'ADD DETAILS'
    ]
