# -*- coding: utf-8 -*-

import sys, urllib, re, os.path, datetime, time, urllib2, cookielib, urlparse
import xbmc, xbmcgui, xbmcplugin, xbmcvfs

from os.path import basename
from urlparse import urlsplit

base_url = 'http://ororo.tv'

def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url:
        localName = url2name(r.url)
    if localFileName:
        localName = localFileName
    f = open(localName, 'wb')
    f.write(r.read())
    f.close()

def get_html(url):
    conn = urllib2.urlopen(urllib2.Request(url + urllib.urlencode({})))
    html = conn.read()
    conn.close()
    return html

def categories():
    html = get_html(base_url)
    genre_links = re.compile('<a href="(.+?)" class="name">(.+?)</a>').findall(html.decode('utf-8'))
    for link, title in genre_links:
        display_row(title, u"{0}{1}".format(base_url, link), 20)

def movies(url):
    html = get_html(url)
    #example <a href="#1-1" class="episode" data-href="/en/shows/hannah-montana/videos/8183" data-id="8183" data-time="null">№1 Lilly, Do You Want to Know a Secret?</a>
    genre_links = re.compile('<a href="(.+?)" class="episode" data-href="(.+?)" data-id=(.+?)>(.+?)</a>').findall(html.decode("utf-8").encode('ascii', 'ignore'))
    for href, link, rubbish, title  in genre_links:
        display_row(title, u"{0}{1}".format(base_url, link), 30)

def videos(url, title):
    html = get_html(url)
    video_link = None
    video_links = re.compile("<source src='(.+?)' type='video/mp4'>").findall(html.decode('utf-8'))
    if len(video_links) > 0:
        video_link = video_links[0]
    sub_title = None
    sub_titles = re.compile("<track default='default' kind='captions' label='English' src='(.+?)' srclang='en'>").findall(html.decode('utf-8'))
    if len(sub_titles) > 0:
        sub_title = sub_titles[0]
    addLink(title + ":video", video_link, sub_title)

def get_params():
    if len(sys.argv) < 2:
        return
    parameters = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)
    #exemple of parameters : {'url': ['http://ororo.tv/en/shows/hannah-montana'], 'mode': ['20'], 'title': ['Hannah Montana']}
    #we want to remove the list in each values
    well_formed_param = dict()
    for key, value in parameters.iteritems():
        if len(value) > 0:
            well_formed_param[key] = value[0]
    return well_formed_param


def addLink(title, url=None, subtitle_url=None):
    pass
    # item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
    # item.setInfo( type='Video', infoLabels={'Title': title} )
    # item.setProperty('subtitle', subUrl)
    # xbmcplugin.display_rowectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)
    # xbmc.Player().setSubtitles('http://ororo.tv/uploads/video/subtitle/14012/The_Cleveland_Show_-_1x07_-_A_Brown_Thanksgiving.en.srt')

    #print "url: %s sub: %s" % (url, subtitle_url)
    if url:
        video_link = "{0}{1}".format(base_url, url)
        xbmc.Player().play(url)
        if subtitle_url:
            subtitle_link = "{0}{1}".format(base_url, subtitle_url)
            xbmc.Player().setSubtitles(subtitle_link)

def display_row(title, url, mode):
    parameters = {
                "title":title,
                "url": url,
                "mode": mode,
                }
    sys_url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    #print for debug
    #print u"%s %s" % (title, sys_url)
    item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )
    xbmcplugin.display_rowectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)

params = get_params()

title = params.get('title', None)
url = params.get('url', None)
mode = int(params.get('mode', 0))

if mode == None:
    categories()

elif mode == 20:
    movies(url)

elif mode == 30:
    videos(url, title)

xbmcplugin.endOfDirectory(int(sys.argv[1]))