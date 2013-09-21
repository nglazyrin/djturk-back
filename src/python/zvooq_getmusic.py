# -*- coding: utf-8 -*-
from json import dumps
from urllib2 import Request, urlopen
import requests

values = dumps({
    "login": "veleslavia", 
    "password": "gkfdcr"
})

headers = {"Content-Type": "application/json", "X-Method": "call"}
r = requests.post("http://kazan.zvq.me/auth/login", data=values, headers=headers)
print r.url
print r.text

headers = {"Content-Type": "application/json"}
r = requests.get('http://kazan.zvq.me/api/search?body={"string":"lady gaga bad romance"}', headers=headers)
print r.text
 
headers = {"X-Auth": ":s:a:a:k7y0EHv6tkfDWsP0XhmasUdVvpk=::1413eca6ea7::7874555"}
#request = Request('http://kazan.zvq.me/api/data/track/url?body={"id":5805325,"type":"stream"}', headers=headers)
#response_body = urlopen(request).read()
#print response_body
r = requests.get('http://kazan.zvq.me/api/data/track/url?body={"id":1416499,"type":"stream"}', headers=headers)
print r.text