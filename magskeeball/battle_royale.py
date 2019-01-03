from .state import GameMode
from . import resources as res

class BattleRoyale(GameMode):


    intro_text = [
        "100 PLAYERS ENTER,",
        "ONE PLAYER LEAVES!"
    ]

    #def __init__(self,manager):
    #    super(Dummy,self).__init__(manager)

    def startup(self):
        self.ticks = 0
        self.persist['last_score'] = 0

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button == res.B.START and event.down:
            self.manager.next_state = "GAMEOVER"
            self.done = True

    def update(self):
        self.ticks += 1
        if self.ticks >= 7*res.FPS:
            self.manager.next_state = "GAMEOVER"
            self.done = True


    def draw_panel(self,panel):
        panel.clear()
        panel.draw.text((1,0), 'WHAT DO YOU',font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((1,9), 'THINK THIS IS,',font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((1,18), 'FORTNITE?',font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((1,27), 'DORK.',font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
