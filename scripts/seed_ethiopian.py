"""
Seed >100 Ethiopian items by querying external APIs and importing via admin endpoint.
Usage:
  ADMIN_TOKEN=your_admin_token python scripts/seed_ethiopian.py --count 120

Requires: requests (in venv)
"""
import os
import sys
import time
import argparse
import requests

API_BASE = os.environ.get('API_BASE', 'http://127.0.0.1:5000/api')
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')

QUERIES = [
    'Tilahun Gessesse', 'Aster Aweke', 'Mahmoud Ahmed', 'Mulatu Astatke', 'Gigi', 'Teddy Afro',
    'Ethiopian traditional music', 'Ethiopian pop', 'Ethiopian jazz', 'Ethiopian folk music',
    'Ethiopian songs', 'Ethiopian singer', 'Ethiopian album', 'Ethiopian soundtrack',
    'Ethiopian instrumental', 'Ethiopian gospel', 'Ethiopian reggae', 'Ethiopian electronic',
    'Ethiopian brass band', 'Ethiopian cultural music', 'Ethiopian classical', 'Ethiopian opera',
    'Ethiopian lullaby', 'Ethiopian wedding music', 'Ethiopian praise songs', 'Ethiopian diaspora music'
]

HEADERS = {
    'Content-Type': 'application/json'
}

if ADMIN_TOKEN:
    HEADERS['Authorization'] = f'Bearer {ADMIN_TOKEN}'


def discover_and_import(query, item_type='music'):
    try:
        r = requests.get(f"{API_BASE}/admin/import/search", params={'type': item_type, 'q': query}, timeout=10, headers=HEADERS)
        if r.status_code != 200:
            return []
        results = r.json().get('results', [])
        imported = []
        for res in results:
            payload = dict(res)
            payload['item_type'] = item_type
            payload['is_ethiopian'] = True
            try:
                ir = requests.post(f"{API_BASE}/admin/import/add", json=payload, timeout=10, headers=HEADERS)
                if ir.status_code in (200, 201):
                    imported.append(ir.json().get('item_id'))
                time.sleep(0.2)
            except Exception:
                continue
        return imported
    except Exception:
        return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=120, help='Number of items to import')
    args = parser.parse_args()

    if not ADMIN_TOKEN:
        print('ADMIN_TOKEN environment variable is required to call admin import endpoints.')
        print('Set it and rerun: ADMIN_TOKEN=... python scripts/seed_ethiopian.py')
        sys.exit(1)

    target = args.count
    created = 0
    idx = 0
    while created < target:
        q = QUERIES[idx % len(QUERIES)] + (f" {idx//len(QUERIES)+1}" if idx // len(QUERIES) > 0 else '')
        print(f"Searching and importing for query: {q}")
        items = discover_and_import(q)
        created += len(items)
        print(f"Imported {len(items)} items (total {created}/{target})")
        idx += 1
        if idx > 1000:
            break
        time.sleep(0.5)

    print(f"Seeding complete. Imported approximately {created} items.")


if __name__ == '__main__':
    main()
