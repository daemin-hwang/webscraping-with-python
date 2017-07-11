import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tinydb import TinyDB, where
import datetime
import uuid
import re

current_dir = os.getcwd()

db = TinyDB(current_dir + "/db.json")
pages_table = db.table("pages")
links_table = db.table("links")


def genId() -> str:
    return str(uuid.uuid4())


def datetimeStr() -> str:
    return str(datetime.datetime.now())


def insertPageIfNotExists(pageUrl: str) -> str:
    pages = pages_table.search(where("url") == pageUrl)
    if len(pages) == 0:
        pageId = genId()
        pages_table.insert({"pageId": pageId, "url": pageUrl, "created": datetimeStr()})
        return pageId

    return pages[0]["pageId"]


def insertLink(fromPageId: str, toPageId: str) -> None:
    links = links_table.search((where("fromPageId") == fromPageId) & (where("toPageId") == toPageId))

    if len(links) == 0:
        linkId = genId()
        links_table.insert({"linkId": linkId, "fromPageId": fromPageId, "toPageId": toPageId, "created": datetimeStr()})


def isPageScraped(url: str) -> bool:
    pages = pages_table.search(where("url") == url)
    if len(pages) == 0:
        return False

    pageId = pages[0]["pageId"]
    links = links_table.search(where("fromPageId") == pageId)
    if len(links) == 0:
        return False

    return True


def getLinks(pageUrl: str, recursionLevel: int) -> None:
    if recursionLevel > 4:
        return

    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen("http://en.wikipedia.org" + pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        linkSrc = link.attrs["href"]
        insertLink(pageId, insertPageIfNotExists(linkSrc))
        if not isPageScraped(linkSrc):
            # 새 페이지를 만났으니 추가 하고 링크를 검색합니다.
            newPage = linkSrc
            print(newPage)
            getLinks(newPage, recursionLevel + 1)
        else:
            print("skip:" + str(linkSrc) + "found on " + pageUrl)


getLinks("/wiki/Kevin_Bacon", 0)