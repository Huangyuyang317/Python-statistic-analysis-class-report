from threading import Thread
import requests
from tqdm import tqdm
from lxml import etree
import re
import librosa
from queue import Queue

class GetUrlList(Thread):
    def __init__(self,num,queue):
        Thread.__init__(self)
        self.num=num
        self.queue=queue
    def run(self):
        url = f'https://www.51voa.com/VOA_Standard_{self.num}.html'
        response=requests.get(url).text
        html=etree.HTML(response)
        for j in range(0,50):
            self.queue.put(html.xpath('//*[@id="righter"]/div[3]/ul/li[%s]/a/@href'%str(j)))

class GetUrl(Thread):
    def __init__(self,queue,queue1):
        Thread.__init__(self)
        self.queue=queue
        self.queue1=queue1
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    def run(self):
        while True:
            link=''.join(self.queue.get())
            if link is None:
                break
            url = 'https://www.51voa.com'+link
            response = requests.get(url,headers = self.headers)
            self.queue1.put(list(set(re.findall(r'https://.+?\.mp3', response.text))))

class Download(Thread):
    def __init__(self,queue,queue1):
        super().__init__()
        Thread.__init__(self)
        self.queue=queue
        self.queue1=queue1
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    def run(self):
         while True:
            link=''.join(self.queue.get())
            if link is None:
                break
            mp3_stream = requests.get(link,headers = self.headers).content
            fname = link[link.rfind('/')+1:]
            with open(fname,'wb') as f:
                f.write(mp3_stream)
            self.queue1.put(fname)

class SpeechRate(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue=queue
    def run(self):
            while True:
                filename=self.queue.get()
                if filename is None:
                    break
                y, sr = librosa.load(filename, sr = None)
                onsets = librosa.onset.onset_detect(y=y,sr=sr,units="time",hop_length=128,backtrack=False) 
                number_of_words = len(onsets)
                duration = len(y)/sr
                words_per_second = number_of_words/duration
                print(f'{filename}  words-per-second: {words_per_second}\nduration: {duration} seconds\nnumber-of-words: {number_of_words}')

if __name__=='__main__':
    list_queue=Queue()
    url_queue=Queue()
    download_queue=Queue()

    list_threads = [GetUrlList(str(i),list_queue) for i in range(3, 5)]
    url_threads = [GetUrl(list_queue, url_queue) for _ in range(4)]
    download_threads = [Download(url_queue, download_queue) for _ in range(8)]
    speech_thread = SpeechRate(download_queue)

    for thread in list_threads + url_threads+ download_threads + [speech_thread]:
        thread.start()
    
    for thread in list_threads + url_threads + download_threads:
        thread.join()

    download_queue.put(None)
    speech_thread.join()