import matplotlib.pyplot as plt
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
df['Subscribers'] = pd.to_numeric(df['Subscribers'])
df['Views'] = pd.to_numeric(df['Views'])
df['Total_videos'] = pd.to_numeric(df['Total_videos'])

print(df)
df.to_csv('channel_statistics.csv')

def subscribers():
    plt.style.use('dark_background')
    plt.figure(figsize= (10,8))
    plt.title('Comparing Subscribers')
    sns.barplot(x='Channel_name', y = 'Subscribers', data=df, palette='rainbow',
                order=df.sort_values('Subscribers', ascending=False)['Channel_name'])
    plt.show()

def total_videos():
    plt.style.use('dark_background')
    plt.figure(figsize= (10,8))
    plt.title('Comparing Total Amount of Videos')
    sns.barplot(x='Channel_name', y = 'Total_videos', data=df, palette='rainbow',
                order=df.sort_values('Total_videos', ascending=False)['Channel_name'])
    plt.show()

def views():
    plt.style.use('dark_background')
    plt.figure(figsize= (10,8))
    plt.title('Comparing Views')
    sns.barplot(x='Channel_name', y = 'Views', data=df, palette='rainbow',
                order=df.sort_values('Views', ascending=False)['Channel_name'])
    plt.show()

subscribers()
total_videos()
views()