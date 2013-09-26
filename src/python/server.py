# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 13:16:22 2013

@author: Nikolay
"""

import mixcloud
#import zvooq_getmusic as zv
import json
import sys
import urlparse
import os

import eventlet
from eventlet import wsgi

def hello_world(env, start_response):
    #print env
    if env['PATH_INFO'] != '/':
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']
    if env.has_key('QUERY_STRING'):
        q = env['QUERY_STRING']
        params = urlparse.parse_qs(q)
        try:
            artist = params['artist'][0]
            track = params['track'][0]
            #isNext = params.has_key('next')
            isNext = True
            print 'got request for ' + artist + ' - ' + track
            sys.stdout.flush()

            result = ""
            if (isNext):
                m = mixcloud.MixCloud()
                candidates = m.getCandidates(artist, track)
                start_response('200 OK', [('Content-Type', 'application/json')])
                result = json.dumps(candidates, indent=2)
#                for candidate in candidates:
#                    [artist, track] = candidate.split('-')
#                    j = zv.get_music(track, artist)
#                    if (j):
#                        result = j
#                        break;
#            else:
#                result = zv.get_music(track, artist)
            if (result):
                start_response('200 OK', [('Content-Type', 'application/json')])
                return [result]
            else:
                print "Unable to get data from zvooq"
                sys.stdout.flush()
                start_response('501 Internal Server Error: unable to get data from zvooq', [('Content-Type', 'text/plain')])
                return [str(params)]
        except:
            print "Unexpected error:", sys.exc_info()[0]
            sys.stdout.flush()
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [str(params)]
    else:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['djturk-backend\r\n']
    
#wsgi.server(eventlet.listen(('', int(os.environ['PORT']))), hello_world)
wsgi.server(eventlet.listen(('', 8080)), hello_world)
