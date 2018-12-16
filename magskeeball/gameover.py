from .state import State
from . import resources as res

class GameOver(State):

    #def __init__(self,manager):
    #    super(Dummy,self).__init__(manager)

    def startup(self):
        self.ticks = 0
        self.game_modes = self.manager.game_modes
        self.red_game = self.settings['red_game']
        self.yellow_game = self.settings['yellow_game']

    def handle_event(self,event):
        if event.button == res.B.START and event.down:
            self.activate_new_mode(self.red_game)
        elif event.button == res.B.SELECT and event.down:
            self.activate_new_mode(self.yellow_game)

        elif event.button == res.B.CONFIG and event.down:
            self.activate_new_mode('ATTRACT')

    def activate_new_mode(self,mode):
        if mode in self.game_modes:
            self.manager.next_state = 'INTRO'
            self.persist['active_game_mode'] = mode
        else:
            self.manager.next_state = mode
        self.done = True

    def update(self):
        self.ticks += 1
        if self.ticks >= res.FPS * 5:
            self.manager.next_state = 'ATTRACT'
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        panel.draw.text((3, 34), "GAME OVER",font=res.FONTS['MAGMini'],fill=res.COLORS['RED'])

        if self.persist['active_game_mode'] == 'SPEEDRUN':
            display_time = self.persist['last_score']

            minutes = display_time // (60 * res.FPS)
            seconds = (display_time // res.FPS) % 60
            fraction = 5 * (display_time % res.FPS)

            panel.draw.text((7, 6), "%01d" % minutes, font=res.FONTS['Digital14'], fill=res.COLORS['YELLOW'])
            panel.draw.text((28, 6), "%02d" % seconds, font=res.FONTS['Digital14'], fill=res.COLORS['YELLOW'])
            panel.draw.text((63, 6), "%02d" % fraction, font=res.FONTS['Digital14'], fill=res.COLORS['YELLOW'])
            panel.draw.rectangle([21, 18, 24, 21],fill=res.COLORS['YELLOW'])
            panel.draw.rectangle([21, 9, 24, 12],fill=res.COLORS['YELLOW'])
            panel.draw.rectangle([56, 21, 59, 24],fill=res.COLORS['YELLOW'])
            
        else:
            score = self.persist['last_score']
            score_x = 17 if score < 10000 else 4
            panel.draw.text((score_x, 4), "%04d" % score ,font=res.FONTS['Digital16'],fill=res.COLORS['YELLOW'])
        
        if self.ticks % (2*res.FPS) < (1.5*res.FPS):
            panel.draw.text((15,54), "PRESS START",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])