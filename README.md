# WykopTwitterBot

### Idea

Ideą jest sprawdzenie czy uda się wygenerować jakieś zainteresowanie na Twitterze zamieszczając tam posty z [mikrobloga](https://www.wykop.pl/mikroblog/)

### Korzystam z

 * [Wykop API](https://github.com/p1c2u/wykop-sdk)
 * [Twitter API - twit](https://www.npmjs.com/package/twit)
 * [NodeJS](https://nodejs.org/en/)

### Config

Projekt zawiera liki ```config.py``` i ```config.js``` zawierające kolejno klucze do API Wykopu i klucze do API Twittera. 

Klucze do Wykopu dostępne są [na oficjalnej stronie](https://www.wykop.pl/dla-programistow/api/) i przetrzymywane w pliku o strukturze:

```python
key = "klucz"
secret = "sekret"
```

Klucze do Twittera dostępne są dla danego konta na [stronie deweloperskiej](https://apps.twitter.com/) i przetrzymywane w następujący sposób:

```javascript
module.exports = {
	consumer_key:         'klucz1',
	consumer_secret:      'klucz2',
	access_token:         'klucz3',
	access_token_secret:  'klucz4'
}
```

### Zaciąganie z Mikrobloga

Posłużyłem się tutaj **Pythonem**, **API Wykopu** w wersji [pythonowej](https://github.com/p1c2u/wykop-sdk), oraz **BeautifulSoup** do przetwarzania odpowiedzi z API.

Zaciągam konkretny post z gorących w zależności od podanego przy wywołaniu argumentu, np.

```
python 300.py 1
```

Dostaję odpowiedź w stylu:
```
tekst postu

link od obrazka, jeśli taki istnieje
```

Od strony samego kodu mamy tu do czynienia z połączeniem się z serwerem, pobraniem z gorących 12h(tylko taka metoda jest zaimplementowana w API), obrobieniem  odpowiedzi API w BeautifulSoup(odpowiedź to html-owa zawartość body danego postu), a następnie sprawdzenie czy odpowiedź zawiera obrazek, jak tak to dochodzi jeszcze zlinkowanie go, jak post nie ma obrazka to ten etap jest pomijany.

```python
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
```

