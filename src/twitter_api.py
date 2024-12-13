import tweepy
from tweepy.asynchronous import AsyncClient
import os
from custom_logger import logger
from dotenv import load_dotenv
import asyncio

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
token = os.getenv("ACCESS_TOKEN")
secret = os.getenv("ACCESS_SECRET")
bearer = os.getenv("BEARER_TOKEN")


async def post_media(technique, file_name):
    file_name = f"{file_name}.gif"
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, token, secret)
    api = tweepy.API(auth)

    client = AsyncClient(
        consumer_key=api_key,
        consumer_secret=api_secret,
        bearer_token=bearer,
        access_token=token,
        access_token_secret=secret,
    )

    media = api.media_upload(filename=file_name)
    tweet = f"{technique.title()} technique"

    response = await client.create_tweet(
        text=tweet, media_ids=[str(media.media_id_string)]
    )
    logger.info(f"File has uploaded to twitter {response}")
