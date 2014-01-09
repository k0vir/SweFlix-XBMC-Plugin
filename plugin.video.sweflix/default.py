import re
import sys
from urllib import quote, unquote
import xbmcaddon
from resources.lib import scraper, utils
import xbmc
import HTMLParser

def add_video(video):
    if 'tv' not in params['mode']:
        if video['type'] == 'film':
            htmlEscaper = HTMLParser.HTMLParser()
            utils.add_directory_link(video['titel'], 
                                        video['logo'], 
                                        'play_video', 
                                        video['url'],
                                        plot=htmlEscaper.unescape(video['plot']),
                                        cat=video['genre'],
                                        year=video['year'],
                                        rating=video['imdbRating'],
                                        duration=video['duration'],
                                        director=video['director'],
                                        srt=video['id'],
                                        is_folder=False, 
                                        is_playable=True,
                                        total_items=1)

def print_video_error(video):
    print type(video['titel'])
    print video['titel']
    print 'your fucking titel is null in your db, fix it sweflix.'

def main(params):
    if not params.has_key('mode') or params['mode'] == 'categeories':
        
        logo = 'http://c3.cdn.sweflix.com/sweflxlogo2.png'
        categories = scraper.get_categories()
        for category, titel in categories.iteritems():
            utils.add_directory_link(titel.encode('utf-8'), 
                                     logo, 
                                     category, 
                                     '', 
                                     is_folder=True, 
                                     is_playable=False, 
                                     total_items=20)

    elif params['mode'] == 'ltst':
        videos = scraper.get_all_movies()
        for vid in videos:
            video = scraper.get_video_information(vid)
            try:
                add_video(video)
            except TypeError:
                print_video_error(video)

    elif params['mode'] == 'rec':
        videos=scraper.get_all_movies()
        for vid in videos:
            video = scraper.get_video_information(vid)
            if video['rek'] == '1':
                try:
                    add_video(video)
                except TypeError:
                    print_video_error(video)

    elif params['mode'] == 'pplr':
        videos=scraper.get_all_movies_views()
        for vid in videos:
            video = scraper.get_video_information(vid)
            try:
                add_video(video)
            except TypeError:
                print_video_error(video)
                
    elif params['mode'] == 'alpha':
        videos=scraper.get_all_movies_alpha()
        for vid in videos:
            video = scraper.get_video_information(vid)
            try:
                add_video(video)
            except TypeError:
                print_video_error(video)

    elif params['mode'] == 'play_video':
        utils.play_video(params['url'])
        subtitles=scraper.get_video_subtitle(params['srt'])
        player = xbmc.Player()
        while not xbmc.Player().isPlaying():
            xbmc.sleep(1000)
        player.setSubtitles(subtitles)
    utils.end_directory()

if __name__ == '__main__':
    params = utils.get_params()
    main(params)
