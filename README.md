Twitter Code Listener
=====================
Find codes (QR, UPC, and more) in images posted on Twitter.

Usage
-----
* `pip install -r requirements.txt`
* Make sure the following environment variables are set:
```
TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```
* `python code_listener.py`

I had issues installing `zbar` on OSX so there is a simple
docker compose setup:
* Make sure the following environment variables are set (or edit `docker-compose.yml`):
```
TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```
* `docker-compose up`
