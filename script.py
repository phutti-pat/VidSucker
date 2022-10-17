from curses import echo
from fileinput import filename
from multiprocessing.resource_sharer import stop
import pdb
from os import remove
import os
from queue import Empty
from turtle import down
from unicodedata import name
from urllib import response
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse
from pathlib import Path
import re
from aiohttp import web 
import asyncio
import aiofiles
from asyncinit import asyncinit

@asyncinit
class FileReader(object):
    async def __init__(self, filename, type: str):
        self.file = await open(self.filename, self.type)
        self.filename = filename
        self.type = type
        
    async def _file(data):
        async with asyncio.open(self.filename, mode='a') as fp:
            fp.read(data)
            return data
        
    async def read_file(self):
        
        if self.type == 'w':
            return self
            pass
        
        self.file_content = self.file.read()
        print("********************************\n" + self.filename + "\n********************************\n" + self.file_content + "****************************************************************")
        self.file.close()
        return self
        
    async def get_items(self, split=" "):
        if self.type == 'w':
            pass
        return self.file_content.split(split)
        
    async def update_item(self, link, url):
        write = open(self.filename, 'w')
        read = open(self.filename, 'r').read()
        write.writelines(read.replace(link, link + "||" + url))
        print("Updated file")
        write.close()
        
    # def remove_downloaded_link(self, link):
    #     if self.type != 'w':
    #         pass
    #     file = self.read_file(type='w')
    #     content = file.file_content
    #     content.replace(link, "")
    #     file.writelines(self.file_content)
    #     file.close()
    #     print("Removed link %s" % link)

        
    
@asyncinit
class VidSucker:

    vdo_link = ""
    async def __init__(self, link, download="results/"):
        self.link = link
        self.download = download
        print("Initialized %s" % self.link)
        Path(self.download).mkdir(parents=True, exist_ok=True)
        
        
    async def get_link(self):
        print("Getting link %s" % self.link)
        self.response = requests.get(self.link)
        self.soup = BeautifulSoup(self.response.content,'html5lib')    

        self.vdo_name = self.soup.select('title')[0].text.__add__(".mp4").lower().replace(' ','_')
        if self.vdo_name is None:
            self.vdo_name = self.link.split("/")[-2].__add__(".mp4").lower().replace(' ','_')
        print("####" + self.vdo_name + " #####")
        
        print("Extracting vdo resource url")
        self.queries = self.soup.find_all('source',attrs={'type':re.compile("video")})
        
        found_links = [n['src'] for n in self.queries]
        for link in found_links:
            if link is not None: 
                if link.startswith("https:"):
                    if link.endswith(".mp4"):
                        self.vdo_link = link
                        print("####FOUND IT####\n" + self.vdo_link + "\n#####********************************")
                        return self
        
        
    # def get_vdo(self, name, url):
    #     print("================================================")
    #     self.folder_name = self.download
    #     self.r = requests.get(url,stream=True)
    #     self.save_file = self.folder_name + name + ".mp4"
    #     self.total_file_size = int(self.r.headers["Content-Length"])
    #     self.chunk_size = 1024
    #     with open(self.save_file, 'wb') as f:
    #         for chunk in tqdm(self.r.iter_content(chunk_size=self.chunk_size), total = self.total_file_size/ self.chunk_size, unit= 'KB'):
    #             if chunk:
    #                 f.write(chunk)
                    
    #     print("Downloaded" + name + "\nat:" + self.save_file)
        
    async def download_vid(self):
        print("================================================")
        self.folder_name = self.download
        chunk_size = 1024
        sema = asyncio.BoundedSemaphore(5) # initial

        async with sema, web.ClientSession() as session:
            async with session.get(self.vdo_link) as resp:
                assert resp.status == 200
                data = await resp.read()
            async with aiofiles.open(
                os.path.join(self.folder_name, self.vdo_name), "wb"
            ) as outfile:
                data = tqdm(outfile.raw, total=resp.header.size / chunk_size, unit="KB")
                await outfile.write(data)
        
        # self.r = requests.get(url,stream=True)
        # self.save_file = self.folder_name + name + ".mp4"
        # self.total_file_size = int(self.r.headers["Content-Length"])
        # self.chunk_size = 1024
        # with open(self.save_file, 'wb') as f:
        #     for chunk in tqdm(self.iter_content(chunk_size=self.chunk_size), total = self.total_file_size/ self.chunk_size, unit= 'KB'):
        #         if chunk:
        #             f.write(chunk)
                    
        # print("Downloaded" + name + "\nat:" + self.save_file)
    
        
async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(inside_main())
    
    async def inside_main():
        download_path = "/Users/PPath/Downloaded/VidSucker/"
        file_name = "url2.txt"#input("file name: ")
        read_file = await FileReader(file_name, 'r').read_file()
        write_file = await FileReader(file_name,'w')
        links = await read_file.get_items()
    
    
    pass
    asyncio.run_coroutine_threadsafe(start_loop(links=links), loop=self.loop)
    
    async with read_all_file as files:
        assert read_file is not None
        with read_file.get_items() as links:
            assert links is not None
            await create_vid(link=links)

    await create_vid(link) as links:
        assert links is not None
        with await VidSucker(link=link,download=download_path) as vid:
            assert vid is not None
            with await vid.get_link() as link:
                assert link is not None
                
    await VidSucker(download=download_path) as links:
        
            
    async def start_loop(links: list[str]):
        [await read_all_filezzzx(link=n) for n in links]
            
asyncio.run(main())