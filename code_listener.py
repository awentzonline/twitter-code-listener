import argparse
import json
import os
import sys
import time
from cStringIO import StringIO

import requests
import tweepy
import zbar
from PIL import Image


class ImageStreamListener(tweepy.StreamListener):
    def __init__(self, config, *args, **kwargs):
        super(ImageStreamListener, self).__init__(*args, **kwargs)
        self.n_images = 0
        self.url_cache = {}
        self.config = config
        self.scanner = zbar.ImageScanner()
        self.scanner.parse_config('enable')

    def on_status(self, status):
        status_media = status.entities.get('media', [])
        if (self.n_images + 1) % 100 == 0:
            print('Processed {} images'.format(self.n_images + 1))
        for media in status_media:
            self.n_images += 1
            url = media['media_url']
            if url in self.url_cache:
                continue
            print(url)
            self.url_cache[url] = True
            response = requests.get(url)
            img_io = StringIO(response.content)
            img = Image.open(img_io)
            codes = self.find_codes(img)
            if codes:
                print('found codes', self.n_images, codes)
                prefix = os.path.join(self.config.output_path, str(self.n_images))
                img.save('{}.jpg'.format(prefix))
                with open('{}.json'.format(prefix), 'wb') as outfile:
                    data = dict(
                        code=codes,
                        tweet='https://twitter.com/statuses/{}'.format(status.id))
                    json.dump(data, outfile)
                # status_parts = [url]
                # for code_type, code_value in codes:
                #     status_parts.append('{}:{}'.format(code_type, code_value))
                # self.api.update_status(' '.join(status_parts))

    def find_codes(self, img):
        img = img.convert('L')
        raw = img.tobytes()
        w, h = img.size
        zimg = zbar.Image(w, h, 'Y800', raw)
        self.scanner.scan(zimg)
        found = []
        for symbol in zimg:
            found.append([str(symbol.type), str(symbol.data)])
        return found

    def on_error(self, status_code):
        if status_code == 420:
            t_chill = 15 * 60.  # 15 minutes
            print('Enhancing chill for {} seconds'.format(t_chill))
            time.sleep(t_chill)


def setup_auth():
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    key = os.getenv('TWITTER_ACCESS_TOKEN')
    secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    return auth


def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', default='found/')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    config = get_config()
    auth = setup_auth()
    print('Starting bot...')
    listener = ImageStreamListener(config, api=tweepy.API(auth))
    while True:
        try:
            stream = tweepy.Stream(auth=auth, listener=listener)
            stream.filter(track='jpg png jpeg'.split())
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            print('An error occurred:', sys.exc_info())
            continue
