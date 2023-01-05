# https://stackoverflow.com/questions/73827182/youtube-api-get-all-videos-of-channel-with-more-than-500-videos
# https://developers.google.com/youtube/v3/getting-started

# https://www.youtube.com/channel/UCvShfJtvC2owV0AFi_qyy

import pandas as pd
import requests
import datetime


# Read Secret API Credentials from .gitignore file 
# Also read YouTube Channel ID
import credentials
api_key = credentials.google_api
import configuration
channel_id = configuration.channel_id
channel_name = configuration.channel_name

print(f'channel_id:{channel_id}\nchannel_name:{channel_name}')
# CONFIGURE SECTION
# channel_id = 'UCXDi1F7Q-cJQ4mGGavtfYRQ'
# channel_id = 'UCvShfJtvC2owV0AFi_qyykA' # The Helix Center

# build dataframe
df = pd.DataFrame(columns=['channel_id',
                           'video_id',
                           'video_title'
                           'published_date',
                           'type'])


# first request
my_url = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=' + channel_id + '&maxResults=50&order=date&type=video&key=' + api_key
response = requests.get(url=my_url).json()
print(my_url)
total_results = response['pageInfo']['totalResults']

# save the channel_id and video_id in a dataframe
for i in response['items']:

    channel_id = i['snippet']['channelId']
    video_id = i['id']['videoId']
    published_date = i['snippet']['publishedAt']
    video_title = i['snippet']['title']
    vid_type = i['id']['kind']

    df = pd.concat([df, pd.DataFrame([{
        'channel_id': channel_id,
        'video_id': video_id,
        'video_title': video_title,
        'published_date': published_date,
        'type': vid_type
    }])], ignore_index=True)

while df['video_id'][len(df)-1] != df['video_id'][len(df)-2]:
    url = 'https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=' + channel_id + '&maxResults=50&order=date&type=video&publishedBefore=' + published_date + '&key=' + api_key

    response = requests.get(url=url).json()
    total_results = response['pageInfo']['totalResults']

    for i in response['items']:
        channel_id = i['snippet']['channelId']
        video_id = i['id']['videoId']
        published_date = i['snippet']['publishedAt']
        video_title = i['snippet']['title']
        vid_type = i['id']['kind']

        df = pd.concat([df, pd.DataFrame([{
            'channel_id': channel_id,
            'video_id': video_id,
            'video_title': video_title,
            'published_date': published_date,
            'type': vid_type
        }])], ignore_index=True)

# because the last row is a duplicate we need to delete the last row
df.drop(df.tail(1).index, inplace=True)

# df.to_csv('C:\\Users\\...\\data\\video_ids_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv')

df.to_csv('video_ids___' + channel_name + '___' + channel_id + '___' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv')