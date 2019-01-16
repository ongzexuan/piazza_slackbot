# Piazza Slackbot

Simple slackbot that polls Piazza every minute for new posts and posts their content to the Piazza channel on Slack with a link

## Installation and Deployment

### Slack

1. Under Administration > Manage Apps > Custom Integrations > Bots, create a new bot integration. It should require you to give a bot a username.
2. Decide on which channel the bot should post to and then add the bot to the channel. The bot cannot post if it is not already in the channel.

### Deployment

The bot needs to run somewhere. A free tier Heroku deployment would suffice.

1. Create a new app on Heroku. You can do this either via the Heroku CLI or using the web interface. Follow the instructions to create a local Heroku git repo.
2. The required environment variables can be found on in `.env.template`. Fill in the corresponding fields on the app deployment (this is so that we don't put confidential credentials in the program itself)
3. Follow the deployment instructions provided by Heroku

The supporting files required for Heroku deployment are provided, you can modify them if you wish. Their functions are roughly listed below:

`Procfile` - specifies to Heroku the type of application and the instruction to run
`requirements.txt` - packages/dependencies to install
`runtime.txt` - which version of Python we are using


### Local Deployment

You can also run the bot on your local machine for testing purposes.

1. Create a `.env` file from the `.env.template` and fill it up with your own credentials
2. Install the required packages using `pip install -r requirements.txt`. Using a virtualenv is recommended to isolate dependencies
3. Run the bot with `python piazza_bot.py`

If everything goes well, the bot should print a relatively healthy message every minute


## Credits

Inspired by [t-davidson's piazza-slackbot](https://github.com/t-davidson/piazza-slackbot). Modified the handling of env variables, as rewriting the logic for pulling new posts.

https://github.com/t-davidson/piazza-slackbot/blob/master/slackbot.py
