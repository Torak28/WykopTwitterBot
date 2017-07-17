import wykop
import re

index = 17
'''
    Nie udaje mi sie jak całość nie kończy się #
    W sensie nie udaje mi się kiedy np. zaczyna się od # albo # jest gdzieś w środku
    No i maks indeks to 17 nie wiem czemu :c
'''


klucz = "klucz"
sekret = "sekret"

api = wykop.WykopAPI(klucz, sekret)
profile = api.get_stream_hot()

#zmienne:
TekstWyciagniety = profile[index].body
Zdjecie = profile[index].embed.url

Tekst = TekstWyciagniety.replace('<br />', '')
hasz = "#"
Hasztag = Tekst[Tekst.index(hasz) + len(hasz):]
TekstPostu = Tekst[:Tekst.index(hasz)]

Post = TekstPostu

regex = r"(?<=>)[^\<# ]+"

hasztagi = re.finditer(regex, Hasztag)

for matchNum, match in enumerate(hasztagi):
    matchNum = matchNum + 1
    TekstPostu += "#" + match.group() + " "


if (len(TekstPostu) < 300):
    print (TekstPostu)
    print (Zdjecie)
