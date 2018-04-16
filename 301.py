import wykop, requests, json, time, tweepy, os, random
from bs4 import BeautifulSoup
from config import klucz, sekret, twitter_key, twitter_secret, twitter_acces_token, twitter_acces_token_secret

twitter_max = 280
min_votes = 100
num_of_links = 20
min_time = 300
max_time = 600

def get_link(id):
    link = 'https://www.wykop.pl/wpis/' + str(id) + '/'
    page = requests.get(link)
    if page.status_code == 200:
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        text_box_s1 = soup.find('div', attrs={'class':'text'})
        text_box_s2 = text_box_s1.find('p')
        text = text_box_s2.text.strip()
        image = text_box_s1.find('img')
        votes_s1 = soup.find('div', attrs={'class':'author ellipsis'})
        votes_s2 = votes_s1.find('span')
        vote = votes_s2.text[1:]
        if image is not None:
            return text, vote, image['src']
        return text, vote, None
    else:
        return None

def check_link(link):
    if link is None or link[0] is None or len(str(link[0])) > 279 or int(link[1]) < min_votes:
        return None
    return link

def get_links(amount):
    ret = {}
    ret['links'] = []
    index = get_wykop_id()
    i = 0
    while i < amount:
        link = get_link(index)
        good_link = check_link(link)
        if good_link is not None:
            text = good_link[0] if good_link[0] is not None else None
            vote = good_link[1]
            photo = good_link[2] if good_link[2] is not None else None
            ret['links'].append({
                        'id': str(index),
                        'text': str(text),
                        'votes': str(vote),
                        'photo': str(photo)
                        })
            i += 1
        index -= 2
    return ret

def get_wykop_id():
    api = wykop.WykopAPI(klucz, sekret)
    all = api.get_stream()
    return all[0].id

def dump_links_JSON(amount):
    str = get_links(amount)
    with open('data.json', 'w+', encoding='utf-8') as f:
        json.dump(str, f, ensure_ascii=False, indent=4)
    f.close()

def dump_JSON(str):
    with open('data.json', 'w+', encoding='utf-8') as f:
        json.dump(str, f, ensure_ascii=False, indent=4)
    f.close()

def read_links_JSON():
    try:
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)
        f.close()
    except Exception as e:
        data = None
    return data

def print_JSON(f):
    return json.dumps(f, sort_keys=True, indent=4, ensure_ascii=False)

def get_link_JSON():
    data = read_links_JSON()
    if data is None or len(data['links']) is 0:
        dump_links_JSON(num_of_links)
        data = read_links_JSON()
    id = data['links'][0]['text']
    text = data['links'][0]['text']
    photo = data['links'][0]['photo']
    del data['links'][0]
    dump_JSON(data)
    return text, photo

def dowload_pic(url):
    try:
        img_data = requests.get(url).content
        with open('tmp.jpg', 'wb') as h:
            h.write(img_data)
        return True
    except Exception as e:
        return False

auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
auth.set_access_token(twitter_acces_token, twitter_acces_token_secret)
api = tweepy.API(auth)

"""
[ ] Ogarnac zdjecia
[ ] Ogarnac followanie
[ ] Jakies odpowiedzi?
[ ] A co jak gif?
[ ] A co jak filmik?
"""

i = 0
while True:
    status, img = get_link_JSON()
    send_flag = False
    if img is 'None':
        api.update_status(status)
        send_flag = True
    else:
        check = dowload_pic(img)
        if check:
            api.update_with_media('tmp.jpg', status)
            send_flag = True
            os.remove('tmp.jpg')
    if send_flag:
        print('Poszedl: ', str(i), ' tweet')
    i +=1
    time.sleep(random.randint(min_time, max_time))
