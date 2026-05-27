import urllib.request
import re
import urllib.parse

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def test_unsplash(query):
    print(f"Searching Unsplash for: '{query}'")
    encoded = urllib.parse.quote(query)
    url = f"https://unsplash.com/s/photos/{encoded}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            # Find all images starting with https://images.unsplash.com/photo-
            urls = re.findall(r'(https://images.unsplash.com/photo-[^?"]+)', html)
            print(f"Found {len(urls)} urls for '{query}'")
            for i, u in enumerate(list(set(urls))[:10]):
                print(f"  {i+1}. {u}?w=500&auto=format&fit=crop")
    except Exception as e:
        print("Error:", e)

test_unsplash("concert stage lighting")
