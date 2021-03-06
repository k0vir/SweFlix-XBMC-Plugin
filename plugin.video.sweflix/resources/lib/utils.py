import urllib2
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

# Add on info
__addon__        = xbmcaddon.Addon()
__addon_id__     = __addon__.getAddonInfo('id')
__addon_id_int__ = int(sys.argv[1])
__addon_dir__    = xbmc.translatePath(__addon__.getAddonInfo('path'))
__translation__    = __addon__.getLocalizedString

def get_params():
    """Return a dictionary of parameters collected from the plugin URL"""
    params = {}
    paramstring = sys.argv[2]
    # Check params exist
    if len(paramstring)>=2:
        all_params = sys.argv[2]
        # If there's a final slash, remove it
        if (all_params[len(all_params)-1]=='/'):
            all_params = all_params[0:len(all_params)-2]
        # Remove the '?'
        all_params = all_params.replace('?', '')
        # split param string into individual params
        pair_params = all_params.split('&', 3)

        for p in pair_params:
            split = p.split('=')
            # Set dictionary mapping of key : value
            try:
              params[split[0]] = split[1]
            except:
              print 'Exception fucntion get_params in utils.py'

    return params

def add_directory_link(title, thumbnail, mode, url=None, is_folder=True, 
                       is_playable=False, total_items=0, plot=None, cat=None, 
                       year=None, rating=None, duration=None, director=None, srt=None):
    """Return addDirectoryItem method"""
    final_url = "{0}?mode={1}&title={2}".format(sys.argv[0], 
                                                mode, 
                                                title)
    if srt:
        final_url += "&srt={0}".format(srt)
    if url:
        final_url += "&url={0}".format(url)

    list_item = xbmcgui.ListItem(title,
                                 '',
                                 thumbnail,
                                 thumbnail)
    if is_playable:
        list_item.setProperty('IsPlayable', 'true') 
    list_item.setInfo('video', {'plot': plot, 'genre': cat, 'year': year, 'rating': rating, 'duration': duration, 'director':director})
    return xbmcplugin.addDirectoryItem(__addon_id_int__, 
                                       final_url, 
                                       list_item, 
                                       isFolder=is_folder, 
                                       totalItems=total_items) 

def add_next_page(mode, url, page_no):
    """Return addDirectoryItem method for Next Page"""
    final_url = "{0}?mode={1}&url={2}&page={3}".format(sys.argv[0], 
                                                          mode, 
                                                          url,
                                                          page_no)
    nxt=__translation__(30001)
    list_item = xbmcgui.ListItem(nxt)

    return xbmcplugin.addDirectoryItem(__addon_id_int__, 
                                       url=final_url, 
                                       listitem=list_item, 
                                       isFolder=True, 
                                       totalItems=5)
def play_video(url):
    """Return setResolvedUrl method to play a video"""
    list_item = xbmcgui.ListItem(path=url)
    return xbmcplugin.setResolvedUrl(handle=__addon_id_int__,
                                     succeeded=True,
                                     listitem=list_item)

def end_directory():
    """Return endOfDirectory method """
    return xbmcplugin.endOfDirectory(__addon_id_int__)