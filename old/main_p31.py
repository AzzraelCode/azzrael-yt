import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

'''
!!!! Usefull links !!!!! 
https://github.com/googleapis/google-api-python-client
https://developers.google.com/docs/api/quickstart/python

https://github.com/youtube/api-samples
https://developers.google.com/youtube/v3/docs
https://developers.google.com/youtube/v3/determine_quota_cost
'''

API_KEY = 'AIzaSyABAheWOiEiA5ErRrj7d4rh_OZqMxYHDgE'

APP_TOKEN_FILE = "client_secret.json"
USER_TOKEN_FILE = "user_token.json"

# https://developers.google.com/identity/protocols/oauth2/scopes#youtube
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    # 'https://www.googleapis.com/auth/youtube.upload',
    # 'https://www.googleapis.com/auth/userinfo.email'
]

'''
Ask from console
'''
def get_creds_cons():
    flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
    return flow.run_console()

'''
Reusebale user OAuth2 token
'''
def get_creds_saved():
    # https://developers.google.com/docs/api/quickstart/python
    creds = None

    if os.path.exists(USER_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


'''
Get YouTube API service w API Key only
'''
def get_service():
    #creds = get_creds_cons()
    creds = get_creds_saved()
    service = build('oauth2', 'v2', credentials=creds)
    return service


'''
Get User Info 
'''
def get_user_info(channel_id = 'UCf6kozNejHoQuFhBDB8cfxA'):
    r = get_service().userinfo().get().execute()
    print(json.dumps(r))

if __name__ == '__main__':
    print("** Hola Hey, Azzrael_YT subs!!!\n")
    get_user_info()
