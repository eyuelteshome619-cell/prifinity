"""
Full System Review Script - Tests all endpoints and reports issues.
"""
import sys
import requests
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.database import execute_query
from app.utils.auth import generate_token

app = create_app()
BASE = 'http://localhost:5000/api'

fails = []
passes = []

client = app.test_client()

def test(label, url, method='GET', headers=None, json_data=None, expect=200):
    try:
        url = url.replace('http://localhost:5000', '')
        if method == 'POST':
            r = client.post(url, json=json_data, headers=headers)
        else:
            r = client.get(url, headers=headers)
        
        if r.status_code == expect:
            passes.append(label)
            print(f'  [PASS] {label}')
            return r
        else:
            body = r.get_data(as_text=True)[:300]
            fails.append((label, r.status_code, body))
            print(f'  [FAIL] {label} -> {r.status_code}: {body}')
            return r
    except Exception as e:
        fails.append((label, 0, str(e)))
        print(f'  [ERR ] {label} -> {e}')
        return None

with app.app_context():
    user = execute_query('SELECT * FROM users LIMIT 1', fetch_one=True)
    if not user:
        print('ERROR: No users in database!')
        sys.exit(1)

    print(f"Using user: {user['username']} ({user['role']}) id={user['id']}")
    token = generate_token(user['id'], user['role'])
    H = {'Authorization': f'Bearer {token}'}

    print('\n=== 1. PUBLIC ITEM ENDPOINTS ===')
    test('List all items', f'{BASE}/items')
    test('List movies', f'{BASE}/items?type=movie')
    test('List books', f'{BASE}/items?type=book')
    test('List music', f'{BASE}/items?type=music')
    test('Get single item (id=34)', f'{BASE}/items/34')
    test('Popular items', f'{BASE}/items/popular')
    test('Genres list', f'{BASE}/items/genres')
    test('Ethiopian items', f'{BASE}/items/ethiopian')
    test('Ethiopian genres', f'{BASE}/items/ethiopian-genres')

    print('\n=== 2. AUTH ENDPOINTS ===')
    r = test('Login with admin@example.com', f'{BASE}/auth/login', 'POST', 
             json_data={'email': user['email'], 'password': 'password'})
    
    print('\n=== 3. USER ENDPOINTS ===')
    test('Get user profile', f'{BASE}/users/profile', headers=H)
    test('Get user ratings', f'{BASE}/users/ratings', headers=H)
    test('Get user activity', f'{BASE}/users/activity', headers=H)
    r = test('Rate an item', f'{BASE}/users/rate', 'POST', H, 
             {'item_id': 34, 'rating': 4, 'review': 'Great item!'})

    print('\n=== 4. RECOMMENDATION ENDPOINTS ===')
    test('Cold-start (public)', f'{BASE}/recommendations/cold-start')
    test('Personalized recs', f'{BASE}/recommendations', headers=H)
    test('Similar items (id=34)', f'{BASE}/recommendations/similar/34', headers=H)
    test('Ethiopian recs', f'{BASE}/recommendations/ethiopian', headers=H)
    test('Rec history', f'{BASE}/recommendations/history', headers=H)

    print('\n=== 5. ADMIN ENDPOINTS ===')
    test('Admin stats', f'{BASE}/admin/stats', headers=H)
    test('Admin users list', f'{BASE}/admin/users', headers=H)
    test('Admin activity', f'{BASE}/admin/activity', headers=H)
    test('Admin item search', f'{BASE}/admin/items/search?q=avatar', headers=H)
    test('Import search: movie', f'{BASE}/admin/import/search?type=movie&q=Inception', headers=H)
    test('Import search: book', f'{BASE}/admin/import/search?type=book&q=Harry+Potter', headers=H)
    test('Import search: music', f'{BASE}/admin/import/search?type=music&q=Tizita', headers=H)

    print('\n=== 6. ITEM DETAIL DATA CHECK ===')
    r_item = client.get('/api/items/34')
    if r_item.status_code == 200:
        data = r_item.get_json()
        item = data.get('item', {})
        ext_links = data.get('external_links', [])
        ratings = data.get('ratings', [])
        print(f'  title: {item.get("title")}')
        print(f'  description: {repr(item.get("description","")[:80])}')
        print(f'  cover_image: {bool(item.get("cover_image"))}')
        print(f'  avg_rating: {item.get("avg_rating")} ({item.get("rating_count")} ratings)')
        print(f'  external_links count: {len(ext_links)}')
        for lnk in ext_links:
            print(f'    - {lnk.get("provider")}: {lnk.get("url")}')
        print(f'  recent ratings count: {len(ratings)}')
    
    print('\n==============================')
    print(f'RESULTS: {len(passes)} passed, {len(fails)} failed')
    if fails:
        print('\nFAILED ENDPOINTS:')
        for label, status, body in fails:
            print(f'  [{status}] {label}')
            print(f'       {body}')
    else:
        print('ALL ENDPOINTS PASSING!')
