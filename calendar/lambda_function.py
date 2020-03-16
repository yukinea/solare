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

    # ���[�U����̃��b�Z�[�W(�Ȃ�)�ɑ΂��ĉ������邽�߂�API
    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    # Authorization�́uBearer �A�N�Z�X�g�[�N���v�Ƃ���K�v������B�����Q�ƁB
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

    # ���b�Z�[�W����replyToken���܂߂�K�v������
    # event��body�������P�Ȃ�String�Ȃ̂�json�ɂ��Ă���Ƃ�
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
    
    """ PUSH�ʒm����ꍇ
    userId = ''  # ������userId�܂���groupId��roomId���w��ł���
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
