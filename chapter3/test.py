from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import datetime
import random
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

pages = set()
random.seed(datetime.datetime.now())

# 페이지에서 발견된 내부 링크를 모두 목록으로 만듭니다.
def getInternalLinks(bsObj: object, includeUrl: str) -> list:
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    # /로 시작하는 링크를 모두 찾습니다.
    for link in bsObj.findAll("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in internalLinks:
                if link.attrs["href"].startswith("/"):
                    internalLinks.append(includeUrl + link.attrs["href"])
                else:
                    internalLinks.append(link.attrs["href"])

    return internalLinks


# 페이지에서 발견된 외부 링크를 모두 목록으로 만듭니다.
def getExternalLinks(bsObj: object, excludeUrl: str) -> list:
    externalLinks = []
    # 현재 URL을 포함하지 않으면서 http나 www로 시작하는 링크를 모두 찾습니다.
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in externalLinks:
                externalLinks.append(link.attrs["href"])

    return externalLinks


def getRandomExternalLinks(startingPage: str) -> str:
    try:
        html = urlopen(startingPage)
    except HTTPError as e:
        # 응답에러 또는 access Deny처리된 경우 최초 startingSite 부터 재시작
        print("error :" + str(e))
        return getRandomExternalLinks(startingSite)

    bsObj = BeautifulSoup(html, "html.parser")
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        domain = urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        # 인터널링크가 없는경우가 있어서 방어 처리
        if len(internalLinks) == 0:
            return getRandomExternalLinks(startingSite)
        else:
            return getRandomExternalLinks(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite: str) -> None:
    externalLink = getRandomExternalLinks(startingSite)
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)


startingSite = "http://oreilly.com"
followExternalOnly(startingSite)
