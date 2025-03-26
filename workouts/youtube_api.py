import random
from googleapiclient.discovery import build
from django.conf import settings

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

def is_video_available(video_id):
    """Проверяет, доступно ли видео и можно ли его встроить."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    try:
        stats_request = youtube.videos().list(
            part="status",
            id=video_id
        )
        stats_response = stats_request.execute()
        
        if not stats_response.get("items"):
            return False, False  # Видео не найдено

        status = stats_response["items"][0]["status"]
        is_public = status.get("privacyStatus") == "public"
        embeddable = status.get("embeddable", False)  # Можно ли встроить

        return is_public, embeddable

    except Exception as e:
        print(f"Ошибка при проверке видео {video_id}: {e}")
        return False, False


def search_youtube_videos(query, max_results=10):
    """Ищет видео на YouTube, убирает недоступные и сортирует по популярности."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results
        )
        response = request.execute()
    except Exception as e:
        print(f"Ошибка YouTube API: {e}")
        return []  # Если ошибка, возвращаем пустой список

    videos = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]

        is_public, embeddable = is_video_available(video_id)
        if not is_public:
            continue  # Пропускаем скрытые или удаленные видео

        thumbnail_url = item["snippet"].get("thumbnails", {}).get("medium", {}).get("url", "")

        videos.append({
            "title": item["snippet"]["title"],
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "embed_url": video_id if embeddable else None,  # Если нельзя встроить, оставляем None
            "thumbnail": thumbnail_url
        })

    return videos