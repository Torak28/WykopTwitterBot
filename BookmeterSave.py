import requests, json, os
from bs4 import BeautifulSoup

class WykopWrapper:

    def get_link(self, id: int) -> str:
        '''
        Return text, number of + and link to img
        '''
        link = 'https://www.wykop.pl/wpis/' + str(id) + '/'
        page = requests.get(link)
        if page.status_code == 200:
            data = page.text
            soup = BeautifulSoup(data, 'html.parser')
            text_box_s1 = soup.find('div', attrs={'class':'text'})
            text_box_s2 = text_box_s1.find('p')
            text = text_box_s2.text.strip()
            image_s1 = text_box_s1.find('div', attrs={'class':'media-content video'})
            image = image_s1.find('a', href=True)['href'] if image_s1 is not None else (text_box_s1.find('img')['src'] if text_box_s1.find('img') is not None else None)
            votes_s1 = soup.findAll('div', attrs={'class':'author ellipsis '})
            votes_s2 = votes_s1[0].find('p', attrs={'class':'vC'})
            votes_s3 = votes_s2.find('span')
            vote = votes_s3.text[1:]
            if vote is '':
                vote = '0'
            if image is not None:
                return text, vote, image
            return text, vote, None
        else:
            return None

    def dump_JSON(self, str: str) -> None:
        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump(str, f, ensure_ascii=False, indent=4)
        f.close()

ww = WykopWrapper()
ww.dump_JSON(ww.get_link(11633869))

"""
[ ] Pobrac i wyluskac:
    * Tytul
    * Autor
    * Gatunek
    * Ocena
[ ] Zapisac do Bazy Danych powyzsze dane:
    * sql lite i jazda
[ ] Pobrac wiecej
    * Najstarszy : 11633869
    * Potem      : +2
"""
