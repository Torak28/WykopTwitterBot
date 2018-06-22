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
        elif 'autor:' in text:
             return text.split('autor:')[1].split('\n')[0][1:]
        elif 'Autorzy:' in text:
             return text.split('Autorzy:')[1].split('\n')[0][1:]
        elif 'autorzy:' in text:
             return text.split('autorzy:')[1].split('\n')[0][1:]
        return None

    def get_title(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if 'Tytuł:' in text:
             return text.split('Tytuł:')[1].split('\n')[0][1:]
        elif 'tytuł:' in text:
             return text.split('tytuł:')[1].split('\n')[0][1:]
        elif 'Tytułł:' in text:
             return text.split('Tytułł:')[1].split('\n')[0][1:]
        elif 'tytułł:' in text:
             return text.split('tytułł:')[1].split('\n')[0][1:]
        elif 'Tytuły:' in text:
             return text.split('Tytuły:')[1].split('\n')[0][1:]
        elif 'tytuły:' in text:
             return text.split('tytuły:')[1].split('\n')[0][1:]
        elif 'Tutuły:' in text:
             return text.split('Tutuł:')[1].split('\n')[0][1:]
        return None

    def get_type(self, text: str) -> str:
        text = BeautifulSoup(text, 'html.parser').text
        if 'Gatunek:' in text:
             return text.split('Gatunek:')[1].split('\n')[0][1:]
        elif 'gatunek:' in text:
             return text.split('gatunek:')[1].split('\n')[0][1:]
        elif 'Gatuenk:' in text:
             return text.split('Gatuenk:')[1].split('\n')[0][1:]
        elif 'gatuenk:' in text:
             return text.split('gatuenk:')[1].split('\n')[0][1:]
        elif 'Garunek:' in text:
             return text.split('Garunek:')[1].split('\n')[0][1:]
        elif 'garunek:' in text:
             return text.split('garunek:')[1].split('\n')[0][1:]
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
        """
        No info
        """
        author = self.get_author(text)
        title = self.get_title(text)
        type = self.get_type(text)
        grade = self.get_grade(text)
        if author is not None and title is not None and type is not None:
            return author, title, type, grade
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
    count, aut, tyt, gat, oce = 0, 0, 0, 0, 0
    deb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(ret['Books'])):
        # print(sw.get_data(ret['Books'][i]['Book']))
        if sw.get_data(ret['Books'][i]['Book']) is None:
            txt = BeautifulSoup(ret['Books'][i]['Book'], 'html.parser').text

            t1 = 'A' if sw.get_author(txt) is None else '-'
            t2 = 'T' if sw.get_title(txt) is None else '-'
            t3 = 'G' if sw.get_type(txt) is None else '-'
            t4 = 'O' if sw.get_grade(txt) is None else '-'

            tD = t1 + t2 + t3 + t4

            if tD != 'ATGO':
                count += 1
                aut += 1 if sw.get_author(txt) is None else 0
                tyt += 1 if sw.get_title(txt) is None else 0
                gat += 1 if sw.get_type(txt) is None else 0
                oce += 1 if sw.get_grade(txt) is None else 0

                tmp1 = 'A' if sw.get_author(txt) is None else '-'
                tmp2 = 'T' if sw.get_title(txt) is None else '-'
                tmp3 = 'G' if sw.get_type(txt) is None else '-'
                tmp4 = 'O' if sw.get_grade(txt) is None else '-'

                D = tmp1 + tmp2 + tmp3 + tmp4

                deb[0] += 1 if D == 'ATGO' else 0
                deb[1] += 1 if D == 'A---' else 0
                deb[2] += 1 if D == '-T--' else 0
                deb[3] += 1 if D == '--G-' else 0
                deb[4] += 1 if D == '---O' else 0
                deb[5] += 1 if D == 'AT--' else 0
                deb[6] += 1 if D == '-TG-' else 0
                deb[7] += 1 if D == '-T-O' else 0
                deb[8] += 1 if D == 'A-G-' else 0
                deb[9] += 1 if D == '--GO' else 0
                deb[10] += 1 if D == 'A--O' else 0
                deb[11] += 1 if D == 'ATG-' else 0
                deb[12] += 1 if D == '-TGO' else 0
                deb[13] += 1 if D == 'A-GO' else 0
                deb[14] += 1 if D == 'AT-O' else 0
                xd['Books'].append({'Autor: '   : sw.get_author(txt),
                                    'Tytuł: '   : sw.get_title(txt),
                                    'Gatunek: ' : sw.get_type(txt),
                                    'Ocena: '   : sw.get_grade(txt),
                                    'Text: '    : txt,
                                    'Debug: '   : D
                                    })
    dw.save_to_JSON(data=xd, file='xd.json')
    print(f'Wszystkich zlych: {count}, w tym\n\tAutorow: {aut}\n\tTytulow: {tyt}\n\tGatunkow: {gat}\n\tOcen: {oce}\n\nA dokladnie:\n\tATGO - {deb[0]}\n\tA--- - {deb[1]}\n\t-T-- - {deb[2]}\n\t--G- - {deb[3]}\n\t---O - {deb[4]}\n\tAT-- - {deb[5]}\n\t-TG- - {deb[6]}\n\t-T-O - {deb[7]}\n\tA-G- - {deb[8]}\n\t--GO - {deb[9]}\n\tA--O - {deb[10]}\n\tATG- - {deb[11]}\n\t-TGO - {deb[12]}\n\tA-GO - {deb[13]}\n\tAT-O - {deb[14]}\nW sumie: {sum(deb)}')
    # 546, 542(Autorzy), 130(brak oceny), 67(po ifie i odrzuceniu jakis zapytan), 59(gatunek plus wielkosc liter) textow failuje :c

"""
Co jak jest wiecej niz jedno xd

Wszystkich zlych: 59, w tym
        Autorow: 26
        Tytulow: 24
        Gatunkow: 51
        Ocen: 24

A dokladnie:
        ATGO - 0
        A--- - 1
        -T-- - 2
        --G- - 11
        ---O - 0
        AT-- - 0
        -TG- - 0
        -T-O - 1
        A-G- - 1
        --GO - 19
        A--O - 3
        ATG- - 20
        -TGO - 0
        A-GO - 0
        AT-O - 1
W sumie: 59



[ ] Zapisac do Bazy Danych powyzsze dane:
    * sql lite i jazda
"""
