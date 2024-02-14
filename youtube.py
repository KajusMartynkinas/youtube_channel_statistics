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
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data


channel_statistics = get_channel_stats(youtube, channel_ids)

df=pd.DataFrame(channel_statistics)
df['Subscribers'] = pd.to_numeric(df['Subscribers'])
df['Views'] = pd.to_numeric(df['Views'])
df['Total_videos'] = pd.to_numeric(df['Total_videos'])
df['Views_per_video'] = df['Views']/df['Total_videos']




def save_plot(plt, folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
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


if len(channel_ids) > 1:
    subscribers()
    total_videos()
    views()
    views_per_video()

    # print(df)
    df.to_csv('channel_statistics.csv')
    folder_path = 'results'



if len(channel_ids) == 1:
    def get_video_ids(youtube, playlist_id):
        video_ids = []
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50  # Adjust as needed
        )
        response = request.execute()

        for item in response.get('items', []):
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        more_pages = True
        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token)
                response = request.execute()

                for item in response.get('items', []):
                    video_ids.append(item['contentDetails']['videoId'])

                next_page_token = response.get('nextPageToken')

        return video_ids


    for playlist_id in df['playlist_id']:
        video_ids = get_video_ids(youtube, playlist_id)
        print(f"Video IDs for playlist {playlist_id}: {video_ids}")

    video_ids = get_video_ids(youtube, playlist_id)
    # print(video_ids)

    def get_video_details(youtube, video_ids):
        all_video_stats = []

        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part='snippet,statistics',
                id =','.join(video_ids[i:i+50]))
            response = request.execute()

            for video in response['items']:
                video_stats = dict(Title = video['snippet']['title'],
                                   Published_date=video['snippet'].get('publishedAt', 'N/A'),
                                   Views=video['statistics'].get('viewCount', 'N/A'),  # Using .get() with a default value
                                   Likes=video['statistics'].get('likeCount', 'N/A'),  # Using .get() with a default value
                                   Comments=video['statistics'].get('commentCount', 'N/A'))
                all_video_stats.append(video_stats)

        print(all_video_stats)
        return all_video_stats



    video_details = get_video_details(youtube, video_ids)
    video_data = pd.DataFrame(video_details)

    video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
    video_data['Views'] = pd.to_numeric(video_data['Views'], errors='coerce')
    video_data['Likes'] = pd.to_numeric(video_data['Likes'], errors='coerce')
    video_data['Comments'] = pd.to_numeric(video_data['Comments'], errors='coerce')

    def top10_most_viewed():
        top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)

        plt.style.use('dark_background')
        plt.figure(figsize=(24,10))
        sns.barplot(x='Views', y='Title', data= top10_videos, palette='rainbow')
        plt.title('Top 10 Most Viewed Videos')
        save_plot(plt, 'results', 'top10_most_viewed_videos.png')
        plt.show()

    def top10_most_liked():
        top10_liked = video_data.sort_values(by='Likes', ascending=False).head(10)

        plt.style.use('dark_background')
        plt.figure(figsize=(24,10))
        sns.barplot(x='Views', y='Title', data= top10_liked, palette='rainbow')
        plt.title('Top 10 Most Liked Videos')
        save_plot(plt, 'results', 'top10_most_liked_videos.png')
        plt.show()


    def top10_most_commented():
        top10_commented = video_data.sort_values(by='Comments', ascending=False).head(10)

        plt.style.use('dark_background')
        plt.figure(figsize=(24,10))
        sns.barplot(x='Views', y='Title', data= top10_commented, palette='rainbow')
        plt.title('Top 10 Most Commented Videos')
        save_plot(plt, 'results', 'top10_most_commented_videos.png')
        plt.show()


    def video_release():
        video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')
        videos_per_month = video_data.groupby('Month', as_index=False).size()
        sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)

        plt.style.use('dark_background')
        plt.figure(figsize=(14,9))
        sns.barplot(x='Month', y='size', data=videos_per_month, palette='rainbow')
        plt.title('Montly Video Release')
        save_plot(plt, 'results', 'video_release.png')
        plt.show()

    top10_most_viewed()
    top10_most_liked()
    top10_most_commented()
    video_release()
    video_data.to_csv('videos.csv')