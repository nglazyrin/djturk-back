# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 04:42:09 2013

@author: Nikolay
"""

import re

def clean(s):
    return re.sub('[^0-9a-zA-Z_]', '', s.lower())
        
def toUtf8(text):
    return text.encode('UTF-8', errors='replace')
    
def toName(artist, track):
    return artist + ' - ' + track
 