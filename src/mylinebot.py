import os
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))


def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    signature = headers['x-line-signature']

    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    input_text = event.message.text
    newName = random.choice(input_text)
    reply_word = f"フン。{input_text}というのかい。贅沢な名だねぇ。 今からお前の名前は{newName}だ。いいかい、{newName}だよ。分かったら返事をするんだ、{newName}!!"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_word))
