# -*- coding: utf-8 -*-
from json import dumps
from urllib2 import Request, urlopen
import requests
import json
import sys

values = dumps({
    "login": "username", 
    "password": "password"
})

title = 'Yesterday'
artist = 'The Beatles'

def get_id(text):
#     idx = 0
#     cur_idx = 0
#     ids = []
#     while cur_idx != -1:
#         cur_idx = text.find("id:",idx)
#         print cur_idx
#         if cur_idx != -1:
#             number = text.find(",",cur_idx)
#             print text[cur_idx+4:number]
#             ids.append(text[cur_idx+4:number])
#             idx = cur_idx
#     print "Indexes", ids
#     return ids
    ids = []
    if "releases" not in text:
        return ids 
    for track in text["releases"]:
        ids.append(track["id"])
#    print ids
    return ids
    
def get_track_id(title, artist):
    headers = {"Content-Type": "application/json", "X-Method": "call"}
    r = requests.post("http://kazan.zvq.me/auth/login", data=values, headers=headers)
    headers = {"Content-Type": "application/json"}
    
    r = requests.get('http://kazan.zvq.me/api/search?body={"string":"'+title.strip()+'"}', headers=headers)
#    print r.url
#    print r.text
    if (r.status_code == requests.codes.ok):
        title_id = get_id(json.loads(r.text))
    else:
        title_id = []
    
    r = requests.get('http://kazan.zvq.me/api/search?body={"string":"'+artist.strip()+'"}', headers=headers)
#    print r.url
#    print r.text
    if (r.status_code == requests.codes.ok):
        artist_id = get_id(json.loads(r.text))
    else:
        artist_id = []
    if len(title_id) != 0:
        for id in title_id:
            if len(artist_id) != 0:
                if id in artist_id:
                    return id
            return title_id[0]
    return "Song not found"

def get_music(title, artist):
    id = get_track_id(title, artist)
    print id
    sys.stdout.flush()
    if id != "Song not found":
        headers = {"X-Auth": ":s:a:a:k7y0EHv6tkfDWsP0XhmasUdVvpk=::1413eca6ea7::7874555"}
        r = requests.get('http://kazan.zvq.me/api/data/track/url?body={"id":'+str(id)+',"type":"stream"}', headers=headers)
        #headers = {"Content-Type": "application/json", "X-Method": "call"}
        print r.status_code
        print r.text
        sys.stdout.flush()
        if (r.status_code == requests.codes.ok):
            url = json.loads(r.text)
            song_info = dumps({
                               "author": artist, 
                               "composition": title,
                               "url": url["url"]
            })
            return song_info
        else:
            return None
    else:
        return None
    #print id

#get_music(title, artist)
