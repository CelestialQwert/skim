from .state import State
from . import resources as res

class GameOver(State):

    #def __init__(self,manager):
    #    super(Dummy,self).__init__(manager)

    def startup(self):
        self.ticks = 0
        self.red_game = self.settings['red_game']
        self.yellow_game = self.settings['yellow_game']

    def handle_event(self,event):
        if event.button == res.B.START and event.down:
            self.manager.next_state = 'INTRO'
            self.persist['active_game_mode'] = self.red_game
            self.persist['last_color'] = 'red'
            self.done = True
        elif event.button == res.B.SELECT and event.down:
            self.manager.next_state = 'INTRO'
            self.persist['active_game_mode'] = self.yellow_game
            self.persist['last_color'] = 'yellow'
            self.done = True
        elif event.button == res.B.CONFIG and event.down:
            self.manager.next_state = 'ATTRACT'
            self.done = True

    def update(self):
        self.ticks += 1
        if self.ticks >= res.FPS * 10:
            self.manager.next_state = 'ATTRACT'
            self.done = True

    def draw_panel(self,panel):
        panel.clear()
        #panel.draw.text((0,0), self.name ,font=FONTS['Tiny'],fill=COLORS.GREEN)
#        panel.draw.text((8, 26), "GAME",font=res.FONTS['GameOver'],fill=res.COLORS['RED'])
#        panel.draw.text((25, 39), "OVER",font=res.FONTS['GameOver'],fill=res.COLORS['RED'])
        # panel.draw.text((8, 26), "GAME",font=res.FONTS['MAGFest'],fill=res.COLORS['RED'])
        # panel.draw.text((32, 38), "OVER",font=res.FONTS['MAGFest'],fill=res.COLORS['RED'])
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
            score_x = 17 if self.score < 10000 else 4
            panel.draw.text((score_x, 4), "%04d" % self.score ,font=res.FONTS['Digital16'],fill=res.COLORS['YELLOW'])
        
        if self.ticks % (2*res.FPS) < (1.5*res.FPS):
            panel.draw.text((15,54), "PRESS START",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])