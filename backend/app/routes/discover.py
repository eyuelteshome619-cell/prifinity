"""
Discovery Routes - Trending and External Sync
"""
from flask import Blueprint, request, jsonify, g
from app.utils.database import execute_query
from app.utils.auth import token_required
from app.services.media_api import MediaAPIService
import json

discover_bp = Blueprint('discover', __name__)

@discover_bp.route('/trending', methods=['GET'])
def get_trending():
    """Get trending items from external APIs"""
    item_type = request.args.get('type', 'movie') # movie, music, book
    try:
        trending = MediaAPIService.get_trending(item_type)
        return set_synced(trending)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@discover_bp.route('/version', methods=['GET'])
def get_version():
    return jsonify({'version': '1.0.10', 'status': 'Master Patch Applied'}), 200

def set_synced(results):
    """Augment search results with local database IDs if they exist and are complete"""
    if not results: return jsonify({'results': []}), 200
    
    for r in results:
        ext_id = r.get('external_id')
        item_type = r.get('item_type')
        if ext_id:
            try:
                db_item = execute_query(
                    "SELECT id FROM items WHERE external_id = %s AND item_type = %s",
                    (ext_id, item_type),
                    fetch_one=True
                )
                if db_item:
                    # VERIFY: Ensure the item actually exists in its subtype table too
                    table_map = {'movie': 'movies', 'music': 'music', 'book': 'books'}
                    subtype = execute_query(
                        f"SELECT item_id FROM {table_map[item_type]} WHERE item_id = %s",
                        (db_item['id'],),
                        fetch_one=True
                    )
                    if subtype:
                        r['id'] = db_item['id']
                        r['is_synced'] = True
                    else:
                        # Orphan item! Items row exists but type-specific row is missing
                        r['id'] = None
                        r['is_synced'] = False
                else:
                    r['id'] = None
                    r['is_synced'] = False
            except:
                r['id'] = None
                r['is_synced'] = False
    return jsonify({'results': results}), 200

@discover_bp.route('/search', methods=['GET'])
def search_external():
    """Live search external APIs"""
    item_type = request.args.get('type', 'movie') # movie, music, book
    query = request.args.get('q')
    
    if not query:
        return jsonify({'results': []}), 200
        
    try:
        results = MediaAPIService.search(item_type, query)
        return set_synced(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@discover_bp.route('/sync', methods=['POST'])
@token_required
def sync_external_item():
    data = request.get_json()
    external_id = data.get('external_id')
    item_type = data.get('item_type')
    
    if not external_id or not item_type:
        return jsonify({'error': 'Missing identification fields'}), 400

    # 1. Truncate long strings to prevent DB crashes (VARCHAR 255 limit)
    data['title'] = str(data.get('title', 'Unknown'))[:250]
    if data.get('description'):
        data['description'] = str(data['description'])[:2000] # TEXT limit is safe but let's be safe
    if data.get('genre'):
        data['genre'] = str(data['genre'])[:90]
    if data.get('creator'):
        data['creator'] = str(data['creator'])[:250]
    if data.get('album'):
        data['album'] = str(data['album'])[:250]

    # 2. Check if already exists (and is complete)
    item = execute_query(
        "SELECT id FROM items WHERE external_id = %s AND item_type = %s",
        (external_id, item_type),
        fetch_one=True
    )
    
    main_item_id = item['id'] if item else None
    
    try:
        if main_item_id:
            # Update base item
            execute_query(
                """UPDATE items 
                   SET title=%s, description=%s, genre=%s, cover_image=%s, popularity_score=%s
                   WHERE id=%s""",
                (data['title'], data.get('description', ''), data.get('genre', 'Other'), 
                 data.get('cover_image', ''), data.get('popularity', 0), main_item_id),
                fetch_all=False
            )
        else:
            # Insert base item
            main_item_id = execute_query(
                """INSERT INTO items (title, description, genre, item_type, cover_image, popularity_score, external_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (data['title'], data.get('description', ''), data.get('genre', 'Other'), item_type, 
                 data.get('cover_image', ''), data.get('popularity', 0), external_id),
                fetch_all=False
            )
        
        # 3. Clean release_year
        raw_year = data.get('release_year')
        try:
            clean_year = int(str(raw_year)[:4]) if raw_year and str(raw_year).strip() else None
        except:
            clean_year = None

        # 4. Insert or Update type-specific details
        if item_type == 'movie':
            execute_query(
                """INSERT INTO movies (item_id, director, release_year) 
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE director=%s, release_year=%s""",
                (main_item_id, data.get('creator', 'Unknown'), clean_year,
                 data.get('creator', 'Unknown'), clean_year),
                fetch_all=False
            )
        elif item_type == 'music':
            creator = data.get('creator') or data.get('artist') or 'Unknown Artist'
            album = data.get('album') or ''
            execute_query(
                """INSERT INTO music (item_id, artist, album, release_year, spotify_id) 
                   VALUES (%s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE artist=%s, album=%s, release_year=%s, spotify_id=%s""",
                (main_item_id, creator, album, clean_year, external_id,
                 creator, album, clean_year, external_id),
                fetch_all=False
            )
        elif item_type == 'book':
            execute_query(
                """INSERT INTO books (item_id, author, publication_year) 
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE author=%s, publication_year=%s""",
                (main_item_id, data.get('creator', 'Unknown'), clean_year,
                 data.get('creator', 'Unknown'), clean_year),
                fetch_all=False
            )
            
        return jsonify({'message': 'Success', 'item_id': main_item_id}), 201
        
    except Exception as e:
        print(f"MASTER SYNC ERROR: {str(e)}")
        return jsonify({'error': str(e)}), 500
