import os
import re

def find_highlights():
    transcript_file = "audio.txt"

    if not os.path.exists(transcript_file):
        return [0]

    with open(transcript_file, "r", encoding="utf-8") as f:
        text = f.read()

    lines = re.split(r"[.!?\n]", text)

    keywords = [
        "allah", "rasool", "mohabbat",
        "gunah", "dua", "jannat",
        "akhirat", "imaan"
    ]

    highlights = []

    for i, line in enumerate(lines):
        if any(k in line.lower() for k in keywords):
            highlights.append(i * 3)

    if not highlights:
        highlights = [0]

    return highlights[:4]

def render_short(start_time, index):
    duration = 40

    if start_time < 30:
        duration = 50
    elif start_time > 120:
        duration = 30

    cmd = (
        f'ffmpeg -y -ss {start_time} -i input.mp4 '
        f'-t {duration} '
        '-vf "scale=720:1280,'
        'drawbox=x=0:y=0:w=720:h=1280:color=black@0.3:t=fill,'
        'subtitles=audio.srt:force_style=\'Fontsize=20,PrimaryColour=&Hffffff&,OutlineColour=&H000000&,BorderStyle=1,Outline=2\','
        'drawtext=text=\'YT / GulameAqib\':x=20:y=40:fontsize=24:fontcolor=white" '
        '-c:v libx264 -preset slow -crf 22 '
        f'-c:a aac exports/short_{index}.mp4'
    )

    os.system(cmd)

def process(link):
    os.makedirs("exports", exist_ok=True)

    print("Downloading video...")
    os.system(f'yt-dlp "{link}" -o input.mp4')

    print("Extracting audio...")
    os.system('ffmpeg -y -i input.mp4 audio.mp3')

    print("Transcribing...")
    os.system('whisper audio.mp3 --model base')

    highlights = find_highlights()

    print(f"Found {len(highlights)} highlights")

    for i, start in enumerate(highlights):
        print(f"Rendering short {i+1}...")
        render_short(start, i)

    print("All shorts created.")
