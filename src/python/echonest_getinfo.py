# -*- coding: utf-8 -*-
from pyechonest import config
from pyechonest import song
from pyechonest import artist
from pyechonest import catalog

config.ECHO_NEST_API_KEY='WQ7YLXHWHTEIOZ9SK'

class SongsByTitleAndArtist:
    
    def init(self, title_name, artist_name):
        self.title = title_name
        self.artist = artist_name
        self.results = song.search(title=self.title, artist=self.artist, results=1)
#        self.results = song.search(title=self.title, artist=self.artist, results=1)
        self.counts = len(self.results)
        
# give url on the Last.fm with bio of artist        
    def find_lastfm_bio(self, artist_id):
        for bio in artist.Artist(artist_id).biographies:
            if bio['url'].find('last.fm') != -1:
                return bio['url']
        return 'Artist biography not found'
                
# give additional info about song and artist from the Echonest
# if we have not         
    def give_info(self):
        if self.counts == 0:
            return "Song not found"
        print self.counts
#        self.results[0].get_tracks('7digital-US')

#            print res.id
#        print res.title
#            print res.song_hotttnesss
#            print res.artist_name
#        print res.artist_id
        return self.find_lastfm_bio(self.results[0].artist_id)
#            print res.artist_hotttnesss
#            print res.audio_summary

#    def available_urls(self):
#        print self.results[0].get_tracks('7digital-US')
        #[0].get('preview_url')
        
def info_by_sample(sample):
    songs_res = SongsByTitleAndArtist()
    songs_res.init(sample[0], sample[1])
    return songs_res.give_info()

info_about_next_track = [["Bad Romance","Lady Gaga"], ["Yesterday","The Beatles"]]

for info_sample in info_about_next_track:
# create and init new songs list on the info_sample
    info_by_sample(info_sample)