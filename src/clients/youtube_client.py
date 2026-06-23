import googleapiclient.discovery as dis
from urllib.parse import parse_qs, urlparse
from src.config import YOUTUBE_API_KEY

youtube = dis.build("youtube", "v3", developerKey=YOUTUBE_API_KEY) if (YOUTUBE_API_KEY) else None

def trowException(type="not-api-key"):
    if type == "not-api-key":
        raise Exception("YOUTUBE_API_KEY is not assigned.")
    else:
        raise Exception("youtube client risk.")
    
def get_playlist_id(url):
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]
    return playlist_id

def get_playlist_name(playlist_id):
    if youtube == None:
        trowException("not-api-key")
        return

    playlist_response = youtube.playlists().list(part="snippet", id=playlist_id).execute()
    playlist_name = playlist_response["items"][0]["snippet"]["title"]
    return playlist_name

def get_all_links_from_playlist(playlist_id):
    if youtube == None:
        trowException("not-api-key")
        return
    request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=100)
    response = request.execute()
    playlistItems = []

    while request is not None:
        response = request.execute()
        playlistItems += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    links = []
    for item in playlistItems:
        video_id = item["snippet"]["resourceId"]["videoId"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        links.append(link)

    return links
