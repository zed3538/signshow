from bs4 import BeautifulSoup
import requests

url = "https://www.nzsl.nz/signs/search?tag=Actions+and+activities"
req = requests.get(url)

soup = BeautifulSoup(req.content, "html.parser")

print(soup.title.prettify())