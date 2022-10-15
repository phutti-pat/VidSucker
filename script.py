from ast import AsyncFor
from os import remove
import os
from queue import Empty
from urllib import response
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse
from pathlib import Path
import re
import asyncio
import aiohttp  # pip install aiohttp
import aiofiles  # pip install aiofiles

class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.read_file()
            
        
    def read_file(self):
        self.file = open(self.filename)
        self.file_content = self.file.read()
        return self, self.file, self.file_content
        
    def get_items(self, split=""):
        if split == "":
            return self.file_content.splitlines
        else:
            return self.file_content.split(split)
    
    def remove_downloaded_link(self, link):
        file, content = self.read_file()
        content.replace(link, "")
        file.writelines(self.file_content)
        file.close()
        print("Removed link %s" % link)

        
    
class VidSucker:
    # LinkContent = tuple[VidSucker@self, str, str]
    
    def __init__(self, link, download="results/"):
        self.link = link
        self.download = download
        Path(self.download).mkdir(parents=True, exist_ok=True)
        # return self
        
    def get_link(self, url: str) -> tuple[self, str, str]:
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content,'html5lib')    
        self.vdo_name = self.soup.find('h1').string
        
        self.queries = self.soup.find_all('source',attrs={'type':re.compile("video")})
        
        found_links = [n['src'] for n in self.queries]
        for link in found_links:
            if link is not None: 
                if link.startswith("https:"):
                    if link.endswith(".mp4"):
                        if self.vdo_name is None:
                            self.vdo_name = link.split("/")[-1]
                        return self, self.vdo_name, link
                
        
        
    def get_vdo(self, name, url):
        print("================================================")
        self.folder_name = self.download
        self.r = requests.get(url,stream=True)
        self.save_file = self.folder_name + name + ".mp4"
        self.total_file_size = int(self.r.headers["Content-Length"])
        self.chunk_size = 1024
        with open(self.save_file, 'wb') as f:
            for chunk in tqdm(self.r.iter_content(chunk_size=self.chunk_size), total = self.total_file_size/ self.chunk_size, unit= 'KB'):
                if chunk:
                    f.write(chunk)
                    
        print("Downloaded" + name + "\nat:" + self.save_file)
        
    async def get_vdos(self, name, url):
            print("================================================")
            self.folder_name = self.download
            chunk_size = 1024
            sema = asyncio.BoundedSemaphore(5) # initial
            
            async with sema, aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    assert resp.status == 200
                    data = await resp.read()
                async with aiofiles.open(
                    os.path.join(self.folder_name, name), "wb"
                ) as outfile:
                    tqdm(data.iter_content(chunk_size=chunk_size), total = session.get('total') / chunk_size, unit="KB")
                    await outfile.write(data)
            
            self.r = requests.get(url,stream=True)
            self.save_file = self.folder_name + name + ".mp4"
            self.total_file_size = int(self.r.headers["Content-Length"])
            self.chunk_size = 1024
            with open(self.save_file, 'wb') as f:
                for chunk in tqdm(self.r.iter_content(chunk_size=self.chunk_size), total = self.total_file_size/ self.chunk_size, unit= 'KB'):
                    if chunk:
                        f.write(chunk)
                        
            print("Downloaded" + name + "\nat:" + self.save_file)
    
    
        
def main():
    download_path = "~/Downloaded/VidSucker/"
    file_name = "url.txt"#input("file name: ")
    file, filing, content = FileReader(file_name).read_file()
    links = file.get_items(split=" ")

    vids, names, urls = [VidSucker(link=n,download=download_path).get_link(url=n) for n in links]  # type: ignore
    
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(vid.get_vdos(name=name,url=url)) for (vid, name, url) in (vids, names, urls)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

main()