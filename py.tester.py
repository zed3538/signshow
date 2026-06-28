from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(requests.get("https://www.nzsl.nz/signs/search?tag=Actions+and+activities").content, "html.parser")

videos = soup.find_all('video')
for video in videos:
    print(video.source['src'])