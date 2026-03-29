import edge_tts, asyncio, os
from config import TTS_VOICE, OUTPUT_DIR

async def _speak(text, path, voice):
    comm = edge_tts.Communicate(text, voice)
    await comm.save(path)

def generate_tts(text, filename, voice=None):
    if voice is None:
        voice = TTS_VOICE
    path = os.path.join(OUTPUT_DIR, "audio", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"[TTS] Generating: {filename}")
    asyncio.run(_speak(text, path, voice))
    return path

def generate_all_audio(script_data):
    audio = {}
    audio["intro"] = generate_tts(script_data["intro_text"], "intro.mp3")
    for fact in script_data["facts"]:
        n = fact["fact_number"]
        audio[f"fact_{n}"] = generate_tts(
            f"Fact {n}. {fact['narration']}", f"fact_{n}.mp3"
        )
    audio["outro"] = generate_tts(script_data["outro_text"], "outro.mp3")
    print(f"[TTS] Done — {len(audio)} audio files")
    return audio
