import requests
from bs4 import BeautifulSoup

def GetParsedPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def GetFilmsNames(soup):
    data = soup.find("tbody").findAll("tr")
    toplist=[]
    for tag in data:
        movie=tag.find("td",{"class":"titleColumn"}).find("a").text
        rating=tag.find("td",{"class":"ratingColumn imdbRating"}).find("strong").text
        toplist.append({"Title":movie,"Rating":rating})
    
    return toplist