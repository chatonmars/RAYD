import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL

ydl_opts_default = {
    'download_archive': './yt_dlp_archive',
    'outtmpl': '%(title)s.%(ext)s',
    'paths': {
        'home': '~\\Youtube'
    }
}

feed_file = open('rss.txt', 'r', encoding='utf8')
for _, line in enumerate(feed_file):
    request_response = requests.get(line, timeout=60)
    request_response.raise_for_status()
    xml_tree = BeautifulSoup(request_response.text, 'xml')

    uploader = xml_tree.title
    if uploader is None:
        break
    uploader_name = uploader.get_text()
    ydl_opts = {
        'download_archive': ydl_opts_default['download_archive'],
        'outtmpl': ydl_opts_default['outtmpl'],
        'paths': {
            'home': ydl_opts_default['paths']['home'] + '\\' + uploader_name
        }
    }

    for video in xml_tree.find_all('entry'):
        video_link = video.link.get('href')
        with YoutubeDL(ydl_opts) as yt_dl:
            yt_dl.download([video_link])

feed_file.close()
