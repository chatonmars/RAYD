# RAYD - RSS Automatic Youtube Downloader

A Python script to download latest videos from Youtube channels

- [Installation](https://github.com/chatonmars/RAYD#installation)
- [Usage](https://github.com/chatonmars/RAYD#usage)
- [Bug Report & Suggestions](https://github.com/chatonmars/RAYD#Bug-Report-&-Suggestions)

## Installation

- Download the script, rss feed file and playlist url file [here](https://github.com/chatonmars/RAYD/releases/latest)
- Install Python and pip
- Install required dependencies with ```python -m pip install requirements.txt```

## Usage

To use this script you will need to put RSS feeds from the Youtube channel you want in 'rss.txt'.
You can find the RSS feed of a channel by opening the source code of the Youtube page on the channel.
It is in a link tag with the title 'RSS', the link should look like the example in '[rss.txt](https://github.com/chatonmars/RAYD/blob/main/rss.txt)'.
You can also put URL of Youtube playlists in 'playlist.txt' and it will download every video in the playlist.
RSS feeds from Youtube give the last 15 videos from a channel, when the script run it will check those videos and download the ones it never downloaded.
When running the script you can add the argument ```--download_folder``` and a path to choose the folder where the videos will be downloaded.
It is recommended to run this script in a scheduled task on Windows or a cron job in Linux in order to fully automatized it.

## Bug Report & Suggestions

This script was written and tested with Python 3.11 in a Windows
environment but should work with older Python 3 versions and in a Linux
environment.

If you find any bug or have any suggestions on how to improve this script or add features do not hesitate to create an issue.
