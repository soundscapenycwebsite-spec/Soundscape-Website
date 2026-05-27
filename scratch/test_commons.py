import urllib.request
import urllib.parse
import json

def test_commons_search(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    # Query Wikimedia Commons for files matching the search query
    params = {
        'action': 'query',
        'generator': 'search',
        'gsrsearch': query,
        'gsrnamespace': 6,  # File namespace
        'prop': 'imageinfo',
        'iiprop': 'url',
        'format': 'json',
        'gsrlimit': 5
    }
    query_str = urllib.parse.urlencode(params)
    url = f"https://commons.wikimedia.org/w/api.php?{query_str}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            print(f"Found {len(pages)} pages in Wikimedia Commons for '{query}':")
            for page_id, page_data in pages.items():
                title = page_data.get('title')
                img_info = page_data.get('imageinfo', [])
                if img_info:
                    img_url = img_info[0].get('url')
                    print(f"File: {title} -> URL: {img_url}")
    except Exception as e:
        print(f"Error for '{query}': {e}")

test_commons_search("Shure SM58")
