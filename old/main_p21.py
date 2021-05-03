import json

from googleapiclient.discovery import build

'''
!!!! Usefull links !!!!! 
https://github.com/googleapis/google-api-python-client
https://github.com/youtube/api-samples
https://developers.google.com/youtube/v3/docs
https://developers.google.com/youtube/v3/determine_quota_cost

pip install --upgrade google-api-python-client

https://github.com/googleapis/google-cloud-python
'''
print("** Hola Hey, Azzrael_YT subs!!!")


API_KEY = '---'

'''
Get YouTube API service w API Key only
'''
def get_service():
    service = build('youtube', 'v3', developerKey=API_KEY)
    return service

'''
Get Channel Info (title, desc, stats)
https://developers.google.com/youtube/v3/docs/channels/list

https://www.youtube.com/channel/UCXlhVxzpYqr2WguSWbzRNMw
https://www.youtube.com/c/tntonlineru
https://www.youtube.com/user/tn4east
'''
def get_channel_info(channel_id = 'UCf6kozNejHoQuFhBDB8cfxA'):
    r = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
    # print(json.dumps(r))
    print(r['items'][0]['snippet']['title'])
    print(r['items'][0]['snippet']['publishedAt'])
    print(r['items'][0]['statistics']['viewCount'])

'''
Get Video Info (title, desc, stats)
https://developers.google.com/youtube/v3/docs/videos/list
'''
def get_video_info(video_id = 'nIGeJDX8kzg'):
    r = get_service().videos().list(id=video_id, part='snippet,statistics').execute()
    # print(json.dumps(r['items']))
    print(r['items'][1]['snippet']['title'])
    print(r['items'][1]['statistics']['viewCount'])


if __name__ == '__main__':
    # get_channel_info()
    # get_channel_info('UCkbSaWqttPHTS00K0fjniTQ')
    get_video_info('Ji4OKuRGN0k,4qgR-CmqV88')
    # get_video_info('T8OHuABIaro')
