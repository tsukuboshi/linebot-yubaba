import os
import urllib
import json
import random

import logging

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    channel_access_token = get_channel_access_token()
    channel_secret = get_channel_secret()
    line_bot_api = LineBotApi(channel_access_token)
    handler = WebhookHandler(channel_secret)

    headers = event["headers"]
    body = event["body"]
    signature = headers['x-line-signature']

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(line_event):
        input_text = line_event.message.text
        newName = random.choice(input_text)
        reply_word = f"フン。{input_text}というのかい。贅沢な名だねぇ。 今からお前の名前は{newName}だ。いいかい、{newName}だよ。分かったら返事をするんだ、{newName}!!"

        line_bot_api.reply_message(
            line_event.reply_token,
            TextSendMessage(text=reply_word))

    try:
        handler.handle(body, signature)

    except Exception as e:
        logger.exception("Exception occurred: %s", e)
        raise e


def get_channel_access_token():
    line_channel_access_token_path = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    print("Loading AWS Systems Manager Parameter Store values from " + line_channel_access_token_path)
    req = urllib.request.Request('http://localhost:2773/systemsmanager/parameters/get/?name=' + line_channel_access_token_path + '&withDecryption=true')
    req.add_header('X-Aws-Parameters-Secrets-Token', os.environ.get('AWS_SESSION_TOKEN'))
    line_channel_access_token_config = urllib.request.urlopen(req).read()
    line_channel_access_token = json.loads(line_channel_access_token_config.decode("utf-8"))['Parameter']['Value']
    return line_channel_access_token


def get_channel_secret():
    line_channel_secret_path = os.environ['LINE_CHANNEL_SECRET']
    print("Loading AWS Systems Manager Parameter Store values from " + line_channel_secret_path)
    req = urllib.request.Request('http://localhost:2773/systemsmanager/parameters/get/?name=' + line_channel_secret_path + '&withDecryption=true')
    req.add_header('X-Aws-Parameters-Secrets-Token', os.environ.get('AWS_SESSION_TOKEN'))
    line_channel_secret_config = urllib.request.urlopen(req).read()
    line_channel_secret = json.loads(line_channel_secret_config.decode("utf-8"))['Parameter']['Value']
    return line_channel_secret
