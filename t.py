import wykop, json
from config import key, secret

api = wykop.WykopAPI(key, secret)

"102"

ret = {}
ret['books'] = []
index = 11633869
flag = True
page = 1
while flag:
    link = api.request("tag", 'index', ["bookmeter",], {"appkey": key, "page": str(page)})
    print(page)
    for i in range(len(dict(link)['items'])):
        try:
            id = dict(link)['items'][i]['id']
            text = dict(link)['items'][i]['body']
            if int(id) is index:
                flag = False
                break
            else:
                ret['books'].append({'Book' : text,
                                     'ID'   : id})
        except:
            print(f'Blad dla strony: {page} i iteratora: {i}')
    page += 1

# ret = {}
# ret['books'] = []
# link = api.request("tag", 'index', ["bookmeter",], {"appkey": key, "page": str(102)})
# for i in range(len(dict(link)['items'])):
#     try:
#         text = dict(link)['items'][i]['body']
#         id = dict(link)['items'][i]['id']
#         ret['books'].append({'Book' : text,
#                              'ID'   : id})
#     except KeyError:
#         print(i)

with open('dataAPI.json', 'w+', encoding='utf-8') as f:
    json.dump(ret, f, sort_keys=True, ensure_ascii=False, indent=4)
f.close()
