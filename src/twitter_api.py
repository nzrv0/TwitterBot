import tweepy
import os
import tweepy.errors
from custom_logger import logger
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
token = os.getenv("ACCESS_TOKEN")
secret = os.getenv("ACCESS_SECRET")
bearer = os.getenv("BEARER_TOKEN")


def post_media(technique, file_name):

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, token, secret)
    api = tweepy.API(auth)

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        bearer_token=bearer,
        access_token=token,
        access_token_secret=secret,
    )
    file_name = f"{file_name}.gif"

    media = api.media_upload(filename=file_name)
    tweet = f"{technique.title()} technique"

    try:
        response = client.create_tweet(
            text=tweet, media_ids=[str(media.media_id_string)]
        )
    except tweepy.errors.BadRequest as err:
        logger.error(f"Cannot post file: {err}")
        raise RuntimeError(f"Cannot post file: {err} id-{media.media_id_string}")
    except tweepy.errors.TooManyRequests:
        logger.warning("Program has been stop due too many request for 2 hours")
        time.sleep(60 * 60 + 15 * 60)
        post_media(technique, file_name)

    else:
        logger.info(f"File has uploaded to twitter {response}")
