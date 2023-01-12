import json
import time
import requests
import threading
import io
import wave
from collections import deque

import numpy as np
import pyaudio

def get_urls(baseurl = 'http://localhost:50031/'):
    apis = [
        'core_versions',
        'audio_query',
        'accent_phrases',
        'synthesis',
        'presets',
        'speakers'
    ]
    return {api : baseurl + api for api in apis}

urls = get_urls()
# headers = {'speaker':1}
def get_core_veraions():

    response = requests.get(urls['core_versions'])
    return response.json()
CORE_VERSIONS = get_core_veraions()




def get_requests(api,**params):
   response = requests.get(urls[api], params = params)
   return response.json()

def get_audio_query(text, speaker_id = 1, core_version = '0.0.0'):
    params = {'text' :text,'speaker' :speaker_id, 'core_version':core_version}
    response = requests.post(urls['audio_query'], params = params)
    res_data = response.json()
    # print(res_data)
    # print(response.status_code)
    return res_data
 

def synthesis(query, speaker_id =3, core_version = '0.0.0'):
    params = {'speaker' :speaker_id, 'core_version':core_version, 'enable_interrogative_upspeak' : 'true'}
    response = requests.post(urls['synthesis'],params = params,data= json.dumps(query))
    # with open(voice_pass, 'wb') as saved_voice:
    #     print(response.content[:100])
    #     saved_voice.write(response.content)
    #     # print('type: ', type(wf))
    print(response.status_code)
    if response.status_code == 500:
        print(urls['synthesis'])
        print(params)
        print(response.content)
    return response.content


def get_voice(text, speaker_id = 1, speedScale = 1, volumeScale = 1):
    q = get_audio_query(text, speaker_id, CORE_VERSIONS)
    q['speedScale'] = speedScale
    q['volumeScale'] = volumeScale
    bytes = synthesis(q, speaker_id, CORE_VERSIONS)
    return bytes

class Task:
    def __init__(self, text, bytes = None, speaker_id = 0, speedScale = 1, volumeScale = 1):
        self.text = text
        self.bytes = bytes
        self.speaker_id = speaker_id
        self.speedScale = speedScale
        self.volumeScale = volumeScale

class Task_queue:
    def __init__(self,tasks = [],max_prev = 100):
        self.queue = deque(tasks)
        self.prev = deque([],maxlen=max_prev)

    def clear(self):
        self.queue.clear()
        self.prev.clear()

    def pop(self):
        task = self.queue.popleft()
        self.prev.append(task)
        return task
    
    def append(self,*args, **kwargs):
        # print(args)
        if isinstance(args[0],Task):
            self.queue.append(args[0])
        else:
            self.queue.append(Task(*args, **kwargs))
    
    def is_empty(self):
        return not self.queue
    
    def to_next(self,n):
        for _ in range(n-1):
            task = self.queue.popleft()
            self.prev.append(task)
    
    def to_prev(self,n):
        for _ in range(n+1):
            task = self.prev.pop()
            self.queue.appendleft(task)
    
    def check_to_next(self,n):
        return len(self.queue) >= n
    
    def check_to_prev(self,n):
        return len(self.prev) >= n+2
    
    def __len__(self):
        return len(self.queue)
    
def wait_for(f):
    while not f():
        time.sleep(0.5)

def play_bytes(tasks,flag, state, callbacks):
    print('player_thread started')
    
    while not flag['end']:
        wait_for(lambda: not tasks.is_empty())
        print('playing...')
        task = tasks.pop()
        state['task'] = task
        state['finished'] = False
        flag['refresh'] = False
        if callbacks['taskchanged'] is not None:callbacks['taskchanged'](task)
        
        bytes = task.bytes
        print(task.text)
        wf = wave.open(io.BytesIO(bytes), mode='rb')
        if wf.getsampwidth() == 2: # 16-bit PCM
            datatype = np.int16
        elif wf.getsampwidth() == 4: # 32-bit float
            datatype = np.float32

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True) 

        chunk = 1024 # チャンク単位でストリームに出力し音声を再生
        wf.rewind() # ポインタを先頭にする
        
        data = wf.readframes(chunk)
        while data:
            if flag['pause']:
                wait_for(lambda: not flag['pause'])
            if flag['end']:
                break
            if flag['refresh']:
                break
            stream.write((np.frombuffer(data, dtype=datatype)*float(state['volumerate'])).astype(datatype).tobytes())
            state['progress'] = wf.tell() / wf.getnframes()
            if callbacks['progress'] is not None:callbacks['progress'](state['progress'])
            data = wf.readframes(chunk)
            
        stream.close()
        p.terminate()
        state['task'] = None
        state['finished'] = True
        if tasks.is_empty() and callbacks['finished'] is not None:callbacks['finished']()


def get_bytes(tasks,result,flag,callbacks):
    print('voice_thread started')
    
    while not flag['end']:
        wait_for(lambda: not flag['pause'])
        if tasks.is_empty():wait_for(lambda: not tasks.is_empty())
        print('get_voice...')
        task = tasks.pop()
        task.bytes = get_voice(task.text, task.speaker_id, task.speedScale, task.volumeScale)
        result.append(task)
        if callbacks['taskadded'] is not None:callbacks['taskadded']()

class Player:
    def __init__(self, min_block_length = 200, callbacks={}):
        self.min_block_length = min_block_length

        self.tasks = Task_queue()
        self.pretasks = Task_queue()
        
        self.flag = {
            'pause' : False,
            'end'   : False,
            'refresh'   : False,
        }
        self.player_state = {
            'finished' : False,
            'task'     : None,
            'progress' : 0,
            'volumerate':0.5,
        }
        self.callbacks = {
            'finished' : None,
            'taskchanged' : None,
            'progress' : None,
            'taskadded' : None,
        }
        self.callbacks.update(callbacks)

        self.player_thread = threading.Thread(target=play_bytes, args=(self.tasks, self.flag, self.player_state, self.callbacks), name='player_thread', daemon=True)
        self.player_thread.start()
        self.coeiro_thread = threading.Thread(target=get_bytes, args=(self.pretasks, self.tasks, self.flag, self.callbacks), name='coeiro_thread', daemon=True)
        self.coeiro_thread.start()
    
    def tasks_initialize(self):
        self.tasks.clear()
        self.pretasks.clear()

        self.flag.update({
            'pause' : False,
            'end'   : False,
            'refresh'   : True,
        })
        self.player_state.update({
            'finished' : False,
            'task'     : None,
            'progress' : 0,
        })


    def end(self):
        self.flag['end'] = True
        self.player_thread.join()
        self.coeiro_thread.join()
    
    def pause(self):
        self.flag['pause'] = True
    
    def restart(self):
        self.flag['pause'] = False

    def to_next(self,n):
        self.refresh()
        self.tasks.to_next(n)
    
    def to_prev(self,n):
        self.refresh()
        self.tasks.to_prev(n)
    
    def refresh(self):
        self.flag['refresh'] = True
    
    def is_pause(self):
        return self.flag['pause']
    
    def add_task(self, *args, **kwargs):
        self.pretasks.append(*args, **kwargs)
    
    def add_tasks(self, tasks):
        for task in tasks:
            self.pretasks.append(task)

    def add_text(self, text, *args, **kwargs):
        while text:
            # if len(text) == 0:break
            n = text.find('\n',self.min_block_length)+1 
            n = n if n < 500 else 500
            n = n if n > 0 else len(text)
            
            self.add_task(text[:n], *args, **kwargs)
            if self.callbacks['taskadded'] is not None:self.callbacks['taskadded']()
            text = text[n:]


if __name__ == "__main__":
    print(get_requests('speakers'))