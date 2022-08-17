from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
from requests import get, post
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = ["oYnjO6uwFCUxabv1khTNgb2-j5g8"]

template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), weather['wind'], weather['airQuality'], math.floor(
        weather['high']), math.floor(weather['low'])


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en


client = WeChatClient(app_id, app_secret)
note_ch, note_en = get_ciba()
wm = WeChatMessage(client)
wea, temperature, wind, airQuality, high, low = get_weather()
data = {"weather": {"value": wea}, "city": {"value": city}, "temperature": {"value": temperature}, "wind": {"value": wind},
        "low": {"value": low}, "high": {"value": high}, "airQuality": {"value": airQuality},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()},
        "note_ch": {"value": note_ch, "color": get_random_color()},
        "note_en": {"value": note_en, "color": get_random_color()}}
res = wm.send_template(user_id[0], template_id, data)
print(res)

