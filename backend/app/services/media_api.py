import requests
import json
from flask import current_app
from app.utils.database import execute_query

class MediaAPIService:
    """Simplified and Clean Media API Service"""

    @staticmethod
    def _get_config(config_key):
        try:
            result = execute_query(
                "SELECT config_value FROM site_settings WHERE config_key = %s",
                (config_key,),
                fetch_one=True
            )
            val = result['config_value'] if result and result['config_value'] else None
            if val and not val.startswith('your_'):
                return val
            return None
        except:
            return None

    @staticmethod
    def search(item_type, query):
        if not query: return []
        
        if item_type == 'movie':
            return MediaAPIService._search_tmdb(query)
        elif item_type == 'book':
            return MediaAPIService._search_google_books(query)
        elif item_type == 'music':
            return MediaAPIService._search_itunes(query)
        return []

    @staticmethod
    def get_trending(item_type):
        if item_type == 'movie':
            return MediaAPIService._search_tmdb("2024 bestseller")
        elif item_type == 'book':
            return MediaAPIService._search_google_books("2024 hits")
        elif item_type == 'music':
            return MediaAPIService._search_itunes("2024 top")
        return []

    @staticmethod
    def _search_tmdb(query):
        api_key = MediaAPIService._get_config('TMDB_API_KEY')
        if not api_key: return []
        
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": api_key, "query": query, "language": "en-US"}
        
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                results = []
                for m in resp.json().get('results', [])[:12]:
                    results.append({
                        'external_id': f"tmdb_{m['id']}",
                        'title': m.get('title'),
                        'description': m.get('overview'),
                        'genre': 'Movie',
                        'item_type': 'movie',
                        'cover_image': f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get('poster_path') else None,
                        'release_year': m.get('release_date', '')[:4],
                        'creator': 'Director',
                        'popularity': m.get('popularity', 0)
                    })
                return results
        except: pass
        return []

    @staticmethod
    def _search_google_books(query):
        api_key = MediaAPIService._get_config('GOOGLE_BOOKS_API_KEY')
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": query, "maxResults": 12}
        if api_key: params["key"] = api_key
        
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                results = []
                for b in resp.json().get('items', []):
                    info = b.get('volumeInfo', {})
                    results.append({
                        'external_id': f"gb_{b['id']}",
                        'title': info.get('title'),
                        'description': info.get('description', ''),
                        'genre': info.get('categories', ['Book'])[0],
                        'item_type': 'book',
                        'cover_image': info.get('imageLinks', {}).get('thumbnail'),
                        'release_year': info.get('publishedDate', '')[:4],
                        'creator': info.get('authors', ['Unknown'])[0],
                        'popularity': 50
                    })
                return results
        except: pass
        return []

    @staticmethod
    def _search_itunes(query):
        url = "https://itunes.apple.com/search"
        params = {"term": query, "media": "music", "entity": "song", "limit": 12}
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                results = []
                for t in resp.json().get('results', []):
                    results.append({
                        'external_id': f"itunes_{t['trackId']}",
                        'title': t.get('trackName'),
                        'creator': t.get('artistName'),
                        'album': t.get('collectionName'),
                        'genre': t.get('primaryGenreName', 'Music'),
                        'item_type': 'music',
                        'cover_image': t.get('artworkUrl100', '').replace('100x100bb', '600x600bb'),
                        'release_year': t.get('releaseDate', '')[:4],
                        'popularity': 70
                    })
                return results
        except: pass
        return []

    @staticmethod
    def get_external_details(item_type, external_id):
        # Simplification: The sync route already has all base info
        # This is primarily for fetching detailed credits/casts if needed later
        return None
