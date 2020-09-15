import youtube_dl 
import os
import json
from youtube_search import YoutubeSearch
from IPython.display import YouTubeVideo
from ast import literal_eval
from datetime import datetime


#download youtube/vimeo video given the url and the destination path
def download_videos(links, dest_path):
    for link in links:
        os.system(f"youtube-dl --force-ipv4 -o '{dest_path}/%(id)s.%(ext)s' {link} -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'")

#alternate method
def alt_download_videos(links, dest_path):
    for v in links:
        ydl_opts = {
            'outtmpl': f'{dest_path}/%(title)s-%(id)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([v])


#download WebVTT file(subtitle) of youtube/vimeo video given the url
def generate_vtt(video_url):
    try:
        print("Downloading English subtitle")
        os.system(f'youtube-dl {video_url} --skip-download --write-sub --write-auto-sub --sub-lang en')
        
    except Exception as e:
        print("Other language")
        os.system(f'youtube-dl {video_url} --skip-download --write-sub --write-auto-sub')
        

#youtube search module for searching given number of videos for a given search term
def search_videos(search_term, max_results):
    results = YoutubeSearch(search_term, max_results=search_term).to_json()
    parse_results = json.loads(results)
    print(json.dumps(parse_results, indent=4, sort_keys=True))


#read the webVTT file downloaded
def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def read_vtt_file(vtt_filename):
    last_text = ""
    for caption in webvtt.read(vtt_filename):
        if (get_sec(caption.end) - get_sec(caption.start)) > 0.011:
            a = datetime.strptime(caption.start , '%H:%M:%S.%f')
            print(caption.start)
            print(caption.text.strip().replace(last_text,"").strip())
            last_text = caption.text.strip().replace(last_text,"").strip()
            print(caption.end)
            print("###########")

#Play the video with its' video id on ipython notebook
# YouTubeVideo('q9j1LJIP4VQ')