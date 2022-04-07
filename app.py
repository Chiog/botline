from flask import Flask, request, abort 
import requests
from bs4 import BeautifulSoup
import json
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
    msg = event.message.text
    r = '無法回覆的內容'
    if msg == "hi":
        r = "hi" 
        #r = str(location, start_time , "到" , end_time , "的天氣狀況是" , weather_state , "，降雨機率為", rain_prob , "%，溫度狀況為" , min_tem , "度到" , max_tem ,"度")

    line_bot_api.reply_message(
        event.reply_token, #要給token才能執行
        TextSendMessage(text= r))


if __name__ == "__main__":
    app.run()



