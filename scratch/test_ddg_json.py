import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def test_ddg_json(query):
    print(f"Testing DDG JSON search for: '{query}'")
    # 1. Get VQD token
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'vqd=([\d-]+)', html)
            if not match:
                match = re.search(r'vqd=["\']([\d-]+)["\']', html)
            if not match:
                # Let's search inside script tags or the whole page
                match = re.search(r'vqd\s*[:=]\s*["\']?([\d-]+)["\']?', html)
                
            if not match:
                print("Failed to find VQD token in HTML response.")
                return
            
            vqd = match.group(1)
            print(f"Found VQD: {vqd}")
            
            # 2. Get JSON results
            json_url = f"https://duckduckgo.com/i.js?q={urllib.parse.quote(query)}&o=json&vqd={vqd}"
            req_json = urllib.request.Request(json_url, headers=headers)
            with urllib.request.urlopen(req_json) as resp_json:
                data = json.loads(resp_json.read().decode('utf-8'))
                results = data.get('results', [])
                print(f"Found {len(results)} images!")
                for i, r in enumerate(results[:5]):
                    print(f"  {i+1}. Title: {r.get('title')}")
                    print(f"     Image: {r.get('image')}")
    except Exception as e:
        print("Error:", e)

test_ddg_json("Chauvet Freedom Par H9 IP")
