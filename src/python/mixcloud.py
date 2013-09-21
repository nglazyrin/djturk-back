# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 00:26:42 2013

@author: Nikolay
"""

import requests
import json
import string
import sys
import util as u
import zvooq_getmusic as zv

class MixCloud(object):
    
    def wwwToApi(self, str):
        return str.replace('http://www.', 'http://api.')
   
    def search(self, artist, track, offset):
        limit = 50
        counts = {}
        q = string.join([artist, track]).replace(' ', '+')
        r = requests.get('http://api.mixcloud.com/search/?q=' + q +
                '&type=cloudcast&limit=' + str(limit) + '&offset=' + str(offset))
        #print u.toUtf8(r.text)
        j = json.loads(u.toUtf8(r.text))
        for d in j['data']:
            url = d['url']
            user = d['user']['url']
            ur = requests.get(self.wwwToApi(user))
            #print u.toUtf8(ur.text)
            follower_count = json.loads(u.toUtf8(ur.text))['follower_count']
            counts[url] = [d['listener_count'], d['play_count'], d['favorite_count'],
                   d['comment_count'], follower_count]
        if ('paging' in j):
            if ('next' in j['paging']):
                counts.update(self.search(artist, track, offset + limit))
        print (str(len(counts)) + ' tracklists were found')
        return counts

    def getTrackFromTracklist(self, url, artist, track):
        r = requests.get(self.wwwToApi(url))
        cloudcast = json.loads(u.toUtf8(r.text))
        if ('sections' in cloudcast):
            for section in cloudcast['sections']:
                if ('track' in section):
                    tracklistArtistName = section['track']['artist']['name']
                    if (u.clean(tracklistArtistName) == u.clean(artist)):
                        trackName = self.getFullName(section['track']['artist']['name'], section['track']['name'])
                        return trackName
        return None

    def getNeighboursFromTracklist(self, url, artist, track):
        r = requests.get(self.wwwToApi(url))
        cloudcast = json.loads(u.toUtf8(r.text))
        result = []
        if ('sections' in cloudcast):
            sections = cloudcast['sections']
            for (i, section) in enumerate(sections):
                if ('track' in section):
                    tracklistArtistName = section['track']['artist']['name']
                    tracklistTrackName = section['track']['name']
                    if (u.clean(tracklistArtistName) == u.clean(artist) and u.clean(tracklistTrackName) == u.clean(track)):
                        if (i > 0):
                            prev = sections[i - 1]
                            name = u.toName(prev['track']['artist']['name'], prev['track']['name'])
                            result.append(name)
                        if (i < len(sections) - 1):
                            nxt = sections[i + 1]
                            name = u.toName(nxt['track']['artist']['name'], nxt['track']['name'])
                            result.append(name)
                        break
        return result

    def getCandidates(self, artist, track):
        tracklists = self.search(artist, track, 0)
        tracks = {}
        total = 0
        for url in tracklists.keys():
            neighbours = self.getNeighboursFromTracklist(url, artist, track)
            for neighbour in neighbours:
                r = self.getRank(tracklists[url])
                tracks[neighbour] = r
            total = total + 1
            if (total % 10 == 0):
                print str(total) + ' playlists processed'
        return sorted(tracks, key=tracks.get, reverse=True)
        #return tracks

    def getRank(self, counts):
        listenerCount = counts[0]
        playCount = counts[1]
        favoriteCount = counts[2]
        commentCount = counts[3]
        followerCount = counts[4]
        result = listenerCount + playCount + favoriteCount + commentCount + followerCount
        return result

    def doTest(self):
        #r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
        #r = requests.get('http://api.mixcloud.com/artist/aphex-twin/')
        artist = 'Lady Gaga'
        track = 'Bad Romance'
        tracks = self.getCandidates(artist, track)
        for candidate in tracks:
            [artist, track] = candidate.split('-')
            j = zv.get_music(track, artist)
            if (j):
                break;
        print j
    
def main(artist, track):
    m = MixCloud()
    c = m.getCandidates(artist, track)
    print c

if __name__ == '__main__':
    print sys.argv
    if (len(sys.argv) >= 3):
        main(sys.argv[1], sys.argv[2])
