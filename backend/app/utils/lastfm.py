import os
import requests
import urllib.parse
from flask import current_app


def _get_api_key():
    # Prefer explicit env var, fall back to Flask config if available
    key = os.environ.get('LASTFM_API_KEY')
    if key:
        return key
    try:
        return current_app.config.get('LASTFM_API_KEY')
    except Exception:
        return None


def search_lastfm_track(title: str, artist: str = "") -> dict | None:
    """Search Last.fm for a track and return a small dict with url/mbid/name/artist.

    Returns None on error or when no results are found.
    """
    api_key = _get_api_key()
    if not api_key:
        return None

    params = {
        'method': 'track.search',
        'track': title,
        'api_key': api_key,
        'format': 'json',
        'limit': 1,
    }
    if artist:
        params['artist'] = artist

    try:
        resp = requests.get('https://ws.audioscrobbler.com/2.0/', params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()

        tracks = data.get('results', {}).get('trackmatches', {}).get('track', [])
        if not tracks:
            return None

        # If API returns a single track as dict, normalize to list
        if isinstance(tracks, dict):
            tracks = [tracks]

        t = tracks[0]
        return {
            'name': t.get('name'),
            'artist': t.get('artist'),
            'url': t.get('url'),
            'mbid': t.get('mbid') or None,
        }
    except Exception:
        return None


def build_lastfm_search_url(title: str, artist: str = "") -> str:
    """Return a Last.fm search URL for the given title/artist fallback."""
    q = f"{title} {artist}".strip()
    return f"https://www.last.fm/search?q={urllib.parse.quote_plus(q)}"
