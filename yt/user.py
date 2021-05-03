'''
Get User Info
'''
import json
from yt.creds import get_service_creds


def get_current_user_info():
    r = get_service_creds('oauth2', 'v2').userinfo().get().execute()
    return r