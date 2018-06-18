import wykop, json
from config import key, secret

api = wykop.WykopAPI(key, secret)
link = api.request("tag", 'index', ["bookmeter",], {"appkey": key})

text = ''
for i in range(len(dict(link)['items'])):
    text += dict(link)['items'][i]['body']


with open('dataAPI.json', 'w+', encoding='utf-8') as f:
    json.dump(text, f, sort_keys=True, ensure_ascii=False, indent=4)
f.close()
