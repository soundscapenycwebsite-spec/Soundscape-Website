import urllib.request
import os

def download_image(url, output_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"Successfully downloaded {url} to {output_path} ({os.path.getsize(output_path)} bytes)")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Shure SM58 dynamic mic image on Wikimedia
url = "https://upload.wikimedia.org/wikipedia/commons/e/ec/Shure-SM58-Microphone.jpg"
out_path = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets\gear_sm58_mic.jpg"
download_image(url, out_path)
