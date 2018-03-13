from common import *
import time
import os
import shutil
import qrcode


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ._<%'

class GameParent():

    def __init__(self,panel,sensor):
        self.panel = panel
        self.sensor = sensor
        self.load_hi_scores()
        
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
        self.panel.draw.text((55,2), "TWEET",font=FONTS['Medium'],fill=(255,255,255))
        self.panel.draw.text((57,11), "YOUR",font=FONTS['Medium'],fill=(255,255,255))
        self.panel.draw.text((54,20), "SCORE!",font=FONTS['Medium'],fill=(255,255,255))
        self.panel.draw.text((57,35), str(self.score),font=FONTS['Medium'],fill=(255,255,255))
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
        score_x = 17 if self.score < 10000 else 4#1
        self.panel.draw.text((score_x, 4), "%04d" % self.score ,font=FONTS['Digital16'],fill=(100,0,255))
        self.panel.draw.text((16,30), "HIGH SCORE!" ,font=FONTS['Medium'],fill=(255,255,50))
        #each line is shown for 3/2 (1.5) seconds
        deltime = int((time.time() - self.base_time)*2/3)
        if deltime%3 == 0:
            self.panel.draw.text((7,40), "ENTER INITIALS" ,font=FONTS['Medium'],fill=(255,255,50))
        if deltime%3 == 1:
            self.panel.draw.text((4,40), "YELLOW = CHANGE" ,font=FONTS['Medium'],fill=(255,255,50))
        if deltime%3 == 2:
            self.panel.draw.text((19,40), "RED = PICK" ,font=FONTS['Medium'],fill=(255,255,50))
        self.panel.draw.text((39,50), self.your_name ,font=FONTS['Medium'],fill=(255,255,255))
        if int(time.time()*8)%4 != 0:
            #blink current letter
            self.panel.draw.text((39+6*len(self.your_name),50), self.curr_letter ,font=FONTS['Medium'],fill=(255,255,255))
        self.panel.draw.text((19,50), "#%d" % self.place,font=FONTS['Medium'],fill=(255,255,255))

        self.panel.update()






