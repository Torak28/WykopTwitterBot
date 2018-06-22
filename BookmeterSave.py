import requests, json, os, wykop
from bs4 import BeautifulSoup
from config import key, secret


class WykopWrapper():

    def download_tag(self, tag: str = 'bookmeter', page: int = 1, flag: bool = True, index: int = 11633869) -> dict:
        api = wykop.WykopAPI(key, secret)

        ret = {}
        ret['Books'] = []
        while flag:
            link = api.request("tag", 'index', [tag,], {"appkey": key, "page": str(page)})
            print(page)
            for i in range(len(dict(link)['items'])):
                try:
                    id = dict(link)['items'][i]['id']
                    text = dict(link)['items'][i]['body']
                    if int(id) < index:
                        flag = False
                        break
                    else:
                        ret['books'].append({'Book' : text,
                                             'ID'   : id})
                except:
                    print(f'Blad dla strony: {page} i iteratora: {i}')
            page += 1
        return ret


    def save_to_JSON(self, data: dict, file: str = 'dataAPI.json') -> None:
        with open(file, 'w+', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, ensure_ascii=False, indent=4)
        f.close()

class StringWrapper:
    '''
    Class to check and save strings
    '''

    def get_author(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if 'Autor:' in text:
             return text.split('Autor:')[1].split('\n')[0][1:]
        return None

    def get_title(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if 'Tytuł:' in text:
             return text.split('Tytuł:')[1].split('\n')[0][1:]
        return None

    def get_type(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if 'Gatunek:' in text:
             return text.split('Gatunek:')[1].split('\n')[0][1:]
        return None

    def get_grade(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if '★' in text:
             return text.count('★')
        return None

    def get_info(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if '\n\n' in text:
             return text.split('\n\n', 1)[1].split('#bookmeter')[0]
        return None

    def get_data(self, text: str) -> dict:
        author = self.get_author(text)
        title = self.get_title(text)
        type = self.get_type(text)
        grade = self.get_grade(text)
        # info = self.get_info(text)
        if author is not None and title is not None and type is not None and grade is not None: #and info is not None:
            return author, title, type, grade# , info
        return None

    def dump_JSON(self, str: dict) -> None:
        '''
        Write str to data.json
        '''
        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump(str, f, ensure_ascii=False, indent=4)
        f.close()

class DataWrapper:

    def read_JSON(self, file: str = 'dataAPI.json') -> dict:
        try:
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
            f.close()
        except Exception as e:
            data = None
        return data

    def save_to_JSON(self, data: dict, file: str = 'data.json') -> None:
        with open(file, 'w+', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, ensure_ascii=False, indent=4)
        f.close()

'''
    Zrobic test dla 11637749 bo mi zawsze wywala :c
'''


if __name__ == "__main__":
    # ww = WykopWrapper()
    # ww.save_to_JSON(ww.download_tag())
    # print(ww.download_tag())
    dw = DataWrapper()
    sw = StringWrapper()
    # dw.save_to_JSON(data=sw.get_data(dw.read_JSON('dataAPI.json')))
    ret = dw.read_JSON('dataAPI.json')
    xd = {}
    xd['Books'] = []
    count = 0
    for i in range(len(ret['Books'])):
        # print(sw.get_data(ret['Books'][i]['Book']))
        if sw.get_data(ret['Books'][i]['Book']) is None:
            count += 1
            xd['Books'].append({'text' : BeautifulSoup(ret['Books'][i]['Book'], 'html.parser').text})
    dw.save_to_JSON(data=xd, file='xd.json')
    print(count)





"""
[x] Add some debug mode to check wykop id
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
