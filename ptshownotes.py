import re
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

def clean_line(line):
    return str().join(c for c in line if ord(c) < 128)


class shownotes():

    def sn(self, chat):
        self.scrape(self.lnk_detect(chat))
        return self.org()

    def __init__(self, text):
        self.key = '#uncategorized'
        self.rdict = defaultdict(list)
        self.bad_links = list()
        self.md_text = self.sn(text)

    def lnk_detect(self, chat):
        return re.findall(r'^#.*|\b\S+\.\S+', chat, re.M)
    
    def scrape(self, rlist):
        for line in rlist:
            nline = line.strip()
        
            if nline.startswith('#'):
                self.key = nline
                continue
            
            if not nline.startswith('http'):
                    nline = 'http://' + nline
                    
            try:
                web = requests.get(nline, timeout = 2.0)
                soup = BeautifulSoup(web.content)
                rtitle = clean_line(soup.title.text)
                if (rtitle, nline) not in self.rdict[self.key]:
                    self.rdict[self.key].append((rtitle, nline))

            except:
                nline = clean_line(nline)
                print(nline, 'failed')
                self.bad_links.append(nline)
        
    def org(self):
        rstr = str()
        for key in self.rdict:
            if key == 'bad links':
                continue
            rstr = rstr + '#{}\n'.format(key)
            
            for item in self.rdict[key]:
                rstr = rstr + '* [{}]({})\n'.format(item[0],item[1])
        
        return rstr


