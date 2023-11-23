import json
import os

import requests


def get_playcount(lastfm_id: str, track_title: str) -> int:
    api_key = os.environ.get("LASTFM_API_KEY")

    # TODO: Requires exception handling if the same track title exist such as
    # adding the artist name as a parameter to last.fm
    url = f"https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&track={track_title}&username={lastfm_id}&format=json"

    response = requests.get(url)
    data = json.loads(response.text)

    try:
        if "error" not in data.keys():
            return int(data["track"]["userplaycount"])
    except KeyError:
        return 0
