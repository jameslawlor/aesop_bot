from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import re

url = "http://www.azlyrics.com/a/aesoprock.html" 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

### Get list of songs
with requests.Session() as s:
    s.headers.update(headers)
    download = s.get(url)
    soup = BeautifulSoup(download.content, 'lxml')
    song_list = []
    for song in soup.findAll(target='_blank'):
        song_list.append(str(song.text))

# cast song names to lower case, remove whitespace
song_list = [re.sub(r'\W+', '', x.lower()) for x in lang]

# Create list of tuples of song name + song url
song_url = "http://www.azlyrics.com/lyrics/aesoprock/"
song_list = [(x,song_url + x + ".html") for x in song_list]

<<<<<<< HEAD
# iterate through song urls, write to text file ./lyrics/songname.txt
=======
# iterate through song urls, write to text file
>>>>>>> 7a2d221a7b0af188583c35d56089af77c49a9dd3
with requests.Session() as s:
    s.headers.update(headers)
    for song_name, song_url in song_list:
        download = s.get(song_url)
        site= BeautifulSoup(download.text,"html.parser")
        for lyrics in site.find_all("div", {"class":""}):
<<<<<<< HEAD
            with open("./lyrics/"+song_name+".txt","w") as fout:
=======
            with open(song_name+".txt","w") as fout:
>>>>>>> 7a2d221a7b0af188583c35d56089af77c49a9dd3
                fout.write(lyrics.text)
            time.sleep(np.random.uniform(low=10.0, high=20.0, size=None))
        print(song_name)
