# -*- coding: utf-8 -*-

import urllib, urllib2, re, sys
import xbmcplugin, xbmcgui

def getHTML(url):
    conn = urllib2.urlopen(urllib2.Request(url + urllib.urlencode({})))
    html = conn.read()
    conn.close()
    
    return html 

def Categories():
    url = 'http://ororo.tv'
    html = getHTML(url)
    genre_links = re.compile('<a href="(.+?)" class="name">(.+?)</a>').findall(html.decode('utf-8'))

    for link, title in genre_links:
        addDir(title, url + link, 20)

def Movies(url):
    html = getHTML(url)
    genre_links = re.compile('<a href="(.+?)" class="episode" data-episode-id="(.+?)" data-href="(.+?)">(.+?)</a>').findall(html.decode("utf-8").encode('ascii', 'ignore'))

    for href, episode_id, link, title  in genre_links:
        addDir(title, 'http://ororo.tv' + link, 30)

def Videos(url, title):
    html = getHTML(url)
    link = re.compile("<source src='(.+?)' type='video/mp4'>").findall(html.decode('utf-8')) [0]

    addLink(title, 'http://ororo.tv' + link)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                            
    return param

def addLink(title, url):
    item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)


def addDir(title, url, mode):
    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))

    item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)

params = get_params()
url    = None
title  = None
mode   = None

try:    title = urllib.unquote_plus(params['title'])
except: pass

try:    url = urllib.unquote_plus(params['url'])
except: pass

try:    mode = int(params['mode'])
except: pass

if mode == None:
    Categories()

elif mode == 20:
    Movies(url)

elif mode == 30:
    Videos(url, title)

xbmcplugin.endOfDirectory(int(sys.argv[1]))