from googleapiclient.discovery import build
from authenticate import authenticate  # Assuming you have a separate file for authentication
import mysql.connector

# Function to connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Password',
        database='youtubedata'
    )

def get_channel_subscribers(channel_id):
    # Authenticate with the YouTube Data API
    youtube = build('youtube', 'v3', credentials=authenticate())

    # Retrieve the subscribers of the specified channel
    subscribers = []
    next_page_token = None
    while True:
        request = youtube.subscriptions().list(
            part='snippet',
            channelId=channel_id,
            maxResults=2,  # Max results per page
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract subscriber data from the response
        for item in response.get('items', []):
            subscriber_id = item['snippet']['resourceId']['channelId']
            subscribers.append(subscriber_id)

        # Check if there are more pages of subscribers
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # Exit loop if there are no more pages

    return subscribers

def get_channel_videos(channel_id):
    # Authenticate with the YouTube Data API
    youtube = build('youtube', 'v3', credentials=authenticate())

    # Retrieve videos uploaded by the specified channel
    videos = []
    next_page_token = None
    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            maxResults=50,  # Max results per page
            order='date',  # Order by date
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video data from the response
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_published_at = item['snippet']['publishedAt']
            videos.append({'video_id': video_id, 'title': video_title, 'published_at': video_published_at})

        # Check if there are more pages of videos
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # Exit loop if there are no more pages

    return videos

if __name__ == '__main__':
    #channel_id = 'UC-Sd0wcOgqoUw7fsLAJd8YQ'  # Replace with the ID of the channel you want to fetch subscribers for
    channel_id= input("Enter channel ID:")
    subscribers = get_channel_subscribers(channel_id)
    print("Subscribers:", subscribers)

    # Get the videos uploaded by each subscribed channel
    for subscriber_id in subscribers:
        print(f"Videos uploaded by channel {subscriber_id}:")
        videos = get_channel_videos(subscriber_id)
        for video in videos:
            print(f"Video ID: {video['video_id']}, Title: {video['title']}, Published At: {video['published_at']}")