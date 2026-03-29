import os

# ── Simple .env loader ────────────────────────────────────────────────────────
def _load_env():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_load_env()

# ── API Keys ──────────────────────────────────────────────────────────────────
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY",   "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# ── Video format — vertical Shorts 9:16 ──────────────────────────────────────
VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920
FPS          = 30
NUM_FACTS    = 5      # 5 facts x ~10s = ~50s (must stay under 60s!)

# ── Voice ─────────────────────────────────────────────────────────────────────
TTS_VOICE = "en-US-GuyNeural"
# TTS_VOICE = "en-US-JennyNeural"  # Female — uncomment to switch

# ── Background music ──────────────────────────────────────────────────────────
BACKGROUND_MUSIC_PATH   = "assets/bg_music.mp3"
BACKGROUND_MUSIC_VOLUME = 0.08

# ── Local scheduler ───────────────────────────────────────────────────────────
UPLOAD_TIME = "10:00"

# ── Paths ─────────────────────────────────────────────────────────────────────
OUTPUT_DIR = "output"
ASSETS_DIR = "assets"

# ── Topic pool ────────────────────────────────────────────────────────────────
TOPICS = [
    "space and astronomy",    "deep ocean creatures",   "human brain facts",
    "ancient Egypt secrets",  "animal superpowers",     "quantum physics",
    "world geography facts",  "dinosaur discoveries",   "psychology tricks",
    "bizarre food facts",     "historical mysteries",   "human body facts",
    "extreme weather events", "AI and technology",      "mathematics facts",
    "famous inventors",       "medieval history",       "black holes",
    "dreams and sleep",       "lost civilizations",     "volcanoes",
    "coral reefs",            "bizarre world records",  "optical illusions",
    "animal camouflage",      "deep space missions",    "fungi facts",
    "ancient rome",           "extreme survival",       "underwater caves",
    "insect world",           "arctic and antarctic",   "rainforest secrets",
]
