from parse import *
import requests
import os
import csv


def download_lyrics():
    # ----- DOWNLOAD LYRICS

    # Variables needed to call the API
    url_tracks = 'http://api.musixmatch.com/ws/1.1/track.search'
    url_lyrics = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get'
    apikey = os.environ['APIKEY']

    print('Downloading...')
    lyrics = []
    # Pop, Hip/hop, Raggae
    genre_ids = [14, 18, 24]
    for i in genre_ids:
        for j in range(1, 15):
            params = dict(
                apikey=apikey,
                page=str(j),
                f_music_genre_id=str(i),
                page_size='70',
                f_lyrics_language='en',
                f_has_lyrics='1'
            )

            # Send request for finding tracks
            resp = requests.get(url=url_tracks, params=params)
            json_data = resp.json()
            try:
                data = [parse_track(track)
                        for track in json_data['message']['body']['track_list']]
            except Exception:
                data = []
                pass

            # For all tracks find and store lyrics
            for track_id, genre in data:
                lyrics.append((parse_lyrics(url_lyrics, track_id, apikey), genre))

    print('Saving ' + len(lyrics) + ' to csv file...')

    with open('lyrics.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lyrics)