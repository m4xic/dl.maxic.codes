import flask
from flask import request, send_file
import tweepy
import dotenv
import os
from urllib.parse import urlparse
from tweepy.errors import TweepyException
import youtube_dl
from sys import exit
import re
import requests
import io
from youtube_dl.utils import RegexNotFoundError
import random
import string
import glob

del_list = glob.glob("dlm-*")
for del_file in del_list: os.remove(del_file)

dotenv.load_dotenv()

# Flask setup
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Tweepy setup
try:
    auth = tweepy.OAuthHandler(os.getenv('twitter_consumer_key'), os.getenv('twitter_consumer_secret'))
    auth.set_access_token(os.getenv('twitter_access_token'), os.getenv('twitter_access_token_secret'))
    tweep = tweepy.API(auth)
except TweepyException as e:
    print(f"Could not log in to Twitter API! {e.reason}")
    exit(1)

@app.route('/', methods=['GET'])
def home():
    return "I'm a teapot", 418

@app.route('/v1/get_url', methods=['POST'])
def get():
    if 'key' not in request.form:
        return "Missing API key", 401
    
    if request.form.get('key') != os.getenv('DL_API_KEY'):
        return "Invalid API key", 403

    if 'url' not in request.form:
        return "Missing url in request", 400
    
    url = request.form.get('url')
    # Twitter
    if urlparse(url).netloc.endswith('twitter.com'):
        try:
            twitter_id = re.search('[0-9]+', url.split('/status/')[1]).group(0)
            status = tweep.get_status(twitter_id)
            if "media" not in status._json['extended_entities']: return "No media in Twitter URL", 400
            media = status._json['extended_entities']['media'][0]
            if media['type'] != "video": return "No video in Twitter URL", 400
            
            var = media['video_info']['variants']
            for x in range(0, len(var)):
                print(x)
                if 'bitrate' not in var[x]: var.pop(x)

            var = sorted(var, key=lambda d: d['bitrate'], reverse=True)
            video = requests.get(var[0]['url'], allow_redirects=True)
            f = io.BytesIO(video.content)
            return send_file(f, mimetype="video/mp4")

        except RegexNotFoundError:
            return "No Twitter status ID found", 400
        except TweepyException:
            return "Twitter API error", 502
        except Exception as e:
            print(e)
            return "Some other error!", 500
    # All others
    else:
        try:
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
            with youtube_dl.YoutubeDL({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'outtmpl': f'dlm-{name}',}) as ydl:
                result = ydl.download([url])
            return send_file(f'dlm-{name}.mp4')
        except Exception as e:
            print(e)
            return "Some other error!", 500

app.run(host="0.0.0.0")
