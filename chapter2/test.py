import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")
images = bsObj.findAll("img", {"src": re.compile("\.\.\/img\/gifts/img.*\.jpg")})

for img in images:
    print(img.get("src"))

twoAttrTags = bsObj.findAll(lambda tag: len(tag.attrs) == 2)
for tag in twoAttrTags:
    print(tag)





