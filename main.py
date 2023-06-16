import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import schedule
import time

# Ключ для YouTube API
api_key = os.getenv('API_KEY')

# ID видео, которое нужно проверять
video_id = '<video_id>'

def check_comments():
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Получаем количество комментариев на видео
        comments_response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText'
        ).execute()
        num_comments = comments_response['pageInfo']['totalResults']

        # Получаем текущее название видео
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        video_title = video_response['items'][0]['snippet']['title']

        # Создаем новое название видео
        new_title = f'{video_title} ({num_comments} comments)'

        # Обновляем название видео
        update_response = youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': {
                    'title': new_title
                }
            }
        ).execute()

        print(f'Successfully updated title for video {video_id}. New title: {new_title}')

    except HttpError as e:
        print(f'An error occurred: {e}')

# Запускаем задачу каждую минуту
schedule.every(1).minutes.do(check_comments)

while True:
    schedule.run_pending()
    time.sleep(1)
