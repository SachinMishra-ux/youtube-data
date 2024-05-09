from googleapiclient.discovery import build
from authenticate import authenticate  # Assuming you have a separate file for authentication
import mysql.connector
from datetime import datetime, timedelta

# Function to connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Root@#123$',
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

def get_video_duration(video_id):
    youtube = build('youtube', 'v3', credentials=authenticate())
    
    request = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    response = request.execute()
    
    # Extract duration from the response
    duration = response['items'][0]['contentDetails']['duration']
    
    return duration

def get_channel_videos(channel_id):
    # Authenticate with the YouTube Data API
    youtube = build('youtube', 'v3', credentials=authenticate())

    # Calculate the date range for today
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    today_iso = today.isoformat() + 'T00:00:00Z'
    tomorrow_iso = tomorrow.isoformat() + 'T00:00:00Z'

    # Retrieve videos uploaded by the specified channel within the date range of today
    videos = []
    next_page_token = None
    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            maxResults=50,  # Max results per page
            order='date',  # Order by date
            publishedAfter=today_iso,
            publishedBefore=tomorrow_iso,
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video data from the response
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_published_at = item['snippet']['publishedAt']
            
            # Fetch video duration
            video_duration = get_video_duration(video_id)

            videos.append({
                'video_id': video_id,
                'title': video_title,
                'published_at': video_published_at,
                'duration': video_duration
            })

        # Check if there are more pages of videos
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # Exit loop if there are no more pages

    return videos

def insert_video_data(subscriber_id,video_id, title, published_at, duration):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Convert published_at to the correct datetime format
    datetime_obj = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
    formatted_published_at = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')


    # SQL query to insert video data into the table
    insert_query = "INSERT IGNORE INTO new_table (subscriber_id, video_id, title, published_at, duration) VALUES (%s, %s, %s, %s, %s)"
    data = (subscriber_id, video_id, title, formatted_published_at, duration)

    cursor.execute(insert_query, data)
    connection.commit()

    cursor.close()
    connection.close()



if __name__ == '__main__':
    channel_id= input("Enter channel ID:")
    subscribers = get_channel_subscribers(channel_id)
    print("Subscribers:", subscribers)

    # Get the videos uploaded by each subscribed channel
    for subscriber_id in subscribers:
        print(f"Videos uploaded by channel {subscriber_id}:")
        videos = get_channel_videos(subscriber_id)
        print(videos)
        for video in videos:
            insert_video_data(subscriber_id, video['video_id'],video['title'],video['published_at'],video['duration'])
            print('data inserted')
            #print(f"Video ID: {video['video_id']}, Title: {video['title']}, Published At: {video['published_at']}, Video Duration: {video['duration']}")