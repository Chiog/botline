from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('m0v5zVz8LTLNgnT8q40sTaqW8QnNPk5r/HPucZJ9lZ2BLt9B2Um/pFNsRSNJx6Mqhz1Sh3OYc/9CknSM0ONeSq8Vxh1IbQfEuqHfdtBF/+MYqRXXjzLfcJlgXEpxtItIi3pHLkVqtemwtDDqUKyeNAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f924288068b86649d555531365bde00')

#網址後callback 這邊會被執行
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, #要給token才能執行
        TextSendMessage(text='早安'))


if __name__ == "__main__":
    app.run()