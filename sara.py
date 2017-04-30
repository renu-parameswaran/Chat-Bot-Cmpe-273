import os
import time
from slackclient import SlackClient
import log
import botController
import config

# instantiate Slack & Twilio clients
slack_client =  SlackClient(config.appKey)

def getBotID():
    log.writetofile("entering getBotID function")
    BOT_NAME = "sara_sjsu"
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                log.writetofile("found bot user "+ BOT_NAME)
                return user.get('id')
    else:
        log.writetofile("could not find bot user with the name " + BOT_NAME)

def send_message(channel_id, message):
    log.writetofile("posting reponse to channel: "+channel_id)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        as_user=True,
        icon_emoji=':robot_face:'
    )

def handle_command(userInput, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    log.writetofile("entering handle command function")
    log.writetofile("User Input: " + userInput)
    response = botController.currentWorkingMode(userInput)
    print response
    log.writetofile("bot reply: " + response)
    send_message(channel, response)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

BOT_ID = getBotID()

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

def slackListeToChannel():
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        log.writetofile("StarterBot connected and running!")
        print("StarterBot connected and running!")
        send_message(config.channel,config.initialDisplayMessage)
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel and channel==config.channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        log.writetofile("Connection failed. Invalid Slack token or bot ID?")
        print("Connection failed. Invalid Slack token or bot ID?")