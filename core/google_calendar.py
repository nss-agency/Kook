from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

"""
Scope	                                                              Meaning
https://www.googleapis.com/auth/calendar	                read/write access to Calendars
https://www.googleapis.com/auth/calendar.readonly	        read-only access to Calendars
https://www.googleapis.com/auth/calendar.events	            read/write access to Events
https://www.googleapis.com/auth/calendar.events.readonly	read-only access to Events
https://www.googleapis.com/auth/calendar.settings.readonly	read-only access to Settings
https://www.googleapis.com/auth/calendar.addons.execute	    run as a Calendar add-on
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def login_credentials():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    token_pickle_path = os.path.join(BASE_DIR, 'token.pickle')
    credentials_json_path = os.path.join(BASE_DIR, 'credentials.json')
    if os.path.exists(token_pickle_path):
        with open(token_pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def create_event_from_booking(booking):
    creds = login_credentials()
    service = build('calendar', 'v3', credentials=creds)

    colors = {
        'Стандарт': '4',
        'Комфорт': '5',
        'Комфорт Плюс': '6',
        'Люкс': '7',
        'Тріо': '8'
    }

    event = {
        'summary': f'{booking.pib} | {booking.phone} | {booking.room_type} ({booking.quantity})',
        'description': f'E-mail: {booking.email} \nДодаткові опції: {booking.additional} \nНотатки: {booking.notes}',
        'colorId': f'{booking.room_type.color_id}',
        'start': {
            'dateTime': f'{booking.date_entry}T5:00:00-07:00',
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': f'{booking.date_leave}T3:00:00-07:00',
            'timeZone': 'Europe/Kiev',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()


def create_event_from_banquet(banquet):
    creds = login_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'БАНКЕТНИЙ ЗАЛ {banquet.pib} | {banquet.phone} ',
        'description': f'E-mail: {banquet.email} \nНотатки: {banquet.notes}',
        'colorId': '9',
        'start': {
            'dateTime': f'{banquet.check_in}T1:00:00-07:00',
            'timeZone': 'Europe/Kiev',
        },
        'end': {
            'dateTime': f'{banquet.check_in}T24:00:00-07:00',
            'timeZone': 'Europe/Kiev',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()


def main():
    creds = login_credentials()
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event)


if __name__ == '__main__':
    main()
