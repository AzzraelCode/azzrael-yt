import datetime
from datetime import *

from yt import helpers
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

    created = helpers.parse_date(r['items'][0]['snippet']['publishedAt'])
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
        pub_time = helpers.parse_date(v['snippet']['publishedAt'])
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
'''
def video_upload():
    print("** upload video")