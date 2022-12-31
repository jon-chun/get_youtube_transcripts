# **Get YouTube Transcripts**

This repo provides Python code to scrape transcripts from multiple videos within a choosen YouTube Channel.

---
## **Description**

This repo consists of two sequential python files. In addition, one equivalent Jupyter notebook that unifies the two programs will be added shortly.

The two python programs that need to be executed in sequence are:

1. **get_yt_channel_videos_ids.py**: get the unique video_id for every video within a YouTube channel

2. **get_yt_transcripts_by_ids.py**: scrape the YouTube SRT transcript for every video that has one.

---
## **Getting Started**

* Clone this Repo:

    1. git clone https://github.com/jon-chun/get_youtube_transcripts.git



---
## **Dependencies**

* pandas (including numpy)
* youtube-transcript-api

---
## **Installing**

* Create a virtual environment and switch into it
* git clone https://github.com/jon-chun/get_youtube_transcripts.git
* pip install -r requirements.txt

---
## **Executing Program**

* Setup Credentials

    1. Login to Google and get an API Key from Google Console <a href="https://console.cloud.google.com/apis/credentials">API & Services</a> submenu

    2. Copy 'credentials_template.py' to 'credentials.py'

    3. Edit 'credentials.py' by inserting your Google API Key where indicated.

 * Get the YouTube "channel_id" and all the "video_id"s in that channel to scrape.
 
    1. Find the **YouTube Channel ID** using this <a href="https://www.youtube.com/channel/UCvShfJtvC2owV0AFi_qyy">procedure</a>

    2. Edit the **configuration.py**' by setting the value "**channel_id = X**" where X is the YouTube Channel ID found in step #1. Also, give a user-friendly name for this Channel (no spaces or punctuation)
    
    3. Run '**get_yt_channel_video_ids.py**' to get a list of all the video_ids in the given channel. The video_ids are written in the file: '**video_ids___(channel_name)___(channel_id)___(datetime).csv**'

* Scrape modified SRT Transcripts (to *.json files) for each video in the target YouTube channel

    1. Run '**get_yt_transcripts_by_ids.py**' which

        a. Creates a new subdir to hold all SRT transcript *.json files under **data___(channel_name)___(channel_id)**

        b. Tries to scrape each YouTube Channel Video by '**video_id**' into a filename: '**(video_title)___(date)___(video_channel)___(video_id).json**'

        c. Creates a logfile of all successes, failures and duplicates (will not scrape a transcript that already exists)

* **NOTE**: For various reasons, some YouTube Videos within a Channel may not be successfully scraped (e.g. due to traffic, rate limiting blocks, etc). If this happens, you can rerun **get_yt_transcripts_by_id.py** repeatedly as it will skip over videos that were already scraped and only attempt to download SRT transcripts for videos that previously failed to download.

* **OUTPUT**: Each YouTube Video transcript rearranges SRT information to make a valid JSON file. The **key** is the start time of an utterance and the **value** is a list of the ['text','duration']

---
## **Help**

Please open an Issue for common problems or feature requests

---
## **Authors**

Jon Chun 
* Twitter: [@jonchun2000](https://twitter.com/jonchun2000)

---
## **Version History**

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

---
## **License**

This project is licensed under the MIT License - see the LICENSE.md file for details

---
## **Acknowledgments**

Inspiration, code snippets, etc.
* [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)
