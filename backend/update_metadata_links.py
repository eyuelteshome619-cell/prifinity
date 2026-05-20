import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

mongo_uri = os.getenv('MONGO_URI') or os.getenv('MONGODB_URI')
if not mongo_uri:
    print("MONGO_URI not found.")
    exit(1)

try:
    client = MongoClient(mongo_uri)
    db_name = 'ethiopian_recommendations'
    if '/' in mongo_uri.replace('mongodb://', '').replace('mongodb+srv://', ''):
        parts = mongo_uri.split('/')
        if parts[-1]:
            db_name = parts[-1].split('?')[0]
    db = client[db_name]
    print(f"Connected to DB: {db_name}")
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

def search_tvmaze(title):
    try:
        resp = requests.get("https://api.tvmaze.com/search/shows", params={"q": title}, timeout=5)
        if resp.status_code == 200 and resp.json():
            show = resp.json()[0].get('show', {})
            desc = show.get('summary', '') or ''
            desc = desc.replace('<p>', '').replace('</p>', '').replace('<b>', '').replace('</b>', '')
            link = show.get('url', '')
            image = show.get('image', {}).get('original', '') if show.get('image') else ''
            return desc, [{'provider': 'tvmaze', 'url': link}] if link else [], image
    except Exception as e:
        print(f"TVmaze error: {e}")
    return None, [], None

def search_openlibrary(title):
    try:
        resp = requests.get("https://openlibrary.org/search.json", params={"q": title, "limit": 1}, timeout=5)
        if resp.status_code == 200 and resp.json().get('docs'):
            b = resp.json()['docs'][0]
            key = b.get('key', '')
            image = f"https://covers.openlibrary.org/b/id/{b['cover_i']}-L.jpg" if b.get('cover_i') else ''
            link = f"https://openlibrary.org{key}" if key else ''
            return "Book available on OpenLibrary.", [{'provider': 'openlibrary', 'url': link}] if link else [], image
    except Exception as e:
        print(f"OpenLibrary error: {e}")
    return None, [], None

def search_itunes(title):
    try:
        resp = requests.get("https://itunes.apple.com/search", params={"term": title, "media": "music", "limit": 1}, timeout=5)
        if resp.status_code == 200 and resp.json().get('results'):
            t = resp.json()['results'][0]
            desc = t.get('longDescription') or t.get('shortDescription') or "Music track available on iTunes."
            links = []
            if t.get('trackViewUrl'): links.append({'provider': 'itunes', 'url': t.get('trackViewUrl')})
            if t.get('previewUrl'): links.append({'provider': 'itunes_preview', 'url': t.get('previewUrl')})
            image = t.get('artworkUrl100', '').replace('100x100bb', '500x500bb')
            return desc, links, image
    except Exception as e:
        print(f"iTunes error: {e}")
    return None, [], None

items = list(db.items.find())
updated_count = 0

print(f"Found {len(items)} items to process.")

for item in items:
    title = item.get('title')
    item_type = item.get('item_type')
    if not title or not item_type:
        continue
        
    print(f"Processing: {title} ({item_type})")
    
    desc, links, image = None, [], None
    
    if item_type == 'movie':
        desc, links, image = search_tvmaze(title)
    elif item_type == 'book':
        desc, links, image = search_openlibrary(title)
    elif item_type == 'music':
        desc, links, image = search_itunes(title)
        
    update_doc = {}
    
    # Update description if missing or too short
    if desc and (not item.get('description') or len(item.get('description', '')) < 10):
        update_doc['description'] = desc
        
    # Update cover image if missing
    if image and not item.get('cover_image'):
        update_doc['cover_image'] = image
        
    if update_doc:
        db.items.update_one({"_id": item["_id"]}, {"$set": update_doc})
        print(f"  -> Updated metadata for {title}")
        updated_count += 1
        
    # Update external links
    if links:
        for link in links:
            # Check if link exists
            exists = db.external_links.find_one({"item_id": item["_id"], "provider": link['provider']})
            if not exists:
                db.external_links.insert_one({
                    "item_id": item["_id"],
                    "provider": link['provider'],
                    "url": link['url']
                })
                print(f"  -> Added {link['provider']} link for {title}")

print(f"Done! Updated metadata for {updated_count} items.")
