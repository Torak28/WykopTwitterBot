import wykop, json
from config import key, secret

def download_tag(tag: str = 'bookmeter', page: int = 1, flag: bool = True, index: int = 11633869) -> dict:
    api = wykop.WykopAPI(key, secret)

    ret = {}
    ret['books'] = []
    while flag:
        link = api.request("tag", 'index', [tag,], {"appkey": key, "page": str(page)})
        print(page)
        for i in range(len(dict(link)['items'])):
            try:
                id = dict(link)['items'][i]['id']
                text = dict(link)['items'][i]['body']
                if int(id) <= index:
                    flag = False
                    break
                else:
                    ret['books'].append({'Book' : text,
                                         'ID'   : id})
            except:
                print(f'Blad dla strony: {page} i iteratora: {i}')
        page += 1
    return ret

'''102'''

with open('dataAPI.json', 'w+', encoding='utf-8') as f:
    json.dump(download_tag(), f, sort_keys=True, ensure_ascii=False, indent=4)
f.close()
