import urllib.request
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

url = "https://www.bhphotovideo.com/images/images2500x2500/chauvet_dj_intimspot260x_intimidator_spot_260x_75w_1666878.jpg"
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=5) as response:
        print(f"HTTP Status: {response.status}")
        content = response.read()
        print(f"Content Length: {len(content)} bytes")
except Exception as e:
    print(f"Error occurred: {e}")
