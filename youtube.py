import matplotlib.pyplot as plt
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import os


print('YouTube Channel Comparison')
print('To continue, enter your API key:')

api_key = input()

channel_ids = []
skip = False

for i in range(1, 11):
    if not skip:
        channel_id = input(f'Enter the {i}th channel ID (or write "skip" to end): \n')
        if channel_id.lower() == 'skip':
            skip = True
        else:
            channel_ids.append(channel_id)

youtube = build('youtube','v3', developerKey = api_key)

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
df['Views_per_video'] = df['Views']/df['Total_videos']


print(df)
df.to_csv('channel_statistics.csv')
folder_path = 'results'

def save_plot(plt, folder_path, file_name):
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Full path for saving the file
    file_path = os.path.join(folder_path, file_name)
    # Save the figure
    plt.savefig(file_path)
    print(f"Plot saved to {file_path}")


def subscribers():
    plt.style.use('dark_background')
    plt.figure(figsize= (14,9))
    plt.title('Comparing Subscribers')
    sns.barplot(x='Channel_name', y = 'Subscribers', data=df, palette='rainbow',
                order=df.sort_values('Subscribers', ascending=False)['Channel_name'])
    save_plot(plt, 'results', 'subscribers_comparison.png')
    plt.show()

def total_videos():
    plt.style.use('dark_background')
    plt.figure(figsize= (14,9))
    plt.title('Comparing Total Amount of Videos')
    sns.barplot(x='Channel_name', y = 'Total_videos', data=df, palette='rainbow',
                order=df.sort_values('Total_videos', ascending=False)['Channel_name'])
    save_plot(plt, 'results', 'total_videos.png')
    plt.show()

def views():
    plt.style.use('dark_background')
    plt.figure(figsize= (14,9))
    plt.title('Comparing Views')
    sns.barplot(x='Channel_name', y = 'Views', data=df, palette='rainbow',
                order=df.sort_values('Views', ascending=False)['Channel_name'])
    save_plot(plt, 'results', 'comparing_views.png')
    plt.show()

def views_per_video():
    plt.style.use('dark_background')
    plt.figure(figsize=(14, 9))
    plt.title('Views per video')
    sns.barplot(x='Channel_name', y='Views_per_video', data=df, palette='rainbow',
                order=df.sort_values('Views_per_video', ascending=False)['Channel_name'])
    save_plot(plt, 'results', 'views_per_video.png')
    plt.show()

subscribers()
total_videos()
views()
views_per_video()