import sys
import requests
import os
import json
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def get_url_setting(setting,url):
    parse = urlparse(url)
    domain = parse.netloc
    paths  = parse.path.strip('/').split('/')
    parse = [domain]+paths
    value = {
            'selectors' :{
                'get_texts' : 'body',
                'get_urls'  : 'body',
            },
        }
    exist = False
    for key in parse:
        if 'pages' in setting.keys() and key in setting['pages'].keys():
            value = setting['pages'][key]
            exist = True
            setting = value
        else:
            break
    return value, exist

def set_url_setting(setting,url,set_selectors):
    parse = urlparse(url)
    domain = parse.netloc
    paths  = parse.path.strip('/').split('/')
    parse = [domain]+paths
    root = setting
    for key in parse:
        if 'pages' not in setting.keys() or not isinstance(setting['pages'],dict):
            setting['pages'] = {}
        pages = setting['pages']  
        if key not in pages.keys() or not isinstance(pages[key],dict):
            pages[key] = {}
        setting = pages[key]
        if 'selectors' not in setting.keys() or not isinstance(setting['selectors'],dict):
            setting['selectors'] = {}
        selectors = setting['selectors']
        selectors.update(set_selectors)
    return root
    
    

class Scraping:
    def __init__(self):
        self.setting_name = 'scraping.json'
        self.setting_path = os.path.join(os.path.dirname(__file__), self.setting_name)
        if os.path.exists(self.setting_path):
            with open(self.setting_path) as f:
                self.setting = json.load(f)
            
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def save_setting(self):
        with open(self.setting_path, 'wt') as f:
            json.dump(self.setting, f)    
    
    def get_selectors(self,url):
        setting,e=get_url_setting(self.setting,url)
        return setting['selectors']
    
    def set_selectors(self,url,selectors):
        set_url_setting(self.setting,url,selectors)
        self.save_setting()

    def get_html(self, url, **params):
        r = self.session.get(url,headers=self.headers,params=params)
        html = BeautifulSoup(r.text, 'html.parser')
        return html

    def get_texts(self, url, selector = 'get_texts'):
        
        setting,e=get_url_setting(self.setting,url)
        if e and selector is None :
            selector='body'
        else:
            selector=setting['selectors'][selector] if selector in setting['selectors'].keys() else selector
        html = self.get_html(url)
        return '\t'.join([e.get_text() for e in html.select(selector)]).strip()
    
    def get_urls(self, url, selector = 'get_urls'):
        
        setting,e=get_url_setting(self.setting,url)
        if e and selector is None :
            selector='body'
        else:
            selector=setting['selectors'][selector] if selector in setting['selectors'].keys() else selector
        html = self.get_html(url)
        texts = [e.get_text() for e in html.select(selector)]
        urls = [urljoin(url,e.get('href')) for e in html.select(selector)]
        # texts = [[ee.get_text() for ee in e.find_all(href=True)] for e in html.select(selector)]
        # urls = [[urljoin(url,ee['href']) for ee in e.find_all(href=True)] for e in html.select(selector)]
        # texts = sum(texts,[])
        # urls = sum(urls,[])
        return list(zip(texts,urls))


if __name__ == '__main__':
    
    target_url = 'https://ncode.syosetu.com/n9418eg/1/' if len(sys.argv) == 1 else sys.argv[1]
    text = Scraping().get_urls(target_url,'get_urls')

    print(text)