"""
Compatibility shim for legacy `spotify` utilities.

This project no longer uses the Spotify Web API. The former helpers
are kept as a compatibility layer that maps requests to Last.fm where
possible. Callers can still import `search_spotify_track` but will
receive Last.fm search results instead.
"""
import os
from app.utils import lastfm


def search_spotify_track(title, artist=""):
    """Backward-compatible function: returns Last.fm track info when available.

    Returns a dict with keys `name`, `artist`, `url`, `mbid` or None.
    """
    try:
        return lastfm.search_lastfm_track(title, artist)
    except Exception:
        return None
