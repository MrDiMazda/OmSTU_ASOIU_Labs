import Lab1

if __name__=="__main__":
    url = "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250"
    parsedPage = Lab1.GetParsedPage(url)
    topList = Lab1.GetFilmsNames(parsedPage)
    print(topList)