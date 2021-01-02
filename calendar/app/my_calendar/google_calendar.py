import json
import datetime
import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../lib'))
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def _get_service():
        # サービスアカウントのJSONファイルパス
        GOOGLE_APPLICATION_CREDENTIALS=os.environ['GOOGLE_CREDENTIALS_FILE']
        c = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
        return build('calendar', 'v3', credentials=c)


def _get_calendar_id():
       # データを取得したいGoogleカレンダーのIDを指定する
       return os.environ['GOOGLE_CALENDAR_ID']

   
def _get_dateTime(string):
    return string


def _get_insert_body(b):
    #startDate = _get_dateTime(start)
    #endDate = _get_dateTime(end)

    body = dict()
    body['summary'] = b.summary
    body['start'] = {'timeZone': 'Asia/Tokyo', 'dateTime': '2021-01-09T11:00:00+09:00'}
    body['end'] = {'timeZone': 'Asia/Tokyo', 'dateTime': '2021-01-09T11:30:00+09:00'}
    body['location'] = b.location
    body['guestsCanSeeOtherGuests'] = False
    body['guestsCanInviteOthers'] = False

    return body


class Body:
    def __init__(self, summary, start, end, location):
        self.summary  = summary
        self.start    = start
        self.end      = end
        self.location = location


class GoogleCalendar:
    def __init__(self):
        self.service     = _get_service()
        self.calendar_id = _get_calendar_id()
   
    
    def get_schedules(self):
        service     = self.service
        calendar_id = self.calendar_id
        now = datetime.datetime.utcnow().isoformat() + 'Z'
    
        result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return result
    
    
    def insert_schedule(self, summary, start, end, location):
        _body = Body(summary, start, end, location)
    
        # Call the Calendar API
        body = _get_insert_body( _body )
        insert_result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=body
                ).execute()
    
    #   events = events_result.get('items', [])
#    
#    #    if not events:
#    #        print('No upcoming events found.')
#    #    for event_c in events:
#    #        event_id = event_c['id']
#    #        start = event_c['start'].get('dateTime', event_c['start'].get('date'))
#    #        print(event_id, start, event_c['summary'])
#    # 
#    #    return events
#    
