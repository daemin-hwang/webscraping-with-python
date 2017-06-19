from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


def getBsObj(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
    except AttributeError as e:
        print(e)
    return bsObj


bsObj = getBsObj("http://www.pythonscraping.com/pages/page3.html")

if bsObj == None:
    print("not found DOM")

imgs = bsObj.findAll("img", {"src": re.compile("\.\.\/img\/gifts\/img.*\.jpg")})


for img in imgs:
    print(img.get("src"))




