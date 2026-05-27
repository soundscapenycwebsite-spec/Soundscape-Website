import urllib.request
import re
import urllib.parse

def test_bing(query):
    encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={encoded}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            # Let's match all murls correctly up to the closing quote entity
            urls = re.findall(r'murl&quot;:&quot;(http.*?)&quot;', html)
            print(f"Found {len(urls)} urls for '{query}'")
            for i, u in enumerate(urls[:10]):
                print(f"  {i+1}. {u}")
    except Exception as e:
        print("Error:", e)

test_bing("Chauvet Freedom Par H9 IP")
