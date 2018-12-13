from .state import State
from . import resources as res
import random


HISCORE_COLORS = [
    res.COLORS['BLUE'],
    res.COLORS['RED'],
    res.COLORS['YELLOW'],
    res.COLORS['GREEN'],
    res.COLORS['PINK'],
]

class Attract(State):

    def startup(self):
        self.ticks = 0
        self.red_game = self.settings['red_game']
        self.yellow_game = self.settings['yellow_game']
        self.high_scores = self.manager.high_scores
        self.has_high_scores = self.manager.has_high_scores            
        if not self.settings['save_high_scores']:
            self.display_queue = [self.draw_logo]
        else:
            self.display_queue = self.get_display_queue()
        self.current_display_ticks = 0
        self.current_display_func, self.current_display_time = self.display_queue[0]
        self.current_display = 0
        self.attract_song = res.ATTRACT_MUSIC[random.choice(res.ATTRACT_MUSIC_KEYS)]


    def get_display_queue(self):
        queue = []
        if self.persist['last_color'] == 'red':
            if self.has_high_scores[self.red_game]:
                queue.append((self.draw_red_scores,10))
            queue.append((self.draw_logo,10))
            if self.has_high_scores[self.yellow_game]:
                queue.append((self.draw_yellow_scores,10))
                if queue[0] != self.draw_logo:
                    queue.append((self.draw_logo,10))
        elif self.persist['last_color'] == 'yellow':
            if self.has_high_scores[self.yellow_game]:
                queue.append((self.draw_yellow_scores,10))
            queue.append((self.draw_logo,10))
            if self.has_high_scores[self.red_game]:
                queue.append((self.draw_red_scores,10))
                if queue[0] != self.draw_logo:
                    queue.append((self.draw_logo,10))
        else:
            if self.has_high_scores[self.red_game]:
                queue.append((self.draw_logo,10))
                queue.append((self.draw_red_scores,10))
            if self.has_high_scores[self.yellow_game]:
                queue.append((self.draw_logo,10))
                queue.append((self.draw_yellow_scores,10))
            if queue == []:
                queue.append((self.draw_logo,10))
        return queue

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
            self.manager.next_state = 'SETTINGS'
            self.persist['last_color'] = 'settings'
            self.done = True

    def update(self):
        self.ticks += 1
        self.current_display_ticks +=1
        if self.ticks % (90*res.FPS) == res.FPS*30:
            #play jingle once every 90 seconds if idle, starting 30 seconds in
            self.attract_song = res.ATTRACT_MUSIC[random.choice(res.ATTRACT_MUSIC_KEYS)]
            self.attract_song.play()
        if self.current_display_ticks >= (self.current_display_time*res.FPS):
            self.current_display_ticks = 0
            self.current_display = (self.current_display + 1) % len(self.display_queue)
            self.current_display_func, self.current_display_time = self.display_queue[self.current_display]
            print('Switching to next display {}/{}'.format(self.current_display,len(self.display_queue)))


    def draw_panel(self,panel):
        panel.clear()

        self.current_display_func(panel)

        if self.ticks % (2*res.FPS) < (1.5*res.FPS):
            panel.draw.text((15,54), "PRESS START",font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

    def draw_logo(self,panel):
        panel.paste(res.IMAGES['MainLogo'],(0,5))

    def draw_red_scores(self,panel):
        self.draw_high_scores(panel,self.red_game)

    def draw_yellow_scores(self,panel):
        self.draw_high_scores(panel,self.yellow_game)

    def draw_high_scores(self,panel,game):
        title_text = '{} HI SCORES'.format(game)
        x = int(48-len(title_text)*2.5)+1
        panel.draw.text((x,2),title_text,font=res.FONTS['Small'],fill=res.COLORS['WHITE'])

        for i,(name,score) in enumerate(self.high_scores[game]):
            if self.high_scores[game][0][1] > 9999:
                panel.draw.text((5+8*i,(i+1)*9),'{} {:5d}'.format(name,score),font=res.FONTS['Medium'],fill=HISCORE_COLORS[i])
            else:
                panel.draw.text((8+8*i,(i+1)*9),'{} {:4d}'.format(name,score),font=res.FONTS['Medium'],fill=HISCORE_COLORS[i])

        # self.panel.draw.text((24,10),'{} {}'.format(name,score),font=FONTS['Medium'],fill=HISCORE_COLORS[0])
        # for i in [1,2,3,4]:
        #     (name,score) = game.high_scores[i]
        #     self.panel.draw.text((28,i*8+12),'{} {}'.format(name,score),font=FONTS['Small'],fill=HISCORE_COLORS[i])

    def cleanup(self):
        self.attract_song.stop()