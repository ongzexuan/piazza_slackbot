"""
Ze Xuan Ong
15 Jan 2019

Adapted from t-davidson's piazza-slackbot
URL: https://github.com/t-davidson/piazza-slackbot/blob/master/slackbot.py

This is a simple Slackbot that will poll Piazza every minute

Every time a new post is observed a notification will be sent out
"""

import os
import re

from piazza_api import Piazza
from slacker import Slacker
from time import sleep
from dotenv import load_dotenv, find_dotenv


# Config object to collect all required environment and config vars
class Config():

    # Environment variables
    PIAZZA_ID = ""          # Piazza forum id
    PIAZZA_EMAIL = ""       # User account email
    PIAZZA_PASSWORD = ""    # User account password
    SLACK_TOKEN = ""        # Slack API token
    SLACK_CHANNEL = ""      # Slack channel name
    SLACK_BOT_NAME = ""     # Slack bot name    

    def __init__(self, pid, pemail, ppass, stoken, schannel, sbot):
        self.PIAZZA_ID = pid
        self.PIAZZA_EMAIL = pemail
        self.PIAZZA_PASSWORD = ppass
        self.SLACK_TOKEN = stoken
        self.SLACK_CHANNEL = schannel
        self.SLACK_BOT_NAME = sbot        


# Main method
def main():

    # Read all relevant config variables
    conf = config_env()

    # Setup Piazza
    piazza = Piazza()
    piazza.user_login(email=conf.PIAZZA_EMAIL, password=conf.PIAZZA_PASSWORD)
    network = piazza.network(conf.PIAZZA_ID)

    # Setup Slack
    bot = Slacker(conf.SLACK_TOKEN)

    # Get the last posted_id
    last_id = get_max_id(network.get_feed()['feed'])
    post_base_url = "https://piazza.com/class/{}?cid=".format(conf.PIAZZA_ID)
    
    # Run loop
    check_for_new_posts(network, bot, conf.SLACK_BOT_NAME, 
                        conf.SLACK_CHANNEL, last_id, post_base_url)


# Collect env vars
def config_env():

    # Get environment variables from .env file if exists
    load_dotenv(find_dotenv())

    # Piazza specific
    PIAZZA_ID = os.getenv("PIAZZA_ID")
    PIAZZA_EMAIL = os.getenv("PIAZZA_EMAIL")
    PIAZZA_PASSWORD = os.getenv("PIAZZA_PASSWORD")

    if not PIAZZA_ID or not PIAZZA_EMAIL or not PIAZZA_PASSWORD:
        print("Missing Piazza credentials")
        exit(1)

    # Slack specific
    SLACK_TOKEN = os.getenv("SLACK_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
    SLACK_BOT_NAME = os.getenv("SLACK_BOT_NAME")

    if not SLACK_TOKEN or not SLACK_CHANNEL or not SLACK_BOT_NAME:
        print("Missing Slack credentials")
        exit(1)

    return Config(PIAZZA_ID, PIAZZA_EMAIL, PIAZZA_PASSWORD,
                  SLACK_TOKEN, SLACK_CHANNEL, SLACK_BOT_NAME)


# This method exploits the fact that pinned posts have the field
# 'pin: 1' and non-pinned ones don't. So we can return the first
# non-pinned post id
def get_max_id(feed):
    for post in feed:
        if "pin" not in post:
            return post["nr"]
    return -1


# Method that polls Piazza in constant interval and posts new posts
# to Slack
def check_for_new_posts(network, bot, bot_name, channel, last_id,
                        post_base_url, interval=60, include_link=True):
    LAST_ID = last_id

    # Keep looping
    while True:
        try:
            UPDATED_LAST_ID = get_max_id(network.get_feed()['feed'])

            # For all the new posts
            while UPDATED_LAST_ID > LAST_ID:

                LAST_ID += 1

                # Fetch post
                post = network.get_post(LAST_ID)
                if not post.get('history', None):
                    continue
                subject = post['history'][0]['subject']
                content = re.findall(r'<p>(.*?)</p>', post['history'][0]['content'])[0]

                # Create message and attach relevant parts
                attachment = None
                message = None
                if include_link is True:
                    attachment = [
                        {
                            "fallback": "New post on Piazza!",
                            "title": subject,
                            "title_link": post_base_url + str(UPDATED_LAST_ID),
                            "text": content,
                            "color": "good"
                        }
                    ]
                else:
                    message = "New post on Piazza!"

                # Post message
                bot.chat.post_message(channel,
                                      message,
                                      as_user=bot_name,
                                      parse='full',
                                      attachments=attachment)
            print("Slack bot is up!")
            sleep(interval)
        except:
            print("Error when attempting to get Piazza feed, going to sleep...")
            sleep(interval)

# Main
if __name__ == '__main__':
    main()

