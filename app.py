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

def get_data():

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-BC84844D-BF61-4B5E-9DB2-8CAFF5C4DF3F",
        "locationName": "臺北市",
    }

    response = requests.get(url, params=params)
    #print(response.status_code) 確認狀態

    if response.status_code == 200:
         
        #print(response.text)
        data = json.loads(response.text)

        location = data["records"]["location"][0]["locationName"]

        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        #comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        #print(location, start_time , "到" , end_time , "的天氣狀況是" , weather_state , "，降雨機率為", rain_prob , "%，溫度狀況為" , min_tem , "度到" , max_tem ,"度")
        w = (location, start_time , "到" , end_time , "的天氣狀況是" , weather_state , "，降雨機率為", rain_prob , "%，溫度狀況為" , min_tem , "度到" , max_tem ,"度")
        #print(r)
        return w

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
    elif msg == "天氣":
        
        #r = str(location, start_time , "到" , end_time , "的天氣狀況是" , weather_state , "，降雨機率為", rain_prob , "%，溫度狀況為" , min_tem , "度到" , max_tem ,"度")

    line_bot_api.reply_message(
        event.reply_token, #要給token才能執行
        TextSendMessage(text= r))


if __name__ == "__main__":
    app.run()



