import requests, os
from PIL import Image
from io import BytesIO
from config import PEXELS_API_KEY, OUTPUT_DIR

HEADERS = {"Authorization": PEXELS_API_KEY}

def fetch_image(query, index=0):
    print(f"[Images] Fetching: {query}")
    try:
        r = requests.get(
            "https://api.pexels.com/v1/search",
            headers=HEADERS,
            params={"query": query, "per_page": 5, "orientation": "landscape"},
            timeout=10
        )
        photos = r.json().get("photos", [])
        if not photos:
            r = requests.get(
                "https://api.pexels.com/v1/search",
                headers=HEADERS,
                params={"query": "science nature universe", "per_page": 5},
                timeout=10
            )
            photos = r.json().get("photos", [])
        photo   = photos[index % len(photos)]
        img_url = photo["src"]["large2x"]
        img_r   = requests.get(img_url, timeout=20)
        return Image.open(BytesIO(img_r.content)).convert("RGB")
    except Exception as e:
        print(f"[Images] Error — using blank: {e}")
        return Image.new("RGB", (1920, 1080), (15, 15, 30))

def save_image(img, filename):
    path = os.path.join(OUTPUT_DIR, "images", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path
