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

    def check_str(self, text: str) -> bool:
        if  text is not None and '#bookmeter' in text:
            return True
        return False

    def get_max_wykop_id(self) -> int:
        link = 'https://www.wykop.pl/mikroblog/wszystkie/'
        page = requests.get(link)
        if page.status_code == 200:
            data = page.text
            soup = BeautifulSoup(data, 'html.parser')
            id_1 = soup.find('div', attrs={'id':'content'})
            id_2 = id_1.find('li', attrs={'class':'entry iC '})
            id_3 = id_2.findAll('div', attrs={'class':'wblock lcontrast dC '})
            return int(id_3[0]['data-id'])
        else:
            return random.choice(range(21, big_number, 2))

class StringWrapper:
    '''
    Class to check and save strings
    '''

    def get_author(self, text: str) -> str:
        if 'Autor' in text:
             return text.split('Autor:')[1].split('\n')[0][1:]
        return None

    def get_title(self, text: str) -> str:
        if 'Tytuł' in text:
             return text.split('Tytuł:')[1].split('\n')[0][1:]
        return None

    def get_type(self, text: str) -> str:
        if 'Gatunek' in text:
             return text.split('Gatunek:')[1].split('\n')[0][1:]
        return None

    def get_grade(self, text: str) -> str:
        if '★' in text:
             return text.count('★')
        return None

    def get_info(self, text: str) -> str:
        if '\n\n' in text:
             return text.split('\n\n', 1)[1].split('#bookmeter')[0]
        return None

    def get_data(self, text: str) -> dict:
        author = self.get_author(text)
        title = self.get_title(text)
        type = self.get_type(text)
        grade = self.get_grade(text)
        info = self.get_info(text)
        if author is not None and title is not None and type is not None and grade is not None and info is not None:
            return author, title, type, grade, info
        return None

    def dump_JSON(self, str: dict) -> None:
        '''
        Write str to data.json
        '''
        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump(str, f, ensure_ascii=False, indent=4)
        f.close()


if __name__ == "__main__":
    ww = WykopWrapper()
    sw = StringWrapper()
    ret = {}
    ret['books'] = []
    index = 11633869
    max = ww.get_max_wykop_id()
    how_many = (max - index) // 2
    current = 1
    while index <= max:
        text = ww.get_link(index)
        print(f'{current}/{how_many} -> {current/how_many * 100:.3f}%, index - {index}')
        if ww.check_str(text):
            author, title, type, grade, info = sw.get_data(text)
            ret['books'].append({
                        'Author': str(author),
                        'Title': str(title),
                        'Type': str(type),
                        'Grade': str(grade),
                        'Info': str(info)
                        })
        current += 1
        index += 2
    sw.dump_JSON(ret)



"""
[ ] Add some debug mode to check wykop id
[x] Pobrac i wyluskac:
    * Tytul
    * Autor
    * Gatunek
    * Ocena
[x] Zmienic konwencje data.json tak zeby lepiej pobrac
[ ] Zapisac do Bazy Danych powyzsze dane:
    * sql lite i jazda
[x] Pobrac wiecej
    * Najstarszy : 11633869
    * Potem      : +2
    * This is sooooooooooooooooooooo slow. Better try some node js :c
"""
