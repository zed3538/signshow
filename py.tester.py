from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(requests.get("https://learn.nzsl.nz/#/id/co-20").content, "html.parser")

videos = soup.find_all('video')
for video in videos:
    print(video.source['src'])