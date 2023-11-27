import json
import os

import requests


def get_playcount(lastfm_id: str, track_title: str, artist_name: str) -> int:
    api_key = os.environ.get("LASTFM_API_KEY")
    url = f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&track={track_title}&artist={artist_name}&username={lastfm_id}&format=json"

    response = requests.get(url)
    data = json.loads(response.text)

    try:
        if "error" not in data.keys():
            return int(data["track"]["userplaycount"])
    except KeyError:
        return 0
