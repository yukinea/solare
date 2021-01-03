import json
import urllib.request
import boto3
import re
import os
import datetime

def reply(replyToken, message):
    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    headers = {
        'Authorization': os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
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
        return res.read()


def get_payload(event):
    text = event['message']['text']
    print(text)
    p = {}
    if text == 'みせて' or text == '見せて' or text == '予定':
        p['type'] = 'show'
    else:
        p['type'] = 'insert'
        p['payload'] = event['message']['text']

    return json.dumps(p)


def lambda_handler(event, context):
    event_body = json.loads(event['body'])['events'][0]
    reply_token = event_body['replyToken']

    payload = get_payload(event_body)

    response = boto3.client('lambda').invoke(
        FunctionName='test3',
        InvocationType='RequestResponse', # Event or RequestResponse
        Payload=payload
    )
    res = json.loads(response['Payload'].read())

    res_message = "レスポンスが想定外だよ"
    if res is None:
        res_message = "error"
    elif 'errorMessage' in res:
        res_message = res['errorMessage']
    elif 'status' in res:
        if res['status'] == 'confirmed':
            res_message = "登録しました\n" + res['summary'] + "\n" + res['location'] + "\n" + res['start']['dateTime']
    elif type(res) is list:
        hoge = []
        hoge.append('-----')
        for r in res:
            hoge.append(r['summary'])
            hoge.append(r['location'])
            hoge.append(r['start']['dateTime'])
            hoge.append('----')
            res_message = '\n'.join(hoge)
        
    message = [
        {
            "type": "text",
            "text": res_message
        }
    ]
    reply(reply_token, message)
    
    return 0
    
    """
    print(event)
    #print(json.loads(event['body'])['events'][0]['message'])

    # ユーザからのメッセージ(など)に対して応答するためのAPI
    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    # Authorizationは「Bearer アクセストークン」とする必要がある。公式参照。
    headers = {
        'Authorization': os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }

    events = {"hoge":"bar"}
    message = [
        {
            "type": "text",
            "text": json.dumps(events)
        }
    ]

    # メッセージ毎のreplyTokenを含める必要がある
    # eventのbody部分が単なるStringなのでjsonにしてからとる
    
    """
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


