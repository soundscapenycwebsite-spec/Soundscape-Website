import urllib.request
import urllib.parse
import re
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

query = '"SWF7246" "DJ Facade"'
print(f"Searching Bing for '{query}'...")
url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
        if not img_urls:
            img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
        
        print("Raw URLs found:")
        for idx, img in enumerate(img_urls[:15]):
            print(f"  [{idx}] {img}")
except Exception as e:
    print(f"Error: {e}")
