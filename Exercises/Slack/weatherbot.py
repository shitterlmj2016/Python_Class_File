import os
import time
import re
import requests
import json
from slackclient import SlackClient
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('../../_secret') / 'slackbot.env'
load_dotenv(dotenv_path=env_path)

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# instantiate Slack client
slack_client = SlackClient(os.getenv('BOT_USER_OAUTH_ACCESS_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def get_weather(command, match):
    print(command, match.groups)
    city = match[2] if match[2] else match[3] if match[3] else None
    if not city:
        return "Did you forget the city name?"

    options = {
        'protocol': 'https:',
        'host': 'api.openweathermap.org',
        'path': '/data/2.5/?weatherq={}&appid={}'.format(city, WEATHER_API_KEY),
        'port': 80,
        'method': 'GET'
    }

    url = '{}//{}/{}'.format(options['protocol'], options['host'], options['path'])
    print(url)
    s = requests.Session()
    r = s.get(url)
    
    reactions = {
        'clear': {'reaction': 'mostly_sunny', 'message': 'It\'s good idea to wear sunglasses before going out'},
        'cloud': {'reaction': 'cloud', 'message': ''},
        'clouds': {'reaction': 'cloud', 'message': ''},
        'smoke': {'reaction': 'smoking', 'message': ''},
        'rain': {'reaction': 'rain_cloud', 'message': 'Don\'t forget your umbrella.'},
        'thunderstorm': {'reaction': 'rain_cloud', 'message': 'Don\'t go outside.'},
    }

    weather = json.loads(r.content)
    if 'weather' in weather is not None and weather['weather'][0] is not None and weather['weather'][0]['main'] is not None:
        weather_conditions = weather['weather'][0]['main'].lower()
        bot_response = "It's {} in {}.".format(weather_conditions, city)
        bot_reaction = reactions[weather_conditions] if weather_conditions in reactions else None
        if bot_reaction is not None:
            bot_response = "{} :{}: {}".format(bot_response, bot_reaction['reaction'], bot_reaction['message'])
    else:
        bot_response = 'I\'m sorry I can\'t find the weather for {}'.format(city)
    return bot_response


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    match = re.match('(.*weather in\s+(.*)|(.*)\s+weather.*)', command, flags=re.MULTILINE | re.IGNORECASE)
    # Finds and executes the given command, filling in response
    bot_response = None
    bot_reaction = None
    # This is where you start to implement more commands!
    if match:
        bot_response = get_weather(command, match)
    else:
        bot_response = "Wha?"
    
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=bot_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")