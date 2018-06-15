import requests, json, time, tweepy, os, random, wget, youtube_dl
from bs4 import BeautifulSoup
from config import twitter_key, twitter_secret, twitter_acces_token, twitter_acces_token_secret

twitter_max = 280
min_votes = 0
num_of_links = 20
min_time = 30
max_time = 60
big_number = 31398503

def get_link(id):
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

def check_link(link):
    '''
    Check if link is long enough and has good amount of +
    '''
    if link is None or len(str(link[0])) > 279 or int(link[1]) < min_votes:
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

def download_jpg(url):
    try:
        img_data = requests.get(url).content
        with open('tmp.jpg', 'wb') as h:
            h.write(img_data)
        return True
    except Exception as e:
        return False

def download_you(url):
    try:
        ydl_opts = {
        'max_filesize' : 15000000,
        'format' : 'mp4',
        'outtmpl' : 'tmp.mp4'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        return False

def download_gfy(url):
    link = url[:8] + 'giant.' + url[8:] + '.mp4'
    try:
        wget.download(link, out='tmp.mp4')
    except Exception as e:
        return False

def download_media(url):
    '''
    1 - jpg
    2 - you
    3 - gfy
    '''
    check = url[8:]
    if check.endswith('.jpg'):
        try:
            download_jpg(url)
            return 1
        except Exception as e:
            return False
    elif check.startswith('www.you'):
        try:
            download_you(url)
            return 2
        except Exception as e:
            return False
    elif check.startswith('gfy'):
        try:
            download_gfy(url)
            return 3
        except Exception as e:
            return False
    else:
        return False

def delete_tmp():
    if os.path.isfile('tmp.mp4'):
        os.remove('tmp.mp4')
    elif os.path.isfile('tmp.jpg'):
        os.remove('tmp.jpg')

"""
auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
auth.set_access_token(twitter_acces_token, twitter_acces_token_secret)
api = tweepy.API(auth)

[x] Odseparowac sie od wykop-sdk
    [x] skrapowac id do najsiwezszego z najnowszych
    [x] przejzec funkcje sprawdzajaca zeby nie sypala sie dla pustych wpisow ale ze zdjeciem
[x] Ogarnac media
    [x] Formaty linkow info - jak to jest gif albo co innego to i tak miniaturke zapisuje jako jpg
    [x] Ogarniete foramty, nadal trzeba pobrac
    [x] Ogarnite pobieranie psozczegolnych formatow
    [x] jakas flaga pobierania?
[x] Debug mediow
    [x] bladNIE
    [ ] Spr czy sie wysyla tyle ile ma
[ ] Ogarnac followanie
[ ] Jakies odpowiedzi?
[ ] A co jak gif?
[ ] A co jak filmik?
[ ] Tweet za followa


i = 0
done_flag = False
dbug = 0
while True:
    status, img = get_link_JSON()
    if img == 'None':
        if api.update_status(status):
            done_flag = True
    else:
        check = download_media(img)
        if check is 1:
            if api.update_with_media('tmp.jpg', status):
                done_flag = True
        elif check is 2 or check is 3:
            if api.update_with_media('tmp.mp4', status):
                done_flag = True
        if done_flag:
            delete_tmp()
    if done_flag:
        print('Poszedl: ', str(i), ' tweet')
        time.sleep(random.randint(min_time, max_time))
    i +=1
    done_flag = False
    print(dbug)
    dbug += 1
"""
