import requests
import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
video_links = []

client_id = '35a7174b24a640a6a89669d1e9d6770a'
client_secret = '935b2bf0b9774b8dbf2681c3d0b9791f'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = sp.Spotify(client_credentials_manager=client_credentials_manager)


def playlist_tracks(sp,playlist_id):
    tracks_response = sp.playlist_tracks(playlist_id)
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response["items"])

    return tracks

playlist = '6p3IRyXLrl28mu33AHtqnj'
results = playlist_tracks(sp, playlist)
for track_info in results['items']:
    track_name = track_info['track']['name']
    print(f"Track Name: {track_name}")

for track in results:
    try:
        search_query = f"{track['track']['name']} {track['track']['artists'][0]['name']} official audio"
        search_results = YouTube(f"https://www.youtube.com/results?search_query={search_query}")

        video_link = search_results.results[0].videolink
        video_links.append(video_link)

    except Exception as e:
        print(f"Error processing track {track['track']['name']}: {e}")


def download_audio(link):
    try:
        selected_video = YouTube(link)
        audio = selected_video.streams.filter(only_audio=True, file_extension='mp4')[0]
        audio.download()
    except:
        print("Connection Error")

