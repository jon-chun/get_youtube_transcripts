# importing modules
import logging
import time
from datetime import datetime
import random
import json
from pathlib import Path

import numpy as np
import pandas as pd
from slugify import slugify

import os
from pytube import YouTube

# Get Configuration
import configuration
channel_id = configuration.channel_id
channel_name = configuration.channel_name
datetime_str = time.strftime("%Y%m%d-%H%M%S")

# Get each YouTube Video ID from the [*.csv] file created by [get_yt_channel_video_ids.py]
filename_videoids_prefix = f'video_ids___{channel_name}___{channel_id}___' # Created by 

# Sort all matching files and pick the one with the most current datetime stamp
filename_videoids = sorted([file.name for file in Path('./').iterdir() if file.name.startswith(filename_videoids_prefix)])[0]

# Create subdir to hold YouTube channel video transcripts
subdir_name = f'data__mp3___{channel_name}___{channel_id}'
Path(subdir_name).mkdir(parents=True, exist_ok=True)
filename_log = f'log___mp3___{channel_name}___{channel_id}___{datetime_str}.txt'

# Setup logging
# Create and configure logger
logging.basicConfig(filename=filename_log,
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Read all existing SRT transcript files in ./data/*.json subdir
# NOTE: 3 underscores ('___') are used to separate components of filename since
#       the underscore itself may be embedded in channel_id, video_id or video_title
videoid_set = set([str(f).split('___')[-1].split('.')[0] for f in Path(f'./{subdir_name}').glob('*.mp3') if f.is_file()])

def get_mp3_by_videoid(yt_id: str, fname_out: str):
    # using the srt variable with the list of dictionaries
    # obtained by the .get_transcript() function
    
    video_id = yt_id.strip()
    try:
        
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')

        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download(output_path=subdir_name)

        base, ext = os.path.splitext(out_file)
        filename_out = base + '.mp3'
        os.rename(out_file, filename_out)    
        
        return filename_out
            
    except:
        # print(f'ERROR: Skipping transcript for video_id: {yt_id}')
        filename_out = ""
        return filename_out


df = pd.read_csv(filename_videoids, index_col=[0])
df['video_title_slug'] = df['video_title'].astype(str).apply(lambda x: slugify(x))
df['fname_clean'] = df['video_title_slug'].astype(str) + '___' + df['published_date'].astype(str).apply(lambda x: x[:10]) + '___' + df['channel_id'].astype(str) + '___' + df['video_id'].astype(str)

# Create an exit_status col initialized to nan to store result of each attempted scrape
df['exit_status'] = np.nan

# For each row in df DataFrame, attempt to scrape the YouTube transcript by the video_id col
videoid_success_ls = []
videoid_fail_ls = []
videoid_exist_ls = []

time_start = datetime.now() 

for index, row in df.iterrows():
    avideo_id = row['video_id']
    afilename = row['fname_clean']
    print(f"Getting Video #{index} \n  ChannelID: {row['channel_id']} \n  VideoID: {avideo_id} \n  Title: {row['video_title']} \n  Date: {row['published_date']} \n  Filename: {afilename}")

    if avideo_id in videoid_set:
        # This yt_id SRT Transcript file already exists in ./data subdir, so skip
        print(f'  SKIPPED: SRT Transcript already exists, skipping')
        videoid_exist_ls.append(avideo_id)
        df.iloc[index]['exit_status'] = 'skipped'
        logger.warning(f'SKIPPED VideoID:{avideo_id} - Already exists')
        
    else:
        delay_sec = random.randint(5,10)
        time.sleep(delay_sec)
        filename_out = get_mp3_by_videoid(avideo_id, afilename)
        if len(filename_out) > 0:
            videoid_success_ls.append(avideo_id)
            df.iloc[index]['exit_status'] = 'scraped'
            print(f'  SCRAPED INTO: {filename_out}')
            logger.info(f'SCRAPED VideoID:{avideo_id} - Success')
        else:
            videoid_fail_ls.append(avideo_id)
            df.iloc[index]['exit_status'] = 'failed'
            print(f'  FAILED')
            logger.error(f'FAILED VideoID:{avideo_id} - Could not scrape')    

time_end = datetime.now()
time_elapsed = time_end - time_start 

print(f'Attempted to scrape {df.shape[0]} Videos:')
print(f'      SUCCESS: {len(videoid_success_ls)}')
print(f'         FAIL: {len(videoid_fail_ls)}')
print(f'       EXISTS: {len(videoid_exist_ls)}')
print(f'\n\n   Start Time: {time_start}')
print(f'     End Time: {time_end}')
print(f' Elapsed Time: {time_elapsed}')

print('\n\nList of FAILED by VideoDI')
for i, videoid in enumerate(videoid_fail_ls):
    print(f'Video #{i}: {videoid}')
    
print('\n\n')
print(f'Check logfile: {filename_log} for full details')


