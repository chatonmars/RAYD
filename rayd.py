"""RAYD - RSS Automatic Youtube Downloader

This script downloads from Youtube the latest videos of a channel via
its RSS feed. It can also download videos from a playlist via its URL.

The script looks for RSS feeds of Youtube channels in './rss.txt' and
for URL of Youtube playlists in './playlists.txt'. There should be one
link per line.

This script was written and tested with Python 3.11 in a Windows
environment but should work with older Python 3 versions and in a Linux
environment.

This script requires that 'requests', 'beautifulsoup4', and 'yt-dlp' be
installed within the Python environment you are running this script in,
they can be installed with pip.
"""

import logging
import argparse
import os

import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL


parser = argparse.ArgumentParser(
    prog='RAYD - RSS Automatic Youtube Downloader',
    description='Download automatically new videos from Youtube using RSS feeds')
parser.add_argument(
    '-f',
    '--download_folder',
    default='~/RAYD_Downloads',
    type=str,
    help='Path to the folder where videos will be downloaded')
args = parser.parse_args()

if not os.path.exists(args.download_folder):
    print('Download folder\'s path not viable')
    exit()


# Config for the Root Logger Object
logging.basicConfig(
    filename='rayd.log',
    encoding='utf-8',
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y/%m/%d %I:%M:%S %p',
    level=logging.INFO)
logging.info('Script starting')

# Default yt-dlp config
ydl_opts_default = {
    'download_archive': './yt_dlp_archive',
    'outtmpl': '%(title)s.%(ext)s',
    'paths': {
        'home': args.download_folder
    },
    'windowsfilename': True,
    'ignoreerrors': True,
    'logger': logging.getLogger()}


# Deep copy default config and change the naming template of the
# downloaded files to place them in a folder named after the playlist
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


# Deep copy default config and change the naming template of the
# downloaded files to place them in a folder named after the uploader
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
    # Check if request failed and continue to next link if so
    if request_response.status_code != 200:
        logging.error(
            '%d: %s // For link: %s',
            request_response.status_code, request_response.reason, rss_link)
        continue
    xml_tree = BeautifulSoup(request_response.text, 'xml')

    # In a Youtube RSS feed 'entry' represent a video
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
logging.shutdown()
