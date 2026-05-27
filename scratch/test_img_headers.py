import urllib.request
import urllib.error

url = "https://media.sweetwater.com/images/items/750/EW500G4-935-large.jpg"

header_combinations = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.sweetwater.com/',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.sweetwater.com/store/detail/EW500G4935--',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'image/avif,image/webp,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.sweetwater.com/'
    }
]

for i, headers in enumerate(header_combinations):
    print(f"\n--- Combination {i+1} ---")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read()
            print(f"SUCCESS! Downloaded {len(content)} bytes.")
            break
    except Exception as e:
        print(f"FAILED: {e}")
