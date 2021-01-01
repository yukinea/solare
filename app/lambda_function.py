import json
import sys

from my_calendar import google_calendar

def lambda_handler(event, context):
    calendar_obj = google_calendar.GoogleCalendar()
    insert(calendar_obj)
    show(calendar_obj)


def insert(obj):
    obj.insert_schedule('TestSummary', '1/1', '1/1', 'Osaka')


def show(obj):
    print(obj.get_schedules())

lambda_handler('hoge','hoge')
