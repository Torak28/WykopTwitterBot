import requests, json, os
from bs4 import BeautifulSoup

class WykopWrapper:
    '''
    Class to wrap wykop.pl content
    '''

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
            return text
        else:
            return None

class StringWrapper:
    '''
    Class to check and save strings
    '''

    def dump_JSON(self, str: str) -> None:
        '''
        Write str to data.json
        '''
        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump(str, f, ensure_ascii=False, indent=4)
        f.close()

    def check_str(self, str: str) -> bool:
        if '#bookmeter' in str:
            return True
        return False

    def get_author(self, str: str) -> str:
        if 'Autor' in str:
             return str.split('Autor:')[1].split('\n')[0][1:]
        return None

    def get_title(self, str: str) -> str:
        if 'Tytuł' in str:
             return str.split('Tytuł:')[1].split('\n')[0][1:]
        return None

    def get_type(self, str: str) -> str:
        if 'Gatunek' in str:
             return str.split('Gatunek:')[1].split('\n')[0][1:]
        return None

    def get_grade(self, str: str) -> str:
        if '★' in str:
             return str.count('★')
        return None

    def get_info(self, str: str) -> str:
        if '#bookmeter' in str:
             return str.split('\n\n', 1)[1].split('#bookmeter')[0]
        return None


ww = WykopWrapper()
sw = StringWrapper()
text = ww.get_link(11633869)
print(text)
if sw.check_str(text):
    print("tak")
    print(sw.get_author(text))
    print(sw.get_title(text))
    print(sw.get_type(text))
    print(sw.get_grade(text))
    print(sw.get_info(text))



"""
[ ] Pobrac i wyluskac:
    * Tytul
    * Autor
    * Gatunek
    * Ocena
[ ] Zmienic konwencje data.json tak zeby lepiej pobrac
[ ] Zapisac do Bazy Danych powyzsze dane:
    * sql lite i jazda
[ ] Pobrac wiecej
    * Najstarszy : 11633869
    * Potem      : +2
"""
