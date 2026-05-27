import urllib.request
import re
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

url = "https://www.sweetwater.com/store/detail/ColorBandPix--chauvet-dj-colorband-pix-linear-led-wash-light"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        print(f"FETCH SUCCESS! Length: {len(html)} characters.")
        # Try to find images in the HTML
        img_urls = re.findall(r'https://media\.sweetwater\.com/[^\s"\']+', html)
        print(f"Found {len(img_urls)} Sweetwater media URLs:")
        for img in img_urls[:10]:
            print(f"  {img}")
except Exception as e:
    print(f"FETCH FAILED: {e}")
