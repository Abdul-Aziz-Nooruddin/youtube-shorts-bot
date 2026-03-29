import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from moviepy.editor import (
    ImageClip, AudioFileClip,
    concatenate_videoclips, CompositeAudioClip
)
from config import (
    OUTPUT_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, FPS,
    BACKGROUND_MUSIC_PATH, BACKGROUND_MUSIC_VOLUME
)

W, H = VIDEO_WIDTH, VIDEO_HEIGHT

def _font(size, bold=False):
    paths = [
        f"C:/Windows/Fonts/{'arialbd' if bold else 'arial'}.ttf",
        "C:/Windows/Fonts/Impact.ttf",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{'Bold' if bold else 'Regular'}.ttf",
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
    ]
    for p in paths:
        try:    return ImageFont.truetype(p, size)
        except: continue
    return ImageFont.load_default()

def _np(img): return np.array(img)

def to_vertical(landscape_img):
    bg = landscape_img.resize((W, H), Image.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=40))
    bg = ImageEnhance.Brightness(bg).enhance(0.3)
    aspect  = landscape_img.width / landscape_img.height
    sharp_h = int(W / aspect)
    sharp   = landscape_img.resize((W, sharp_h), Image.LANCZOS)
    top     = (H - sharp_h) // 2
    bg.paste(sharp, (0, max(0, top)))
    return bg

def make_intro(title):
    img  = Image.new("RGB", (W, H), (8, 8, 20))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(60, 200), (W-60, 295)], fill=(210, 30, 30))
    draw.text((W//2, 247), "DID YOU KNOW?",
              font=_font(54, True), fill=(255,255,255), anchor="mm")
    tf    = _font(70, True)
    clean = title.replace("#Shorts","").replace("#shorts","").strip()
    words = clean.split(); lines=[]; line=""
    for w in words:
        t = (line+" "+w).strip()
        if draw.textbbox((0,0),t,font=tf)[2] < W-80: line=t
        else:
            if line: lines.append(line)
            line=w
    if line: lines.append(line)
    y = H//2 - len(lines)*85//2
    for l in lines:
        b = draw.textbbox((0,0),l,font=tf)
        x = (W-(b[2]-b[0]))//2
        draw.text((x+3,y+3),l,font=tf,fill=(0,0,0))
        draw.text((x,y),l,font=tf,fill=(255,220,50))
        y += 88
    draw.text((W//2,H-200),"FACTS BELOW ▼",font=_font(38),fill=(70,70,90),anchor="mm")
    return img

def make_fact_frame(landscape_img, fact_num, overlay_text, total_facts=5):
    img  = to_vertical(landscape_img)
    ovl  = Image.new("RGBA",(W,260),(0,0,0,0))
    od   = ImageDraw.Draw(ovl)
    for i in range(260):
        od.rectangle([(0,i),(W,i+1)],fill=(0,0,0,int(210*(1-i/260))))
    img = img.convert("RGBA")
    ovl = ovl.resize(img.size)  # make overlay same size
    img = Image.alpha_composite(img, ovl).convert("RGB")
    bot  = Image.new("RGBA",(W,380),(0,0,0,0))
    bd   = ImageDraw.Draw(bot)
    for i in range(380):
        bd.rectangle([(0,i),(W,i+1)],fill=(0,0,0,int(220*i/380)))
    tmp  = img.convert("RGBA"); tmp.paste(bot,(0,H-380),bot)
    img  = tmp.convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((W//2,90),f"FACT #{fact_num}",font=_font(64,True),fill=(255,220,50),anchor="mm")
    tf   = _font(68,True)
    words= overlay_text.upper().split(); lines=[]; line=""
    for w in words:
        t=(line+" "+w).strip()
        if draw.textbbox((0,0),t,font=tf)[2]<W-70: line=t
        else: lines.append(line); line=w
    if line: lines.append(line)
    y = H-310-len(lines)*80//2
    for l in lines:
        b=draw.textbbox((0,0),l,font=tf); x=(W-(b[2]-b[0]))//2
        draw.text((x+3,y+3),l,font=tf,fill=(0,0,0))
        draw.text((x,y),l,font=tf,fill=(255,255,255))
        y+=82
    dot_r=9; spacing=32; sx=W//2-(total_facts*spacing)//2
    for i in range(total_facts):
        clr=(255,220,50) if i<fact_num else (45,45,65)
        draw.ellipse([(sx+i*spacing-dot_r,H-105),(sx+i*spacing+dot_r,H-87)],fill=clr)
    return img

def make_outro():
    img  = Image.new("RGB",(W,H),(8,8,20))
    draw = ImageDraw.Draw(img)
    draw.text((W//2,H//2-250),"👍 LIKE",       font=_font(92,True),fill=(255,220,50), anchor="mm")
    draw.text((W//2,H//2-110),"💬 COMMENT",    font=_font(92,True),fill=(200,200,255),anchor="mm")
    draw.text((W//2,H//2+ 30),"🔔 FOLLOW",     font=_font(92,True),fill=(210,30,30),  anchor="mm")
    draw.text((W//2,H//2+200),"for daily facts!",font=_font(52),   fill=(100,100,130),anchor="mm")
    return img

def assemble_video(script_data, audio_files, image_paths, output_path=None):
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "final_video.mp4")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clips = []

    ia = AudioFileClip(audio_files["intro"])
    clips.append(ImageClip(_np(make_intro(script_data["title"])),duration=ia.duration).set_audio(ia))

    total = len(script_data["facts"])
    for fact in script_data["facts"]:
        n   = fact["fact_number"]
        aud = AudioFileClip(audio_files[f"fact_{n}"])
        img = Image.open(image_paths[f"fact_{n}"]).convert("RGB")
        frm = make_fact_frame(img, n, fact["overlay_text"], total_facts=total)
        clips.append(ImageClip(_np(frm),duration=aud.duration).set_audio(aud))
        print(f"[Video] Fact {n}/{total} done")

    oa = AudioFileClip(audio_files["outro"])
    clips.append(ImageClip(_np(make_outro()),duration=oa.duration).set_audio(oa))

    final = concatenate_videoclips(clips, method="compose")

    if os.path.exists(BACKGROUND_MUSIC_PATH):
        bgm = AudioFileClip(BACKGROUND_MUSIC_PATH).volumex(BACKGROUND_MUSIC_VOLUME)
        bgm = bgm.loop(duration=final.duration) if bgm.duration < final.duration \
              else bgm.subclip(0, final.duration)
        final = final.set_audio(CompositeAudioClip([final.audio, bgm]))

    final.write_videofile(
        output_path, fps=FPS,
        codec="libx264", audio_codec="aac",
        preset="ultrafast", threads=2, logger=None
    )
    print(f"[Video] Saved: {output_path} ({final.duration:.1f}s)")
    return output_path
