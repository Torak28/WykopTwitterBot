from bs4 import BeautifulSoup

d = {
        "Books": [
          {
            "Book": "2 046 - 2 = 2 044<br />\n<br />\n<strong>Tytuł:</strong> Trybunał dusz<br />\n<strong>Autor</strong>: Donato Carrisi<br />\n<strong>Gatunek</strong>: thriller<br />\n★★★★★☆☆☆☆☆<br />\n<br />\nNo tak średnio bym powiedział, tak średnio.<br />\nJest to przeciętny dreszczowiec kilka ciekawych pomysłów, ale źle wykorzystanych. Na włoskiej wikipedii można dowiedzieć się że jest to religijny thriller. No z tym bym nie przesadzał, jest tam co prawda wątek z organizacją kościelną ale jest kiepski.  Główny bohater ma ciekawą przeszłość i jest on chyba najmocniejszą stroną tej książki. Podczas czytania nawet zastanawiałem się czy nie przestać. Końcówka trochę ratuje więc aż 5/10. <br />\nRaczej nie polecam, jeżeli ktoś chce przeczytać jakiś jakiś kryminał albo thriller to lepiej sięgnąć po coś innego.  <br />\n<br />\n<strong>Tytuł:</strong> Mistrz i Małgorzata<br />\n<strong>Autor</strong>: Michaił Bułhakow<br />\n<strong>Gatunek</strong>: Farsa, Mistycyzm, Romans, Satyra, Modernizm<br />\n★★★★★★★★★☆<br />\n<br />\nChyba każdy zna więc nie będę się rozpisywał. Poza tym ktoś 2 tygodnie temu pisał tu na temat tej powieści.  Polecam wszystkim <br />\n<br />\n#<a href=\"#bookmeter\">bookmeter</a> #<a href=\"#ksiazki\">ksiazki</a> #<a href=\"#czytajzwykopem\">czytajzwykopem</a> <br />\n<br />\nWpis został dodany za pomocą skryptu <a href=\"http://bookmeter.anonim1133.me\" rel=\"nofollow\">do odejmowania</a><br />\n<br />\n<code class=\"dnone\">  Dzięki niemu unika się błędów w działaniach<br />\n  Pobierany jest zawsze ostatni wynik<br />\n</code>",
            "ID": 32578235
          }
        ]
    }

def get_author(text: str) -> str:
    text = BeautifulSoup(text, 'html.parser').text
    if 'Autor:' in text:
         tmp = text.split('Autor:')
         ret = []
         for i in range(1, len(tmp)):
             ret.append(tmp[i].split('\n')[0][1:])
         return ret
    return None

txt = BeautifulSoup(d['Books'][0]['Book'], 'html.parser').text

print(get_author(txt))
