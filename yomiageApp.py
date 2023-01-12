import argparse
import json
import os
import time

import eel 

import coeiroink
import scraping


class YomiageApp:
    def __init__(self, min_block_length, **kwargs):
        self.kwargs = kwargs

        self.html = 'index.html'

        self.setting_path =  os.path.join(os.path.dirname(__file__), 'yomiage.ini')
        self.setting = self.get_setting()

        self.sc = scraping.Scraping()
        
        self.url = self.setting['last_url']
        self.is_play = 0
        self.is_pause = 0


        self.player = coeiroink.Player(min_block_length = min_block_length)
        def player_finished_callback():
            if self.player.pretasks.is_empty() and self.setting['auto_next']:
                self.yomiage_next()
        self.player.callbacks['finished'] = player_finished_callback
        self.player.callbacks['taskchanged'] = lambda x:eel.text_update(self.get_playing_texts())()
        self.player.callbacks['taskadded'] = lambda :eel.text_update(self.get_playing_texts())()
        self.player.player_state['volumerate'] = self.setting['volume_rate']
    
    def get_setting(self):
        if os.path.exists(self.setting_path):
            with open(self.setting_path) as f:
                setting = json.load(f)
        else:
            setting = {
                    'last_url':'',
                    'auto_next':True,
                    'volume_rate':0.5,
                    'speaker_id':0,
                }

        return setting
    
    def save_setting(self,setting = {},**kwargs):
        self.setting.update(**setting,**kwargs)
        print('savesetting : ',self.setting)
        with open(self.setting_path, 'wt') as f:
            json.dump(self.setting, f)


    def get_playing_texts(self,):
        if self.player.tasks.prev:
            return {
                        'prev_texts':[task.text for task in list(self.player.tasks.prev)[:-1]],
                        'playing_text':self.player.tasks.prev[-1].text,
                        'next_texts':[task.text for task in self.player.tasks.queue],
                        'pre_texts':[task.text for task in self.player.pretasks.queue],
                    }
        else:
            return {
                        'prev_texts':[],
                        'playing_text':'get_voice...',
                        'next_texts':[task.text for task in self.player.tasks.queue],
                        'pre_texts':[task.text for task in self.player.pretasks.queue],
                    }
    
    def yomiage_url(self,url,speaker_id = None):
        self.url = url
        try:
            text = self.sc.get_texts(url,'get_texts')
        except:
            text = '読み上げを終了します。'
        self.player.tasks_initialize()
        speaker_id = speaker_id if speaker_id is not None else self.setting['speaker_id']
        self.player.add_text(text,speaker_id = speaker_id)
    
    def yomiage_next(self,speaker_id = None):
        urls = self.sc.get_urls(self.url, 'get_next_url')
        if urls:
            time.sleep(1)
            self.yomiage_url(urls[0][1],speaker_id = speaker_id)
            eel.request_target_url_update()()
        else:
            self.player.add_text('読み上げを終了します')

    def run(self):
        @eel.expose
        def print_eel(*args,**kwargs):
            print(*args,**kwargs)

        @eel.expose
        def get_url():
            return self.url

        @eel.expose
        def set_url(url):
            self.url = url
            self.save_setting(last_url = self.url)
            print(url)
            return self.sc.get_selectors(self.url)

        @eel.expose
        def get_is_play():
            return self.is_play

        @eel.expose
        def set_is_play(logit):
            self.is_play = logit

        @eel.expose
        def get_volume_rate():
            return self.player.player_state['volumerate']

        @eel.expose
        def set_volume_rate(value):
            self.player.player_state['volumerate'] = value
            self.save_setting(volume_rate = value)

        @eel.expose
        def get_is_pause():
            return self.is_pause

        @eel.expose
        def set_is_pause(logit):
            self.is_pause = logit

        @eel.expose
        def set_texts_selector(selector):
            self.sc.set_selectors(self.url,{'get_texts':selector})

        @eel.expose
        def text_example():
            return self.sc.get_texts(self.url,'get_texts')[:50]+'...'

        @eel.expose
        def set_next_url_selector(selector):
            self.sc.set_selectors(self.url,{'get_next_url':selector})

        @eel.expose
        def next_url_example():
            r=self.sc.get_urls(self.url,'get_next_url')
            print(r)
            return r

        @eel.expose
        def toggle_pause():
            if self.player.flag['pause']:
                self.player.restart()
            else:
                self.player.pause()

        # @eel.expose
        # def get_auto_next():
        #     return self.auto_next

        # @eel.expose
        # def set_auto_next(logit):
        #     self.auto_next = logit
        #     self.save_setting(auto_next = self.auto_next)

        @eel.expose
        def get_setting():
            return dict(filter(lambda item: item[0] != 'last_url', self.setting.items()))

        @eel.expose
        def set_setting(setting):
            self.save_setting(**setting)

        @eel.expose
        def to_next():
            self.player.to_next(1)

        @eel.expose
        def to_prev():
            self.player.to_prev(1)

        @eel.expose
        def to_next_page():
            print('to_next_page')
            self.yomiage_next()

        @eel.expose
        def finish():
            self.player.tasks_initialize()
            self.player.pause()

        @eel.expose
        def yomiage_url_eel():
            self.yomiage_url(self.url,self.setting['speaker_id'])

        @eel.expose
        def yomiage_text(text):
            self.player.add_text(text)

        @eel.expose
        def request_text_update(text):
            eel.text_update(self.get_playing_texts())()

        @eel.expose
        def get_speakers():
            speakers = {'{}_{}'.format(speaker['name'],style['name']):style['id'] for speaker in coeiroink.get_requests('speakers') for style in speaker['styles']}
            return speakers


        eel.init("web")
        # eel.start("index.html",size=(1024, 768), port=8080, mode=None)
        eel.start("index.html",size=self.kwargs['window_size'], port=self.kwargs['port'], mode=self.kwargs['mode'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='add two integers')

    parser.add_argument('-b', '--min_block_length', type=int, default=200)
    parser.add_argument('-s', '--window_size', default=[768, 1024])
    parser.add_argument('-p', '--port', type=int, default=8000)
    parser.add_argument('-m', '--mode', default='chrome')
    
    app = YomiageApp(**vars(parser.parse_args()))
    app.run()