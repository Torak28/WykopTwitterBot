import wykop
from sys import argv
from bs4 import BeautifulSoup

klucz = "9dFENlI8xb"
sekret = "UH2uLO4KZH"

api = wykop.WykopAPI(klucz, sekret)
gorace = api.get_stream_hot()

nazwa, liczba = argv
index = int(liczba)

#zmienne:
TekstWyciagniety = gorace[index].body

Zdjecie = None
if hasattr(gorace[index], "embed"):
    if hasattr(gorace[index].embed, "url"):
        Zdjecie = gorace[index].embed.url

soup = BeautifulSoup(TekstWyciagniety, 'html.parser')
TekstPostu = soup.get_text()

print (TekstPostu)
if (Zdjecie != None):
    print (Zdjecie)