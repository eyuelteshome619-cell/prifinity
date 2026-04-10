import requests
import json
from flask import current_app
from app.utils.database import execute_query

class MediaAPIService:
    """STRICT MOVIE-ONLY Media API Service"""

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
        
        # WE ARE ONLY ALLOWING MOVIES FOR NOW
        if item_type == 'movie':
            return MediaAPIService._search_tmdb(query)
        return []

    @staticmethod
    def get_trending(item_type):
        # WE ARE ONLY ALLOWING MOVIES FOR NOW
        if item_type == 'movie':
            return MediaAPIService._search_tmdb("trending")
        return []

    @staticmethod
    def _search_tmdb(query):
        api_key = MediaAPIService._get_config('TMDB_API_KEY')
        if not api_key: return []
        
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": api_key, "query": query, "language": "en-US"}
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                results = []
                for m in resp.json().get('results', [])[:20]:
                    if not m.get('poster_path'): continue
                    
                    results.append({
                        'external_id': f"tmdb_{m['id']}",
                        'title': m.get('title'),
                        'description': m.get('overview', 'No description available.'),
                        'genre': 'Movie',
                        'item_type': 'movie',
                        'cover_image': f"https://image.tmdb.org/t/p/w500{m['poster_path']}",
                        'release_year': m.get('release_date', '')[:4],
                        'creator': 'Director',
                        'popularity': m.get('popularity', 0)
                    })
                return results
        except Exception as e:
            print(f"TMDB Search Error: {e}")
        return []

    @staticmethod
    def get_external_details(item_type, external_id):
        return None
