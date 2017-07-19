import wykop
from bs4 import BeautifulSoup

klucz = "9dFENlI8xb"
sekret = "UH2uLO4KZH"

api = wykop.WykopAPI(klucz, sekret)
gorace = api.get_stream_hot()

for i in range(len(gorace)):
    index = i

    #zmienne:
    TekstWyciagniety = gorace[index].body

    Zdjecie = None
    if hasattr(gorace[index], "embed"):
        if hasattr(gorace[index].embed, "url"):
            Zdjecie = gorace[index].embed.url

    soup = BeautifulSoup(TekstWyciagniety, 'html.parser')
    TekstPostu = soup.get_text()

    print(i, ": ----------------")
    print (TekstPostu)
    if (Zdjecie != None):
        print (Zdjecie)