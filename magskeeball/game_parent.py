from common import *
import time
import os
import shutil
import random
import timer

#GameParent is pretty much Basic mode

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ._<%'
DOINGHIGHSCORE = True

class GameParent():

    def __init__(self,panel,sensor):
        self.panel = panel
        self.sensor = sensor
        self.load_hi_scores()
        self.name = 'GAMEPARENT'

    def main_loop(self,settings):

        self.start_prep(settings)

        while self.balls > 0 or self.advance_score:
            self.clock.tick(20)
            self.loop_part1()
            if self.balls == 0:
                continue
            self.resolve_balls(self.detect_balls())

        self.post_game()

    def draw_score(self):  
        self.panel.clear()
        d = 6 if self.show_ball_scores else 0
        self.panel.draw.text((42-d, 39), "%d" % self.balls,font=FONTS['Digital14'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((17-d, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=COLORS.PURPLE)
        self.panel.draw.text((16-d,44), "BALL" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        self.panel.draw.text((57-d,44), "LEFT" ,font=FONTS['Medium'],fill=BALL_COLORS[self.balls])
        if self.show_ball_scores:
            for i,num in enumerate(self.ball_scores):
                t=4 if num == '1000' else 0
                self.panel.draw.text((84-t,1+6*i),num,font=FONTS['Tiny'],fill=COLORS.RED)
        self.panel.update()

    def start_prep(self,settings):
        self.settings = settings
        self.score = 0
        self.score_buffer = 0
        self.balls = 9
        self.ball_scores = []
        self.show_ball_scores = False
        self.advance_score = False

        self.sensor.release_balls()

        self.draw_score()
        self.start_song = START_MUSIC[random.choice(START_MUSIC_KEYS)]
        self.start_song.play()

        self.clock = timer.Timer()

    def loop_part1(self):
        if self.advance_score:
            if self.score_buffer > 0:
                self.score += 100
                self.score_buffer -= 100
                if self.score_buffer == 0:
                    self.advance_score = False

        if self.clock.ticks > self.settings['timeout']*20 or self.sensor.is_pressed(BUTTON['CONFIG']):
            self.balls = 0

        self.draw_score()

    def detect_balls(self):
        self.sensor.update_buttons()

        hit = False

        if self.sensor.is_pressed(BUTTON['B1000L']) or self.sensor.is_pressed(BUTTON['B1000R']):
            hit = 1000
            SOUNDS['SCORE1000'].play()
        if self.sensor.is_pressed(BUTTON['B500']):
            hit = 500
            SOUNDS['SCORE500'].play()
        if self.sensor.is_pressed(BUTTON['B400']):
            hit = 400
            SOUNDS['SCORE400'].play()
        if self.sensor.is_pressed(BUTTON['B300']):
            hit = 300
            SOUNDS['SCORE300'].play()
        if self.sensor.is_pressed(BUTTON['B200']):
            hit = 200
            SOUNDS['SCORE200'].play()
        if self.sensor.is_pressed(BUTTON['B100']):
            hit = 100
            SOUNDS['SCORE100'].play()

        if self.sensor.is_pressed(BUTTON['SELECT']):
            self.sensor.release_balls()

        return hit

    def resolve_balls(self,hit):
        if hit:
            self.score_buffer += hit
            self.ball_scores.append(hit)
            self.balls-=1
            self.advance_score = True
            if self.balls in [3,6]:
                self.sensor.release_balls()
            self.clock.ticks = 0


    def post_game(self):
        time.sleep(1)

        if False:
            self.show_qr_code()

        if self.settings['do_hi_scores']:
            self.check_high_score()
        
        self.clock.ticks = 0
        wait_ticks = 600 if self.settings['do_hi_scores'] else 600
        while self.clock.ticks < wait_ticks:
            self.clock.tick(20)
            self.draw_game_over()
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['ANYBUTTON']):
                self.clock.ticks = wait_ticks

    def draw_game_over(self):
        self.panel.clear()
        self.panel.draw.text((0,0), self.name ,font=FONTS['Tiny'],fill=COLORS.GREEN)
        self.panel.draw.text((8, 26), "GAME",font=FONTS['GameOver'],fill=COLORS.RED)
        self.panel.draw.text((25, 39), "OVER",font=FONTS['GameOver'],fill=COLORS.RED)
        score_x = 17 if self.score < 10000 else 4
        self.panel.draw.text((score_x, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=COLORS.YELLOW)
        if self.clock.ticks % 40 < 30:
            self.panel.draw.text((15,54), "PRESS START",font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.update()
        
    def load_hi_scores(self,erase=False):
        if erase:
            timestamp = time.strftime('_%Y-%m-%d_%H-%M-%S')
            archive_file = self.score_filename.split('.')[0] + timestamp + '.txt'
            shutil.move(self.score_filename,archive_file)
        if not os.path.isdir('./high_scores'):
            os.mkdir('./high_scores')
            os.chmod('./high_scores',0o777)
        if not(os.path.isfile(self.score_filename)) or erase:
            with open(self.score_filename,'w') as sf:
                sf.write('MAG,2000\nFES,1600\nTIS,1200\nADO,800\nNUT,400\n')
            os.chmod(self.score_filename,0o777)
        self.score_file = open(self.score_filename,'r')
        self.high_scores = []
        for line in self.score_file.readlines():
            name,score = line.split(',')
            score = int(score)
            self.high_scores.append((name,score))
        self.score_file.close()

    def show_qr_code(self):
        import qrcode

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=1,
            border=3,
        )
        qr_text = 'https://twitter.com/intent/tweet?text=I+got+{}+points+playing+Skee-Ball+at+MAGFest!'.format(self.score)
        qr.add_data(qr_text)
        qr.make(fit=True)

        img = qr.make_image()

        self.panel.clear()
        self.panel.paste(img,(2,2))
        self.panel.draw.text((55,2), "TWEET",font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.draw.text((57,11), "YOUR",font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.draw.text((54,20), "SCORE!",font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.draw.text((57,35), str(self.score),font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.update()
        
        self.clock.ticks = 0
        wait_ticks = 400
        while self.clock.ticks < wait_ticks:
            self.clock.tick(20)
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['ANYBUTTON']):
                self.clock.ticks = wait_ticks


    def check_high_score(self):
        self.place = 0
        temp_hi_scores = []
        new_score = False
        for their_name,their_score in self.high_scores:
            self.place += 1
            their_score = int(their_score)
            if self.score > their_score and not(new_score):
                self.get_name()
                new_score = True
                temp_hi_scores.append((self.your_name,self.score))
            temp_hi_scores.append((their_name,their_score))
        if new_score:
            self.high_scores = temp_hi_scores[0:5]
            with open(self.score_filename,'w') as sf:
                for name,score in self.high_scores:
                    sf.write('{},{}\n'.format(name,score))

    def get_name(self):
        SOUNDS['PLACE%d' % self.place].play()
        self.your_name = ''
        self.cursor = 0
        self.base_time = time.time()

        frame_time = time.time()
        while len(self.your_name) < 4:
            while frame_time + 1/FPS > time.time():
                pass
            #old_time = frame_time
            frame_time = time.time()
            #print((time.time() - old_time))

            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['SELECT']):
                self.cursor = (self.cursor+1)%len(LETTERS)
            if self.sensor.is_pressed(BUTTON['START']):
                if self.curr_letter == '<':
                    self.cursor = LETTERS.find(self.your_name[-1])
                    if self.cursor == -1:
                        #space isn't in LETTERS, so make it a _ instead
                        self.cursor = LETTERS.find('_')
                    self.your_name = self.your_name[:-1]
                elif self.curr_letter == '%':
                    #name is done so pad with spaces
                    while len(self.your_name) < 4:
                        self.your_name = self.your_name + ' '
                else:
                    self.your_name = self.your_name + self.curr_letter
                    if len(self.your_name) == 3:
                        self.cursor = len(LETTERS)-1
                    else:
                        self.cursor = 0
                    #underscores are there so spaces can be seen
                    self.your_name = self.your_name.replace('_',' ')
            #if name is 3 letters, lock out everything but OK and < (last 2 chars)
            if len(self.your_name) == 3 and self.cursor < len(LETTERS)-2:
                self.cursor = len(LETTERS)-2 
            self.curr_letter = LETTERS[self.cursor]
            self.draw_high_score()

        self.curr_letter = ' '
        self.draw_high_score()
        time.sleep(2)
        #chop off 4th letter
        self.your_name = self.your_name[:3]

    def draw_high_score(self):  
        self.panel.clear()
        score_x = 17 if self.score < 10000 else 4
        self.panel.draw.text((score_x, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=COLORS.PURPLE)
        self.panel.draw.text((16,30), "HIGH SCORE!" ,font=FONTS['Medium'],fill=COLORS.YELLOW)
        #each line is shown for 3/2 (1.5) seconds
        deltime = int((time.time() - self.base_time)*2/3)
        if deltime%3 == 0:
            self.panel.draw.text((7,40), "ENTER INITIALS" ,font=FONTS['Medium'],fill=COLORS.YELLOW)
        if deltime%3 == 1:
            self.panel.draw.text((4,40), "YELLOW = CHANGE" ,font=FONTS['Medium'],fill=COLORS.YELLOW)
        if deltime%3 == 2:
            self.panel.draw.text((19,40), "RED = PICK" ,font=FONTS['Medium'],fill=COLORS.YELLOW)
        self.panel.draw.text((39,50), self.your_name ,font=FONTS['Medium'],fill=COLORS.WHITE)
        if int(time.time()*8)%4 != 0:
            #blink current letter
            self.panel.draw.text((39+6*len(self.your_name),50), self.curr_letter ,font=FONTS['Medium'],fill=COLORS.WHITE)
        self.panel.draw.text((19,50), "#%d" % self.place,font=FONTS['Medium'],fill=COLORS.WHITE)

        self.panel.update()






