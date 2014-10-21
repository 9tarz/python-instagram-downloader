import requests
from bs4 import BeautifulSoup
import sys 
import re
import os
from Queue import Queue
from threading import Thread

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(directory+"/"+local_filename, 'wb') as f:
        for chunk in r.iter_content(1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

class MyThread(Thread):
    def __init__(self, url):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.url = url
 
    def run(self):
        download_file(self.url)

class UrlRequest:
    def __init__(self,request_url):
        import requests
        try:
            r = requests.get(request_url)
            r.raise_for_status()
        except:
            print 'URL : ' + sys.argv[1] + ' doesn\'t exists'
            raise sys.exit()
        self.text = r.text

url = "http://web.stagram.com/n/" + sys.argv[1]
directory = sys.argv[1]
if not os.path.exists(directory):
    os.makedirs(directory)
r = UrlRequest(url)
chk = True
while (chk) :
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('img'):
        #print "loop1"
        img_url = link.get('src')
        #print img_url
        if img_url and( "_6.jpg" in img_url and "scontent" in img_url):
            img_url = img_url.replace("_6.jpg", "_7.jpg")
            print img_url
            MyThread(img_url).start()
        elif img_url and ("_a.jpg" in img_url and "scontent"in img_url):
            img_url = img_url.replace("_a.jpg", "_b.jpg")
            print img_url
            MyThread(img_url).start()
    
    for link in soup.find_all('a'):
        #print "loop2"
        next_page = link.get('href')
        
        if next_page and "?npk=" in next_page:
            url = "http://web.stagram.com" + next_page
            print "-----------------------------------------------------------------"
            print url
            chk = True
            r = UrlRequest(url)
            break
        chk = False
