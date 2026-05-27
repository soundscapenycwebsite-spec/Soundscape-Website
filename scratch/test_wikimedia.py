import urllib.request
import urllib.parse
import json

headers = {
    'User-Agent': 'SoundscapeNYCImageBot/1.0 (contact@soundscapenyc.com)'
}

def test_wikimedia(query):
    print(f"Searching Wikimedia Commons for: '{query}'")
    encoded = urllib.parse.quote(query)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded}&srnamespace=6&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get('query', {}).get('search', [])
            print(f"Found {len(results)} results!")
            for i, r in enumerate(results[:5]):
                title = r.get('title')
                print(f"  {i+1}. Title: {title}")
                
                # Fetch direct image URL
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
                req_info = urllib.request.Request(info_url, headers=headers)
                with urllib.request.urlopen(req_info) as resp_info:
                    info_data = json.loads(resp_info.read().decode('utf-8'))
                    pages = info_data.get('query', {}).get('pages', {})
                    for p_id, p_info in pages.items():
                        image_info = p_info.get('imageinfo', [])
                        if image_info:
                            print(f"     Direct URL: {image_info[0].get('url')}")
    except Exception as e:
        print("Error:", e)

test_wikimedia("stage lighting fixture moving head")
