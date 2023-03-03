import sqlite3
import requests
from bs4 import BeautifulSoup

db_connection = sqlite3.connect('history.db')
feed_file = open('rss.txt', 'r', encoding='utf8')
for _, line in enumerate(feed_file):
    request_response = requests.get(line, timeout=60)
    request_response.raise_for_status()
    xml_tree = BeautifulSoup(request_response.text, 'xml')

    uploader = xml_tree.title
    if uploader is None:
        break
    uploader_name = uploader.get_text()

    for video in xml_tree.find_all('entry'):
        video_id_tag = video.find('yt:videoId')
        video_id = video_id_tag.get_text()
        cursor = db_connection.execute(
            'SELECT * FROM "DOWNLOADED-VIDEOS" WHERE "ID"=?', [video_id])
        if cursor.fetchone() is not None:
            break

        video_link = video.link.get('href')
        # Download command
        db_connection.execute(
            'INSERT INTO "DOWNLOADED-VIDEOS" VALUES (?)', [video_id])
        db_connection.commit()

feed_file.close()
db_connection.close()
