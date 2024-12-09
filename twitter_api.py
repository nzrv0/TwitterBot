import tweepy
import os
from dotenv import load_dotenv
import logging

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
token = os.getenv("ACCESS_TOKEN")
secret = os.getenv("ACCESS_SECRET")
bearer = os.getenv("BEARER_TOKEN")


def post_media(name):
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, token, secret)
    api = tweepy.API(auth)

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        bearer_token=bearer,
        access_token=token,
        access_token_secret=secret,
    )

    media = api.media_upload(filename=name)
    tweet = "Test Uploading Image"
    response = client.create_tweet(text=tweet, media_ids=[media.media_id])

    print(response)
