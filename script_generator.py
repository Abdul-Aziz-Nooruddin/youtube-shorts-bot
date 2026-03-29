import requests, json, random, os
from config import GROQ_API_KEY, TOPICS, NUM_FACTS

USED_FILE = "used_topics.json"

def _load_used():
    if os.path.exists(USED_FILE):
        with open(USED_FILE, "r") as f:
            return json.load(f)
    return []

def _save_used(used):
    with open(USED_FILE, "w") as f:
        json.dump(used, f, indent=2)

def _pick_topic():
    used = _load_used()

    # All topics used — reset and start fresh
    remaining = [t for t in TOPICS if t not in used]
    if not remaining:
        print("[Script] All topics used — resetting list")
        used = []
        _save_used(used)
        remaining = TOPICS[:]

    # Pick a random unused topic
    topic = random.choice(remaining)
    used.append(topic)
    _save_used(used)

    print(f"[Script] Topic: {topic}")
    print(f"[Script] Used {len(used)}/{len(TOPICS)} topics total")
    return topic

def generate_video_content(topic=None):
    if topic is None:
        topic = _pick_topic()

    prompt = f"""You create viral YouTube Shorts for a facts channel.
Topic: {topic}

Return ONLY valid JSON — no markdown, no code fences, no explanation:
{{
  "topic": "{topic}",
  "title": "Catchy hook title under 60 characters. Must end with #Shorts",
  "description": "100-word engaging description. End with: #Shorts #Facts #DidYouKnow #{topic.replace(' ', '')} #Educational #Viral #FunFacts",
  "tags": ["Shorts","facts","didyouknow","educational","{topic.replace(' ', '')}","funfacts","viral","mindblowing","amazing","science"],
  "intro_text": "One shocking hook sentence under 20 words. No welcome — start with the most surprising thing.",
  "facts": [
    {{
      "fact_number": 1,
      "narration": "One punchy sentence under 20 words. Shocking and accurate.",
      "image_query": "specific Pexels image search term (e.g. 'milky way galaxy night sky')",
      "overlay_text": "3-5 WORD HEADLINE IN CAPS"
    }}
  ],
  "outro_text": "Follow for daily facts! Drop a comment if this surprised you."
}}

Generate exactly {NUM_FACTS} facts. Keep every narration under 20 words."""

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.85,
                "max_tokens": 2000
            },
            timeout=30
        )
        content = r.json()["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        data = json.loads(content.strip())
        print(f"[Script] OK: {data['title']}")
        return data

    except Exception as e:
        print(f"[Script] Error: {e}")
        raise
