from .state import State
from . import resources as res

class Settings(State):

    #def __init__(self,manager):
    #    super(Dummy,self).__init__(manager)

    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if event.button == res.B.START and event.down:
            self.manager.next_state = "ATTRACT"
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        panel.draw.text((1,0), 'FAKE SETTINGS',font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((1,9), 'RED TO QUIT',font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])