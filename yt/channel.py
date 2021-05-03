from random import randrange
from time import sleep

from googleapiclient.http import MediaFileUpload

from yt.helpers import *
from yt.creds import *

'''
https://developers.google.com/youtube/v3/docs
https://developers.google.com/youtube/v3/determine_quota_cost
'''

'''
Get Channel Info (title, desc, stats)
https://developers.google.com/youtube/v3/docs/channels/list

channel url types
https://www.youtube.com/channel/UCf6kozNejHoQuFhBDB8cfxA
https://www.youtube.com/c/tntonlineru
https://www.youtube.com/user/tn4east
'''
def get_channel_info(channel_id = 'UCf6kozNejHoQuFhBDB8cfxA'):
    r = get_service_simple().channels().list(
        id=channel_id,
        part='snippet,statistics'
    ).execute()

    created = parse_date(r['items'][0]['snippet']['publishedAt'])
    today = datetime.now(created.tzinfo)

    return {
        'channel_id'    : channel_id,
        'title'         : r['items'][0]['snippet']['title'],
        'desc'          : r['items'][0]['snippet']['description'],
        'created_at'    : r['items'][0]['snippet']['publishedAt'],
        'created_days'  : (today - created).days,
        'videos'  : int(r['items'][0]['statistics']['videoCount']),
        'views'   : int(r['items'][0]['statistics']['viewCount']),
        'subs'    : int(r['items'][0]['statistics']['subscriberCount']),
    }

'''
Get Most Viewed/Liked/etc Videos at Channel
'''
def channel_top50(channel_id = 'UCf6kozNejHoQuFhBDB8cfxA'):
    print(f"searching at {channel_id}")
    ch = get_channel_info(channel_id)


    # также можно использовать playlists#list для плейлиста uploads заданного канала
    # но у этого метода нет сортировки при том же лимите в 50 на запрос
    # соотв пришлось бы организовывать пагинацию, запрашивать статистику по всем видео
    # и сортировать уже после - на маленьком канале смысл есть заморачиваться, на крупном - нет (если топ 50 нам достаточно)

    # https://github.com/youtube/api-samples/blob/master/python/search.py
    # https://developers.google.com/youtube/v3/docs/search/list
    r = get_service_simple().search().list(
        maxResults=50,
        channelId=channel_id,
        order='viewCount',
        part='snippet',
        type='video',
        publishedAfter='2018-01-01T00:00:00Z'
    ).execute()

    # videos stats (likes,comments,dis)
    ids = ",".join([item['id']['videoId'] for item in r['items']])
    video_items = get_video_stats(ids)

    # combine stats
    videos  = []
    for v in video_items:

        # days since publicate
        pub_time = parse_date(v['snippet']['publishedAt'])
        today =  datetime.now(pub_time.tzinfo)

        t = {
            'video_id'      : v['id'],
            'url'      : "https://www.youtube.com/watch?v=" + v['id'],
            'title'         : v['snippet']['title'],
            'published_at'  : v['snippet']['publishedAt'],
            'days_publicated' : (today - pub_time).days,

            'likes': int(v['statistics']['likeCount']) if 'likeCount' in v['statistics'] else 0,
            'views': int(v['statistics']['viewCount']) if 'viewCount' in v['statistics'] else 0,
            'comments': int(v['statistics']['commentCount']) if 'commentCount' in v['statistics'] else 0,
            'dislikes': int(v['statistics']['dislikeCount']) if 'dislikeCount' in v['statistics'] else 0,

            'channel_id'        : ch['channel_id'],
            'channel_title'     : ch['title'],
            'channel_views'     : ch['views'],
            'channel_subs'      : ch['subs'],
            'channel_created_at' : ch['created_at'],
            'channel_created_days' : ch['created_days'],
        }

        videos.append(t)

    return videos

'''
Get Videos Stats
'''
def get_video_stats(ids):
    r = get_service_simple().videos().list(
        part="snippet,statistics",
        id=ids,
    ).execute()

    return r['items']

'''
Upload videos to Channel via YouTube API
https://developers.google.com/youtube/v3/docs/videos/insert
https://developers.google.com/youtube/v3/guides/uploading_a_video
https://github.com/youtube/api-samples/blob/master/python/upload_video.py
'''
def video_upload(video_path, title, **kwargs):
    print("** upload video")

    # chunksize размер блока в БАЙТАХ (int), чем хуже соединение, тем мельче блок
    # напр. для мобильного трафа норм 1024*1024*3 = 3М
    # -1 => видос будет грузиться целиком, быстрее на норм сети и при обрыве все равно будет докачка
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    meta = {
        'snippet': {
            'title' : title,
            'description' : kwargs.get("description", "empty desc")
        },
        # All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020
        # will be restricted to private viewing mode. To lift this restriction,
        # each API project must undergo an audit to verify compliance
        # --- т.е. для прилки в статусе теста тут всегда приват, иначе видос будет заблокирован
        'status':{
            'privacyStatus':kwargs.get("privacy", "private")
        }
    }

    insert_request = get_service_creds("youtube", "v3").videos().insert(
        part=','.join(meta.keys()),
        body=meta,
        media_body=media
    )

    r = resumable_upload(insert_request)

    print(r)

'''
Resumable Upload by chunks
возмобновляемая загрузка файла, см.
https://github.com/youtube/api-samples/blob/master/python/upload_video.py
но здесь я сильно упростил
'''
def resumable_upload(request, retries = 5):
    while retries > 0:
        try:
            status, response = request.next_chunk()
            if response is None: raise Exception("empty response")
            if 'id' in response: return response # success
        except Exception as e:
            print(e)

        retries -= 1
        sleep(randrange(5))

    return None