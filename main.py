import os, sys, shutil, schedule, time, traceback
from datetime import datetime
from config           import OUTPUT_DIR, ASSETS_DIR, UPLOAD_TIME
from script_generator import generate_video_content
from tts_generator    import generate_all_audio
from image_fetcher    import fetch_image, save_image
from video_assembler  import assemble_video
from youtube_uploader import upload_video

def setup():
    for d in [OUTPUT_DIR, f"{OUTPUT_DIR}/audio", f"{OUTPUT_DIR}/images", ASSETS_DIR]:
        os.makedirs(d, exist_ok=True)

def cleanup():
    for sub in ["audio","images"]:
        p = os.path.join(OUTPUT_DIR,sub)
        if os.path.exists(p): shutil.rmtree(p)
    fp = os.path.join(OUTPUT_DIR,"final_video.mp4")
    if os.path.exists(fp): os.remove(fp)
    print("[Cleanup] Done")

def run_pipeline():
    print(f"\n{'='*50}")
    print(f"[BOT] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    try:
        setup()

        print("\n[1/5] Generating script...")
        script = generate_video_content()

        print("\n[2/5] Generating voiceover...")
        audio_files = generate_all_audio(script)

        print("\n[3/5] Fetching images...")
        image_paths = {}
        for fact in script["facts"]:
            n = fact["fact_number"]
            img = fetch_image(fact["image_query"], index=n%4)
            image_paths[f"fact_{n}"] = save_image(img, f"fact_{n}.jpg")

        print("\n[4/5] Assembling video...")
        video = assemble_video(
            script, audio_files, image_paths,
            os.path.join(OUTPUT_DIR,"final_video.mp4")
        )

        print("\n[5/5] Uploading to YouTube...")
        vid_id = upload_video(video, script)

        print(f"\nSHORT LIVE: https://youtube.com/shorts/{vid_id}")
        cleanup()

    except Exception as e:
        print(f"\nPipeline failed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if "--now" in sys.argv:
        run_pipeline()
    else:
        print(f"Bot running | Daily at {UPLOAD_TIME} | Ctrl+C to stop")
        schedule.every().day.at(UPLOAD_TIME).do(run_pipeline)
        # Uncomment to test immediately on your PC:
        #run_pipeline()
        while True:
            schedule.run_pending()
            time.sleep(60)
