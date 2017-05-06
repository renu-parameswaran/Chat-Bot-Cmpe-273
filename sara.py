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

def send_image(channel_id,attachments):
    log.writetofile("posting response image to channel: "+channel_id)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text="",
        attachments =attachments,
        as_user=True,
        icon_emoji=':robot_face:'
    )

def handle_command(userInput, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    log.writetofile("entering handle command function")
    log.writetofile("User Input: " + userInput)
    response,image_url = botController.currentWorkingMode(userInput)
    print response
    log.writetofile("bot reply: " + response)
    user = '<@{user}>'.format(user=user)
    send_message(channel,"Hi" + user + "!. "+response)
    if (image_url!="none"):
        attachments = [{"title":response,"image_url": image_url}]
        send_image(channel,attachments)
        log.writetofile("Sending Image")
    else:
        log.writetofile("No Image to be sent")

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            #print output
            if output and 'text' in output:
                return output['text'], output['channel'],output['user']
    return None, None, None

BOT_ID = getBotID()

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

def slackListeToChannel():
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        log.writetofile("Sara is up and running!")
        print("Sara is up and running running!")
        greetings = botController.getMessage()
        send_message(config.channel,greetings + config.initialDisplayMessage)
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and channel==config.channel and user!="U4P2K7U07":
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        log.writetofile("Connection failed. Invalid Slack token or bot ID?")
        print("Connection failed. Invalid Slack token or bot ID?")
