import urllib.request
import urllib.parse
import json

def test_qwant_images(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    url = f"https://api.qwant.com/v3/search/images?q={urllib.parse.quote(query)}&count=5&locale=en_US&uiv=4"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('data', {}).get('result', {}).get('items', [])
            print(f"Found {len(items)} items for '{query}':")
            for i, item in enumerate(items[:3]):
                print(f"Result {i+1}: {item.get('media')}")
    except Exception as e:
        print(f"Error for '{query}': {e}")

test_qwant_images("Shure SM58 microphone png")
