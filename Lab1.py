import requests, pandas
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250"
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")
data = soup.find("tbody").findAll("tr")

toplist=[]

for tag in data:
    movie=tag.find("td",{"class":"titleColumn"}).find("a").text
    rating=tag.find("td",{"class":"ratingColumn imdbRating"}).find("strong").text
    toplist.append({"Title":movie,"Rating":rating})

print(toplist)