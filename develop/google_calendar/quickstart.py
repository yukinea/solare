from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

GOOGLE_APPLICATION_CREDENTIALS='' # サービスアカウントのJSONファイルパス

def main():

    c = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    service = build('calendar', 'v3', credentials=c)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    calendar_id = 'primary'
    body = dict()
    body['summary'] = 'Test summary'
    body['start'] = {'timeZone': 'Asia/Tokyo', 'dateTime': '2020-03-04T11:00:00+09:00'}
    body['end'] = {'timeZone': 'Asia/Tokyo', 'dateTime': '2020-03-04T11:30:00+09:00'}
    body['location'] = 'Kobe'
    body['guestsCanSeeOtherGuests'] = False
    body['guestsCanInviteOthers'] = False
    body['attendees'] = [
#            {'email':'ゲストメールアドレス', 'optional': True}
            ]

    insert_result = service.events().insert(
            calendarId=calendar_id,
            body=body
            ).execute()

    print(insert_result)

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        event_id = event['id']
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event_id, start, event['summary'])


if __name__ == '__main__':
    main()
