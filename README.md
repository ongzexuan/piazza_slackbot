# Piazza Slackbot

Simple slackbot that polls Piazza every minute for new posts and posts their content to the Piazza channel on Slack with a link

## Installation and Deployment

### Slack

1. Under Administration > Manage Apps > Custom Integrations > Bots, create a new bot integration. It should require you to give a bot a username.
2. Decide on which channel the bot should post to and then add the bot to the channel. The bot cannot post if it is not already in the channel.

### Deployment

The bot needs to run somewhere. A free tier heroku deployment would suffice.

The required environment variables can be found on in `.env.template`


### Local Deployment

You can also run the bot on your local machine for testing purposes.

1. Create a `.env` file from the `.env.template` and fill it up with your own credentials
2. Install the required packages using `pip install -r requirements.txt`. Using a virtualenv is recommended to isolate dependencies
3. Run the bot with `python piazza_bot.py`

If everything goes well, the bot should print a relatively healthy message every minute

