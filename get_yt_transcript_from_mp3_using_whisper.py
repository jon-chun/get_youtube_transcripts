# CUDA reset: https://stackoverflow.com/questions/66857471/cuda-initialization-cuda-unknown-error-this-may-be-due-to-an-incorrectly-set

# https://www.pinecone.io/learn/openai-whisper/

# importing modules
from tqdm.auto import tqdm

import logging
# import time
from datetime import datetime
# import random
import json
from pathlib import Path

# import numpy as np
# import pandas as pd
# from slugify import slugify

# import os
# from pytube import YouTube

import whisper
from whisper.utils import write_srt
from whisper.utils import write_txt
from whisper.utils import write_vtt
import torch

# CONFIGURATION (a)
# Get Configuration
whisper_model = "base.en"
import configuration
channel_id = configuration.channel_id
channel_name = configuration.channel_name

# Source subdir with *.mp3 audio files
# subdir_mp3 = 'data___mp3___Helix_Center___UCvShfJtvC2owV0AFi_qyykA'
subdir_mp3 = f'data___mp3___{channel_name}___{channel_id}'

# CONFIGURATION (b)
# Destination subdirs with transcripts in various output text formats
# Set the following values to:
#   'yes' to transcribe
#   '' to skip
subdir_txt = 'yes'
subdir_srt = 'yes'
subdir_vtt = 'yes'
# Transcript Format (a): Plain Text (full text with punctuation but no timestamps)
if subdir_txt != '':
    subdir_txt = subdir_mp3.replace('___mp3___','___txt___')
    print(f'Saving Plain Text Transcripts to subdir: {subdir_txt}')
    Path(subdir_txt).mkdir(parents=True, exist_ok=True)
# Transcript Format (b): SRT format (timestamped fragments)
if subdir_srt != '':
    subdir_srt = subdir_mp3.replace('___mp3___','___srt___')
    print(f'Saving SRT Transcripts to subdir: {subdir_srt}')
    Path(subdir_srt).mkdir(parents=True, exist_ok=True)
# Transcript Format (c): VTT format (timestamped fragments)
if subdir_vtt != '':
    subdir_vtt = subdir_mp3.replace('___mp3___','___vtt___')
    print(f'Saving VTT Transcripts to subdir: {subdir_vtt}')
    Path(subdir_vtt).mkdir(parents=True, exist_ok=True)
subdir_json = ''
# Transcript Format (d): JSON Format
if subdir_json != '':
    subdir_fulltext = subdir_mp3.replace('___mp3___','___json___')
    print(f'Saving JSON Transcripts to subdir: {subdir_json}')
    Path(subdir_json).mkdir(parents=True, exist_ok=True)

# print(f'Saving transcripts to subdir: {subdir_txt}')
# Path(subdir_txt).mkdir(parents=True, exist_ok=True)
# subdir_srt = subdir_mp3.replace('___mp3___','___srt___')
# subdir_json = subdir_mp3.replace('___mp3___','___json___')

# print(f'Saving SRT to subdir: {subdir_json}')
# Path(subdir_json).mkdir(parents=True, exist_ok=True)

# Setup Logfiles
datetime_str = datetime.now().strftime("%Y%m%d-%H%M%S")
filename_log = f'log___mp3___{channel_name}___{channel_id}___{datetime_str}.txt'
print(f'Logging to file: {filename_log}')

# Check if CUDA available
my_device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'Device: {my_device}')
# model = whisper.load_model("medium.en").to(device)
model = whisper.load_model(whisper_model, device=my_device)

# get list of mp3 audio files as type (path)
mp3_paths_ls = [str(x) for x in Path(f"./{subdir_mp3}").glob('*.mp3')]
print(f'*.mp3 file count: {len(mp3_paths_ls)}')
# print(paths[:5])

# print(mp3_paths_ls[0].split('___')[-1].split('.')[0])


# Get chosen transcript formats for all *.mp3 audio files
data = []
for i, apath in enumerate(tqdm(mp3_paths_ls)):
    # Get *.mp3 id and title
    _id = apath.split('___')[-1].split('.')[0]
    print(f'_id: {_id}')
    _title = apath.split('/')[-1].split('.')[:-1][0]
    print(f'_title: {_title}')

    # transcribe *.mp3
    time_start = datetime.now()
    result = model.transcribe(apath)
    # segments = result['segments'])
    time_end = datetime.now()
    time_elapsed = time_end - time_start
    logging.info(f'Elapsed Time for VideoID:{_id}: {time_elapsed}')
    print(f'Execution Time: {time_elapsed}')

    # Transcript Format (a): Plain Text (full text with punctuation but no timestamps)
    if subdir_txt != '':
        print(f'subdir_txt: {subdir_txt}, type: {type(subdir_txt)}')
        print(f'_title: {_title}, type: {type(_title)}')
        print(f'_id: {_id}, type{type(_id)}')
        file_fullpath = f"./{subdir_txt}/{_title}_{_id}.txt"
        print(f'file_fullpath: {file_fullpath}, type{type(file_fullpath)}')
        with open(file_fullpath, "w", encoding="utf-8") as fp_txt:
            write_txt(result['segments'], file=fp_txt)
        logging.info(f'Saved TXT Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: TXT Transcript to: {file_fullpath}')
    if subdir_srt != '':
        file_fullpath = f"./{subdir_srt}/{_title}_{_id}.srt"
        with open(file_fullpath, "w", encoding="utf-8") as fp_srt:
            write_srt(result['segments'], file=fp_srt)
        logging.info(f'Saved SRT Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: SRT Transcript to: {file_fullpath}')
    if subdir_vtt != '':
        file_fullpath = f"./{subdir_vtt}/{_title}_{_id}.vtt"
        with open(file_fullpath, "w", encoding="utf-8") as fp_vtt:
            write_vtt(result['segments'], file=fp_vtt)
        logging.info(f'Saved VTT Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: VTT Transcript to: {file_fullpath}')
    if subdir_json != '':
        file_fullpath = f"./{subdir_json}/{_title}_{_id}_full.txt"
        segments = result['segments']
        json_ls = []
        for segment in segments:
            meta = {
                "id":f"{_id}-t{segment['start']}",
                "text": segment['text'].strip(),
                "start": segment['start'],
                "end": segment['end']
            }
            json_ls.append(meta)
        with open(file_fullpath, "w", encoding="utf-8") as fp_json:
            for aline in tqdm(json_ls):
                json.dump(aline,fp_json)
                fp_json.write('\n')

        logging.info(f'Saved JSON Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: JSON Transcript to: {file_fullpath}')

    break

print('done')

"""

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


"""