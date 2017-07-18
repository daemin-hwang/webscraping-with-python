from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode("utf-8", "ignore")
# data:str

dataFile = StringIO(data)
# dataFile:<class '_io.StringIO'>

dicReader = csv.DictReader(dataFile)
# dicReader:<class 'csv.DictReader'>

print(dicReader.fieldnames)

for row in dicReader:
    print(row)
    # row:<class 'dict'>
