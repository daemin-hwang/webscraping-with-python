from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from bs4 import BeautifulSoup

wordFile = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()

wordFile = BytesIO(wordFile)
# wordFile: <class '_io.BytesIO'>

document = ZipFile(wordFile)
# document: <class 'zipfile.ZipFile'>

xml_content = document.read("word/document.xml")
bsObj = BeautifulSoup(xml_content.decode("utf-8"), "xml")

textElements = bsObj.findAll("w:t")

for textElement in textElements:
    print(textElement.text)
