from .state import State
from . import resources as res
import os
import time
import shutil

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ._<%'

class HighScore(State):

    def __init__(self,manager):
        super(HighScore,self).__init__(manager)
        self.high_scores = {}

    def startup(self):
        self.manager.next_state = 'GAMEOVER'
        self.active_game_mode = self.persist['active_game_mode']

        print('old list',self.persist['hs_game_hist'])
        self.persist['hs_game_hist'] = [self.active_game_mode] + self.persist['hs_game_hist']
        temp_hist = []
        for game in self.persist['hs_game_hist']:
            if game not in temp_hist:
                temp_hist.append(game)
        self.persist['hs_game_hist'] = temp_hist[:2]
        print('new list',self.persist['hs_game_hist'])

        self.score = self.persist['last_score']
        self.game_high_scores = self.high_scores[self.active_game_mode]

        place = 0

        self.name = ''
        self.cursor = 0
        self.ticks = 0
        self.new_score = False

        for their_name,their_score in self.game_high_scores:
            place += 1
            their_score = int(their_score)
            if (self.score > their_score and self.persist['active_game_mode'] != 'SPEEDRUN') \
            or (self.score < their_score and self.persist['active_game_mode'] == 'SPEEDRUN'):
                self.new_score = True
                self.place = place
                res.SOUNDS['PLACE%d' % self.place].play()
                return


    def handle_event(self,event):
        if event.button == res.B.QUIT:
            self.quit = True
        if not self.new_score:
            return
        if event.down and event.button == res.B.SELECT:
            self.cursor = (self.cursor+1)%len(LETTERS)
        if event.down and event.button == res.B.START:
            if self.curr_letter == '<':
                self.cursor = LETTERS.find(self.name[-1])
                if self.cursor == -1:
                    #space isn't in LETTERS, so make it a _ instead
                    self.cursor = LETTERS.find('_')
                self.name = self.name[:-1]
            elif self.curr_letter == '%':
                #name is done so pad with spaces
                while len(self.name) < 4:
                    self.name = self.name + ' '
            else:
                self.name = self.name + self.curr_letter
                if len(self.name) == 3:
                    self.cursor = len(LETTERS)-1
                else:
                    self.cursor = 0
                #underscores are there so spaces can be seen
                self.name = self.name.replace('_',' ')
            #if name is 3 letters, lock out everything but OK and < (last 2 chars)
            if len(self.name) == 3 and self.cursor < len(LETTERS)-2:
                self.cursor = len(LETTERS)-2 


    def update(self):
        if not self.new_score:
            self.done = True
            return
        if len(self.name) == 4:
            self.done = True
        self.ticks += 1
        self.curr_letter = LETTERS[self.cursor]
        

    def draw_panel(self,panel):
        if not self.new_score:
            return
        panel.clear()

        if self.persist['active_game_mode'] == 'SPEEDRUN':
            display_time = self.persist['last_score']

            minutes = display_time // (60 * res.FPS)
            seconds = (display_time // res.FPS) % 60
            fraction = round( 100.0 / res.FPS * (display_time % res.FPS))

            panel.draw.text((7, 6), "%01d" % minutes, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
            panel.draw.text((28, 6), "%02d" % seconds, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
            panel.draw.text((63, 6), "%02d" % fraction, font=res.FONTS['Digital14'], fill=res.COLORS['PURPLE'])
            panel.draw.rectangle([21, 18, 24, 21],fill=res.COLORS['PURPLE'])
            panel.draw.rectangle([21, 9, 24, 12],fill=res.COLORS['PURPLE'])
            panel.draw.rectangle([56, 21, 59, 24],fill=res.COLORS['PURPLE'])

            panel.draw.text((16,30), "GREAT TIME!" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
            
        else:
            score_x = 17 if self.score < 10000 else 4
            panel.draw.text((score_x, 4), "%04d" % self.score ,font=res.FONTS['Digital16'],fill=res.COLORS['PURPLE'])
            
            panel.draw.text((16,30), "HIGH SCORE!" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])

        #each line is shown for 3/2 (1.5) seconds
        if self.ticks % 90 < 30:
            panel.draw.text((7,40), "ENTER INITIALS" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        elif self.ticks % 90 < 60:
            panel.draw.text((3,40), "YELLOW = CHANGE" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        else:
            panel.draw.text((18,40), "RED = PICK" ,font=res.FONTS['Medium'],fill=res.COLORS['YELLOW'])
        panel.draw.text((39,50), self.name ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        if self.ticks % 4 < 3 and len(self.name) < 4:
            #blink current letter
            panel.draw.text((39+6*len(self.name),50), self.curr_letter ,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])
        panel.draw.text((19,50), "#%d" % self.place,font=res.FONTS['Medium'],fill=res.COLORS['WHITE'])

    def cleanup(self):
        if self.new_score:
            print("Pausing for 2 seconds")
            time.sleep(2)
            self.name = self.name[:3]
            new_high_scores = self.game_high_scores[:self.place-1] + [(self.name, self.score)] + self.game_high_scores[self.place-1:4]
            self.save_high_scores(self.active_game_mode,new_high_scores)


    def load_all_high_scores(self):
        for game_mode in self.manager.game_modes:
            if self.manager.states[game_mode].has_high_scores:
                self.high_scores[game_mode] = self.load_high_scores(game_mode)
        return self.high_scores

    def init_all_high_scores(self):
        for game_mode in self.manager.game_modes:
            if self.manager.states[game_mode].has_high_scores:
                self.high_scores[game_mode] = self.init_high_scores(game_mode)
        return self.high_scores

    def init_high_scores(self,game_mode):
        filename = './high_scores/{}.txt'.format(game_mode)
        if not os.path.isdir('./high_scores'):
            os.mkdir('./high_scores')
            os.chmod('./high_scores',0o777)
        if os.path.isfile(filename):
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
            archive_file = './high_scores/{}_{}.txt'.format(game_mode,timestamp)
            shutil.move(filename,archive_file)
        with open(filename,'w') as sf:
            if game_mode == 'SPEEDRUN':
                sf.write('MAG,1120\nFES,1140\nTIS,1160\nADO,1180\nNUT,1199\n')
            else:
                sf.write('MAG,2000\nFES,1600\nTIS,1200\nADO,800\nNUT,400\n')
        os.chmod(filename,0o777)
        return self.load_high_scores(game_mode)

    def load_high_scores(self,game_mode):
        filename = './high_scores/{}.txt'.format(game_mode)
        high_scores = []
        try:
            with open(filename,'r') as score_file:
                for line in score_file.readlines():
                    name,score = line.split(',')
                    if len(name) > 3:
                        raise IOError('Name is too long')
                    score = int(score)
                    high_scores.append((name,score))
        except:
            print('Error in hi score file, creating new...')
            high_scores = self.init_high_scores(game_mode)
        return high_scores

    def save_high_scores(self,game_mode,scores):
        filename = './high_scores/{}.txt'.format(game_mode)
        with open(filename,'w') as sf:
            for name,score in scores:
                sf.write('{},{}\n'.format(name,score))
        self.high_scores[game_mode] = scores
