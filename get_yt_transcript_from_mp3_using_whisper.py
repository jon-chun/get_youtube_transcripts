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
subdir_json = 'yes'
subdir_fulltext = 'yes'
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
# Transcript Format (d): JSON Format
if subdir_json != '':
    subdir_json = subdir_mp3.replace('___mp3___','___json___')
    print(f'Saving JSON Transcripts to subdir: {subdir_json}')
    Path(subdir_json).mkdir(parents=True, exist_ok=True)
# Transcript Format (e): FULL TEXT Format
if subdir_fulltext != '':
    subdir_fulltext = subdir_mp3.replace('___mp3___','___fulltext___')
    print(f'Saving JSON Transcripts to subdir: {subdir_fulltext}')
    Path(subdir_fulltext).mkdir(parents=True, exist_ok=True)

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
    _channel = apath.split('___')[-2].split('.')[0]
    print(f'_channel: {_channel}')
    _title = apath.split('/')[-1].split('.')[:-1][0]
    print(f'_title: {_title}')

    # Set skip_flag if YouTube ID already has been transcribed in the desired format(s)
    skip_flag = True
    subdir_transcriptions_ls = ['subdir_txt', 'subdir_srt', 'subdir_vtt', 'subdir_json', 'subdir_fulltext']
    for asubdir in subdir_transcriptions_ls:
        if globals()[asubdir] != '':
            subdir_str = f"data___{asubdir.split('_')[1]}___{channel_name}___{channel_id}"
            # file_ls = list(Path(f'./{asubdir}').glob('*.mp3'))
            file_ls = [str(x) for x in Path(subdir_str).glob('*')]
            print(f'{subdir_str}: {len(file_ls)} *.mp3 audio files')
            file_ls_str = ' '.join(file_ls)
            if not(_id in file_ls_str):
                skip_flag = False
    print(f'  Skip?: {skip_flag}')
    if skip_flag == True:
        continue

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
    # Transcript Format (b): SRT (fragments with timestamps)
    if subdir_srt != '':
        file_fullpath = f"./{subdir_srt}/{_title}_{_id}.srt"
        with open(file_fullpath, "w", encoding="utf-8") as fp_srt:
            write_srt(result['segments'], file=fp_srt)
        logging.info(f'Saved SRT Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: SRT Transcript to: {file_fullpath}')
    # Transcript Format (c): VTT (fragments with timestamps)
    if subdir_vtt != '':
        file_fullpath = f"./{subdir_vtt}/{_title}_{_id}.vtt"
        with open(file_fullpath, "w", encoding="utf-8") as fp_vtt:
            write_vtt(result['segments'], file=fp_vtt)
        logging.info(f'Saved VTT Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: VTT Transcript to: {file_fullpath}')
    # Transcript Format (c): VTT (fragments with timestamps)
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
    # Transcript Format (d): FULL TEXT (One continous documents without timestamps))
    if subdir_fulltext != '':
        file_fullpath = f"./{subdir_fulltext}/{_title}_{_id}_full.txt"
        with open(file_fullpath, "w", encoding="utf-8") as fp_fulltext:
            fp_fulltext.write(result['text'])
        logging.info(f'Saved FULL TEXT Transcript for VideoID:{_id}: {file_fullpath}')
        print(f'Wrote: FULL TEXT Transcript to: {file_fullpath}')

print('EXECTUION COMPLETE')
