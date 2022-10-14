from os import remove
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse


class VidSucker:
    def __init__(self, link):
        # self.link = link
        self.get_link(link)
        
    def get_link(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html5lib')    
        name = soup.find('h1').string
        # vdo_url = soup.find('source')['src']
        vdo_url = soup.find('video').contents
        for v in vdo_url:
            if v.string is not None:
                print("SKIPPPPP...")
                continue
            if urlparse(v['src']) and v['src'].endswith(".mp4"):
                link = v['src']
                if name == None:
                    name = link.split('/')[-1]
                    name = name.replace('.mp4.mp4', '.mp4')
                print("///////" + link)
                print("FOUND URL: " + link)
                print("================================================")
                print("name: " + name)
                print("at: " + link) 
                self.get_vdo(name, link)
                print("================================================")
        
        
    def get_vdo(self, name, url):
        folder_name = "results/"
        r = requests.get(url,stream=True)
        save_file = folder_name + name + ".mp4"
        total_file_size = int(r.headers["Content-Length"])
        chunk_size = 1024
        with open(save_file, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total = total_file_size/ chunk_size, unit= 'KB'):
                if chunk:
                    f.write(chunk)
                    
        print("Downloaded" + name + "\nat:" + save_file)
        self.remove_link(url)
    
    def remove_link(self, url):
        url_list = open(file_name,"w")
        url_content = url_list.read()
        url_content.replace(file_name, "")
        url_list.writelines(url_content)
        url_list.close()
        print("Removed" + file_name + "\nat:" + url_content)
        print("================================================================")
        
        
file_name = input("file name: ")
f = open(file_name)
links = f.read().split(" ")
for link in links:
    print("Download link: " + link)
    VidSucker(link)
    
print("VidSucker finished\n" + links.join("\n"))
