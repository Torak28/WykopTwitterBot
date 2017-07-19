import wykop
from bs4 import BeautifulSoup

index = 5
'''
    Tym razem używam BeautifulSoup to parsowania html przez co nie ma zabawy znacznikami i regexem. :>
'''


klucz = "9dFENlI8xb"
sekret = "UH2uLO4KZH"

api = wykop.WykopAPI(klucz, sekret)
profile = api.get_stream_hot()

#zmienne:
TekstWyciagniety = profile[index].body

Zdjecie = None
if hasattr(profile[index], "embed"):
    if hasattr(profile[index].embed, "url"):
        Zdjecie = profile[index].embed.url

soup = BeautifulSoup(TekstWyciagniety, 'html.parser')
TekstPostu = soup.get_text()

if (len(TekstPostu) < 300):
    print (TekstPostu)
    if (Zdjecie != None):
        print (Zdjecie)