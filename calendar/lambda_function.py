import json
import urllib
import boto3
import urllib
import re
import os
import datetime
import os.path
from mylib import googlecalendar

def lambda_handler(event, context):
    events = googlecalendar.insert_schedule()


    #return 0

    print(event)
    print(json.loads(event['body'])['events'][0]['message'])

    # ユーザからのメッセージ(など)に対して応答するためのAPI
    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    # Authorizationは「Bearer アクセストークン」とする必要がある。公式参照。
    headers = {
        'Authorization': os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }

    message = [
        {
            "type": "text",
            "text": json.dumps(events)
        }
    ]

    # メッセージ毎のreplyTokenを含める必要がある
    # eventのbody部分が単なるStringなのでjsonにしてからとる
    replyToken = json.loads(event['body'])['events'][0]['replyToken']
    params = {
        "replyToken": replyToken,
        "messages": message
    }

    request = urllib.request.Request(
        url,
        json.dumps(params).encode("utf-8"),
        method=method,
        headers=headers
    )

    with urllib.request.urlopen(request) as res:
        body = res.read()
    return 0
    
    """ PUSH通知する場合
    userId = ''  # 自分のuserIdまたはgroupIdやroomIdが指定できる
    url = "https://api.line.me/v2/bot/message/push"
    method = "POST"
    headers = {
        'Authorization': os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    message = [
        {
            "type": "text",
            "text": "42"
        }
    ]
    params = {
        "to": userId,
        "messages": message
    }
    request = urllib.request.Request(
        url,
        json.dumps(params).encode("utf-8"),
        method=method,
        headers=headers
    )

    with urllib.request.urlopen(request) as res:
        body = res.read()
    
    return 0
    """
