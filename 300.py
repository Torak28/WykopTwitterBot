import wykop
import urllib.request
import os
from sys import argv
from bs4 import BeautifulSoup
from config import key, secret

klucz = key
sekret = secret
filenamePicture = "output.jpg"
filenameText = "output.txt"

api = wykop.WykopAPI(klucz, sekret)
gorace = api.get_stream()

nazwa, liczba = argv
index = int(liczba)

#zmienne:

if os.path.exists(filenamePicture):
	os.remove(filenamePicture)

if os.path.exists(filenameText):
	os.remove(filenameText)

TekstWyciagniety = gorace[index].body

Zdjecie = None
if hasattr(gorace[index], "embed"):
    if hasattr(gorace[index].embed, "url"):
        Zdjecie = gorace[index].embed.url

soup = BeautifulSoup(TekstWyciagniety, 'html.parser')
TekstPostu = soup.get_text()

if(len(TekstPostu) < 140):
	file = open(filenameText, "wb")
	file.write(TekstPostu.encode('utf8'))
	file.close()
	if (Zdjecie != None):
		urllib.request.urlretrieve(Zdjecie, filenamePicture)