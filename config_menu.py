from common import *
import time
import json
from copy import copy

settings_desc_text = {
    'red_game': 'RED GAME',
    'yellow_game': 'YLW GAME',
    'timeout': 'TIMEOUT',
    'do_hi_scores': 'HI SCORES',
    'erase_hi_scores': 'ERASE SCORES',
    #'show_ball_scores': 'BALL SCORE'
}

settings_type = {
    'red_game': 'game',
    'yellow_game': 'game',
    'timeout': 'timeout',
    'do_hi_scores': 'boolean',
    'erase_hi_scores': 'boolean',
    #'show_ball_scores': 'boolean'
}

k = [
    'red_game',
    'yellow_game',
    'timeout',
    'do_hi_scores',
    'erase_hi_scores',
    #'show_ball_scores'
]

n = len(k)

times = [30,45,60,75,90,9999]

class ConfigMenu():

    def __init__(self,panel,sensor,game_list):
        self.panel = panel
        self.sensor = sensor
        self.game_list = game_list
        self.game_names = [g.name for g in self.game_list]
        self.settings = {
            'red_game': 'BASIC',
            'yellow_game': 'TARGET',
            'timeout': 60,
            'do_hi_scores': True,
            'erase_hi_scores': False
        }
        try:
            #make temp_settings so if it fails we can just copy
            #the default settings to file
            temp_settings = copy(self.settings)
            with open('config.json','r') as config_json_file:
                config_json = json.load(config_json_file)
                for key,value in config_json.items():
                    if key not in k:
                        raise ValueError("That's not a proper setting! {}: {}".format(key,value))
                    if settings_type[key] == 'boolean' and type(value) != type(bool()):
                        raise ValueError("That's not a proper value! {}: {}".format(key,value))
                    if settings_type[key] == 'timeout' and value not in times:
                        raise ValueError("That's not a proper value! {}: {}".format(key,value))
                    if settings_type[key] == 'game' and value not in self.game_names:
                        raise ValueError("That's not a proper value! {}: {}".format(key,value))
                    temp_settings[key] = value
            self.settings = temp_settings
        except Exception as e:
            print(type(e))
            print(e)
            print('json is busted, using default settings')
            with open('config.json','w') as config_json_file:
                json.dump(self.settings,config_json_file)


    def main_loop(self):
        self.cur_loc = 0
        while True:
            self.display()
            self.sensor.update_buttons()
            if self.sensor.is_pressed(BUTTON['START']):
                if self.cur_loc == n:
                    break
                key = k[self.cur_loc]
                if settings_type[key] == 'boolean':
                    self.settings[key] = not(self.settings[key])
                if settings_type[key] == 'game':
                    spot = self.game_names.index(self.settings[key])
                    spot = (spot + 1) % len(self.game_names)
                    self.settings[key] = self.game_names[spot]
                if settings_type[key] == 'timeout':
                    spot = times.index(self.settings[key])
                    spot = (spot + 1) % len(times)
                    self.settings[key] = times[spot]
            if self.sensor.is_pressed(BUTTON['SELECT']):
                self.cur_loc = (self.cur_loc+1)%(n+1)
            time.sleep(.05)
        if self.settings['erase_hi_scores']:
            for game in self.game_list:
                game.load_hi_scores(erase=True)
            self.settings['erase_hi_scores'] = False
            self.panel.draw.text((50,15+8*n), 'ERASED!',font=FONTS['Small'],fill=(255,0,0))
            self.panel.update()
            time.sleep(1.5)

        with open('config.json','w') as config_json_file:
            json.dump(self.settings,config_json_file)


    def display(self):
        self.panel.clear()
        self.panel.draw.text((8,1), 'SKEE-BALL CONFIG',font=FONTS['Small'],fill=(255,255,255))

        for i,key in enumerate(k):
            if settings_type[key] == 'boolean':
                setting_text = 'YES' if self.settings[key] else 'NO'
            else:
                setting_text = 'NONE' if self.settings[key] == 9999 else str(self.settings[key])
            alltext = '{}: {}'.format(settings_desc_text[key],setting_text)
            self.panel.draw.text((6,12+8*i), alltext,font=FONTS['Small'],fill=(255,255,255))

        self.panel.draw.text((6,15+8*n), 'EXIT',font=FONTS['Small'],fill=(255,255,255))

        y = 15+8*self.cur_loc if self.cur_loc == n else 12+8*self.cur_loc
        self.panel.draw.text((0,y), '>',font=FONTS['Small'],fill=(255,255,255))

        self.panel.update()
        