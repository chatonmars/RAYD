import logging
import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

logging.basicConfig(
    filename='rayd.log',
    encoding='utf-8',
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y/%m/%d %I:%M:%S %p',
    level=logging.INFO)
logging.info('Script starting')

ydl_opts_default = {
    'download_archive': './yt_dlp_archive',
    'outtmpl': '%(title)s.%(ext)s',
    'paths': {
        'home': '~/Youtube'
    },
    'windowsfilename': True,
    'ignoreerrors': True,
    'logger': logging.getLogger()}


ydl_opts_playlist = {
    'download_archive': ydl_opts_default['download_archive'],
    'outtmpl': '%(playlist_uploader)s/%(playlist)s/' + ydl_opts_default['outtmpl'],
    'paths': {
        'home': ydl_opts_default['paths']['home']},
    'windowsfilename': ydl_opts_default['windowsfilename'],
    'ignoreerrors': ydl_opts_default['ignoreerrors'],
    'logger': ydl_opts_default['logger']}

playlist_file = open('playlists.txt', 'r', encoding='utf8')
for link in playlist_file:
    with YoutubeDL(ydl_opts_playlist) as yt_dl:
        yt_dl.download([link])

playlist_file.close()


ydl_opts_channel = {
    'download_archive': ydl_opts_default['download_archive'],
    'outtmpl': '%(uploader)s/' + ydl_opts_default['outtmpl'],
    'paths': {
        'home': ydl_opts_default['paths']['home']},
    'windowsfilename': ydl_opts_default['windowsfilename'],
    'ignoreerrors': ydl_opts_default['ignoreerrors'],
    'logger': ydl_opts_default['logger']}

feed_file = open('rss.txt', 'r', encoding='utf8')
for line in feed_file:
    rss_link = line.strip()
    request_response = requests.get(rss_link, timeout=60)
    if request_response.status_code != 200:
        logging.error(
            '%d: %s // For link: %s',
            request_response.status_code, request_response.reason, rss_link)
        continue
    xml_tree = BeautifulSoup(request_response.text, 'xml')

    if xml_tree.find('entry') is None:
        logging.warning(
            'Link: %s seems to not correspond to a rss feed of a Youtube channel',
            rss_link)
        continue

    for video in xml_tree.find_all('entry'):
        video_link = video.link.get('href')
        with YoutubeDL(ydl_opts_channel) as yt_dl:
            yt_dl.download([video_link])

feed_file.close()

logging.info('Script ended')
