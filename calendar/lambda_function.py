import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
from my_calendar import google_calendar

def lambda_handler(event, context):
    calendar_obj = google_calendar.GoogleCalendar()

    event_type = event['type']
    if event_type == 'insert':
        return insert(calendar_obj, event['payload'])
    elif event_type == 'show':
        return show(calendar_obj)
    else:
        pass

    return None


def insert(obj, payload):
    body = get_insert_body(payload)

    result = obj.insert_schedule(
        body['summary'], 
        '1/1',
        '1/1',
        body['location']
    )
    return result


def show(obj):
    return obj.get_schedules()['items']


def get_insert_body(p):
    rows = p.splitlines()
    body = {}
    body['summary']  = rows[0]
    body['start']    = rows[1]
    body['end']      = rows[2]
    body['location'] = rows[3]
    return body


#print(lambda_handler({'type': 'show', 'payload': 'あいうえお\nかきくけこ\nさしすせそ\nたちつてと'},'hoge'))
#lambda_handler({'type': 'insert', 'payload': 'あいうえお\nかきくけこ\nさしすせそ\nたちつてと'},'hoge')

