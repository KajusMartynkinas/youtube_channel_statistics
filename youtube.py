from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyCuG4t1hofbFCTEVmjglqrECwmYUTmuSRc'

channel_id = 'UCq6VFHwMzcMXbuKyG7SQYIg'
channel_ids = ['UCq6VFHwMzcMXbuKyG7SQYIg',
               'UCo_IB5145EVNcf8hw1Kku7w',
               'UC3sznuotAs2ohg_U__Jzj_Q',
               'UCHYoe8kQ-7Gn9ASOlmI0k6Q',
               'UCd4t3EEUy0LUOM4MTdjpNHA']

youtube = build('youtube','v3', developerKey = api_key)

# Function to get channel statistics

def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part = 'snippet,contentDetails,statistics',
        id = ','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'])
        all_data.append(data)

    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)

df = pd.DataFrame(channel_statistics)

print(df)

df.to_csv('channel_statistics.csv')