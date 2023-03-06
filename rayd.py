import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

ydl_opts_default = {
    'download_archive': './yt_dlp_archive',
    'outtmpl': '%(title)s.%(ext)s',
    'paths': {
        'home': '~/Youtube'
    },
    'windowsfilename': True
}


ydl_opts_playlist = {
    'download_archive': ydl_opts_default['download_archive'],
    'outtmpl': '%(playlist_uploader)s/%(playlist)s/' + ydl_opts_default['outtmpl'],
    'paths': {
        'home': ydl_opts_default['paths']['home']},
    'windowsfilename': ydl_opts_default['windowsfilename']}

playlist_file = open('playlists.txt', 'r', encoding='utf8')
for link in playlist_file:
    with YoutubeDL(ydl_opts_playlist) as yt_dl:
        yt_dl.download([link])


ydl_opts_channel = {
    'download_archive': ydl_opts_default['download_archive'],
    'outtmpl': '%(uploader)s/' + ydl_opts_default['outtmpl'],
    'paths': {
        'home': ydl_opts_default['paths']['home']},
    'windowsfilename': ydl_opts_default['windowsfilename']}

feed_file = open('rss.txt', 'r', encoding='utf8')
for line in feed_file:
    request_response = requests.get(line, timeout=60)
    request_response.raise_for_status()
    xml_tree = BeautifulSoup(request_response.text, 'xml')

    for video in xml_tree.find_all('entry'):
        video_link = video.link.get('href')
        with YoutubeDL(ydl_opts_channel) as yt_dl:
            yt_dl.download([video_link])

feed_file.close()
