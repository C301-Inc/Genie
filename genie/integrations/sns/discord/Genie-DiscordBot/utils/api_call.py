import json

import requests
from utils.constants import BACKEND_ENDPOINT


def get_track_counts(discord_id):
    open_bracket = "{"
    close_bracket = "}"
    body = f"""
        query {open_bracket}
            getTrackCounts (
                discriminator: "{discord_id}"
            ) {open_bracket}
                track {open_bracket}
                    title    
                {close_bracket}
                streamingCount
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=BACKEND_ENDPOINT, json={"query": body})

    data = json.loads(response.text)

    if "errors" in data:
        return []

    return data["data"]["getTrackCounts"]
