# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 13:16:22 2013

@author: Nikolay
"""

import mixcloud
import json
import sys
import urlparse

import eventlet
from eventlet import wsgi

def hello_world(env, start_response):
    #print env
    print 'got request'
    if env['PATH_INFO'] != '/':
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']
    q = env['QUERY_STRING']
    if q:
        params = urlparse.parse_qs(q)
        try:
            artist = params['artist'][0]
            track = params['track'][0]
            print 'got request for ' + artist + ' - ' + track
            sys.stdout.flush()
            m = mixcloud.MixCloud()
            candidates = m.getCandidates(artist, track)
            j = json.dumps(candidates)
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [j]
        except:
            print "Unexpected error:", sys.exc_info()[0]
            sys.stdout.flush()
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [str(params)]
    else:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['djturk-backend\r\n']
    
wsgi.server(eventlet.listen(('', 80)), hello_world)
