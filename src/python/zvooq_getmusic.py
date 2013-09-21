# -*- coding: utf-8 -*-
from json import dumps
from urllib2 import Request, urlopen
import requests

values = dumps({
    "login": "veleslavia", 
    "password": "gkfdcr"
})

def get_id(text):
    
    
    
def get_track_id(title, artist):
    headers = {"Content-Type": "application/json", "X-Method": "call"}
    r = requests.post("http://kazan.zvq.me/auth/login", data=values, headers=headers)
    headers = {"Content-Type": "application/json"}

    r = requests.get('http://kazan.zvq.me/api/search?body={"string":"'+title+'"}"', headers=headers)
    title_id = get_id(r.text)
    r = requests.get('http://kazan.zvq.me/api/search?body={"string":"'+artist+'"}"', headers=headers)
    artist_id = get_id(r.text)
    if len(title_id) != 0:
        for id in title_id:
            if len(artist_id) != 0:
                if id in artist_id:
                    return id
            return title_id[0]
    return "Song not found"
    
headers = {"X-Auth": ":s:a:a:k7y0EHv6tkfDWsP0XhmasUdVvpk=::1413eca6ea7::7874555"}
r = requests.get('http://kazan.zvq.me/api/data/track/url?body={"id":'+str(id)+',"type":"stream"}', headers=headers)

print r.text