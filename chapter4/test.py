from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re
import datetime
import random
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

random.seed(datetime.datetime.now())


def getLinks(articleUrl: str) -> list:
    url = "http://en.wikipedia.org" + articleUrl
    print("[url] : " + url)
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))


def getHistoryIps(pageUrl: str) -> set:
    # 개정 내역 페이지 URL은 다음과 같은 형식입니다.
    # http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="
    historyUrl += pageUrl + "&action=history"
    print("history url is :" + historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    # 사용자명 대신 IP주소가 담긴, 클래스가 mw-anonuserlink인 링크만 찾습니다.
    ipAddresses = bsObj.findAll("a", {"class": "mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList


def getCountry(ipAddress: str) -> str:
    url = "http://freegeoip.net/json/"
    url = url + ipAddress
    print("request country get url : " + url)
    try:
        response = urlopen(url, timeout=2).read().decode("utf-8")
    except HTTPError:
        return None
    except URLError:    # freegeoip 서버가 죽은 경우 타임아웃 2초에 대한 에러 방어 처리
        return None

    responseJson = json.loads(response)
    return responseJson.get("country_code")

links = getLinks("/wiki/Python_(programming_language)")

while len(links) > 0:
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIps(link.attrs["href"])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(historyIP + "is from" + country)

    newLink = links[random.randint(0, len(links)-1)].attrs["href"]
    links = getLinks(newLink)