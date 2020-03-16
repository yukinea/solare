
import json
import datetime
import os.path
import sys
sys.path.append('..')

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def insert_schedule():
 # サービスアカウントのJSONファイルパス
    GOOGLE_APPLICATION_CREDENTIALS=os.environ['GOOGLE_CREDENTIALS_FILE']

    c = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    service = build('calendar', 'v3', credentials=c)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    #calendar_id = 'primary'
    # データを取得したいGoogleカレンダーのIDを指定する
    calendar_id = os.environ['GOOGLE_CALENDAR_ID']
    body = dict()
    body['summary'] = 'Test summary'
    body['start'] = {'timeZone': 'Asia/Tokyo', 'dateTime': '2020-03-09T11:00:00+09:00'}
    body['end'] = {'timeZone': 'Asia/Tokyo', 'dateTime': '2020-03-09T11:30:00+09:00'}
    body['location'] = 'Kobe'
    body['guestsCanSeeOtherGuests'] = False
    body['guestsCanInviteOthers'] = False

    insert_result = service.events().insert(
            calendarId=calendar_id,
            body=body
            ).execute()

    print(insert_result)

    events_result = service.events().list(
        calendarId=calendar_id, timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(events)

    if not events:
        print('No upcoming events found.')
    for event_c in events:
        event_id = event_c['id']
        start = event_c['start'].get('dateTime', event_c['start'].get('date'))
        print(event_id, start, event_c['summary'])

    return events
