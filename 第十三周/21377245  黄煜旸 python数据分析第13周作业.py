import asyncio
import aiofiles
from lxml import etree
import aiohttp
import re
import random
import time
from yarl import URL


class VoaCrawler():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    
    async def GetUrlList(self,queue):
            async with aiohttp.ClientSession() as session:
                async with session.get(url='https://www.51voa.com/VOA_Standard_3.html', headers=self.headers) as r:
                    html=etree.HTML(await r.text(errors='ignore'))
                    for j in range(0,50):
                        await queue.put(html.xpath('//*[@id="righter"]/div[3]/ul/li[%s]/a/@href'%str(j)))


    async def GetUrl(self,queue,queue1):
        while True:
            link=''.join(await queue.get())
            if link is None:
                break
            url = URL('https://www.51voa.com'+link,encoded=True)
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=self.headers) as r:
                    mp3_links = list(set(re.findall(r'https://.+?\.mp3', await r.text(errors='ignore'))))
                    for mp3_link in mp3_links:
                        await queue1.put(mp3_link)

    async def Download(self,queue1):
        while True:
            link=await queue1.get()
            if link is None:
                break
            print(link)
            async with aiohttp.ClientSession() as session:
                    async with session.get(url=link) as r:
                        fname = link[link.rfind('/') + 1:]
                        async with aiofiles.open(fname, 'wb') as f:
                            while True:
                                chunk = await r.content.read(1024)
                                if not chunk:
                                    break
                                await f.write(chunk)

    def aio_main(self):
        loop = asyncio.get_event_loop()
        queue=asyncio.Queue()
        queue1=asyncio.Queue()
        task1=loop.create_task(self.GetUrlList(queue))
        task2=loop.create_task(self.GetUrl(queue,queue1))
        task3=loop.create_task(self.Download(queue1))
        tasks=asyncio.gather(task1,task2,task3)
        loop.run_until_complete(tasks)
        loop.close()
        
    def run(self):
        self.aio_main()


if __name__ == '__main__':
    VoaCrawler().run()