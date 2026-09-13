"""
add_voiceover.py
================
Step 2 of 2 — Merges per-slide voiceover MP3 segments with the
exported portfolio video (Yogesh_Raje_Portfolio_Video_Ready.mp4)
using ffmpeg to produce the final voiced video.

Each slide's audio segment is:
  - Padded with silence to match the exact slide duration
  - Concatenated in order to form a 150-second audio track
  - Mixed into the original video (which has no audio)

Prerequisites:
  - ffmpeg installed and on PATH
  - voiceover_script.py already run (voiceover_segments/ folder exists)
  - Yogesh_Raje_Portfolio_Video_Ready.mp4 exists

Run:  python add_voiceover.py
"""

import os, subprocess, sys, json

# ── Configuration ─────────────────────────────────────────────────────────
VIDEO_IN   = "Yogesh_Raje_Portfolio_Video_Ready.mp4"
AUDIO_DIR  = "voiceover_segments"
VIDEO_OUT  = "Yogesh_Raje_Portfolio_With_Voiceover.mp4"
TEMP_DIR   = "voiceover_temp"

# Slide durations in seconds — must match the PPTX timings
DURATIONS  = [10, 6, 8, 9, 9, 9, 10, 9, 9, 10, 8, 10, 10, 9, 9, 8, 7]
NUM_SLIDES = len(DURATIONS)
TOTAL_SECS = sum(DURATIONS)

os.makedirs(TEMP_DIR, exist_ok=True)

def run(cmd: list, desc: str = ""):
    """Run an ffmpeg command, raise on failure."""
    print(f"  [{desc}] " + " ".join(str(c) for c in cmd[:6]) + " ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] {result.stderr[-500:]}")
        sys.exit(1)
    return result

def ffmpeg(*args):
    """Build ffmpeg command with -y (overwrite) and -loglevel warning."""
    exe = "ffmpeg"
    return [exe, "-y", "-loglevel", "warning"] + list(args)

# ── Step 1: Verify inputs ──────────────────────────────────────────────────
print("=" * 60)
print("  Yogesh Raje Portfolio — Adding Voiceover")
print("=" * 60)
print()

if not os.path.exists(VIDEO_IN):
    print(f"[ERROR] Video not found: {VIDEO_IN}")
    print("  Export it from PowerPoint first:")
    print("  File > Export > Create a Video > Use Recorded Timings")
    sys.exit(1)

missing = []
for i in range(1, NUM_SLIDES + 1):
    seg = os.path.join(AUDIO_DIR, f"slide_{i:02d}.mp3")
    if not os.path.exists(seg):
        missing.append(seg)

if missing:
    print(f"[ERROR] Missing {len(missing)} audio segments.")
    print("  Run:  python voiceover_script.py  first.")
    sys.exit(1)

print(f"[OK] Video:  {VIDEO_IN}  ({os.path.getsize(VIDEO_IN):,} bytes)")
print(f"[OK] Audio segments: {NUM_SLIDES} files in '{AUDIO_DIR}/'")
print(f"[OK] Total duration: {TOTAL_SECS}s")
print()

# ── Step 2: Get exact TTS duration of each segment ────────────────────────
def get_duration(path: str) -> float:
    """Return audio duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])

print("Step 1/4: Measuring TTS segment durations...")
tts_durations = {}
for i in range(1, NUM_SLIDES + 1):
    seg = os.path.join(AUDIO_DIR, f"slide_{i:02d}.mp3")
    dur = get_duration(seg)
    tts_durations[i] = dur
    slide_dur = DURATIONS[i - 1]
    pad = max(0.0, slide_dur - dur)
    status = "fits" if dur <= slide_dur else f"OVER by {dur - slide_dur:.1f}s"
    print(f"  Slide {i:02d}: TTS={dur:.2f}s  slide={slide_dur}s  pad={pad:.2f}s  [{status}]")
print()

# ── Step 3: Pad each audio segment to exact slide duration ────────────────
print("Step 2/4: Padding each segment to exact slide duration...")
padded_files = []
for i in range(1, NUM_SLIDES + 1):
    seg      = os.path.join(AUDIO_DIR, f"slide_{i:02d}.mp3")
    padded   = os.path.join(TEMP_DIR, f"padded_{i:02d}.wav")
    tts_dur  = tts_durations[i]
    slide_dur= DURATIONS[i - 1]
    pad_sec  = max(0.0, slide_dur - tts_dur)

    if pad_sec < 0.1:
        # Trim to fit if TTS is longer than slide (truncate last 0.1s gracefully)
        trim_to = slide_dur - 0.05
        run(ffmpeg(
            "-i", seg,
            "-af", f"atrim=end={trim_to:.3f},apad=pad_dur=0.05",
            "-ar", "44100", "-ac", "1",
            "-t", str(slide_dur),
            padded
        ), f"trim+pad slide {i:02d}")
    else:
        # Add silence padding at end so segment = exact slide duration
        run(ffmpeg(
            "-i", seg,
            "-af", f"apad=pad_dur={pad_sec:.3f}",
            "-ar", "44100", "-ac", "1",
            "-t", str(slide_dur),
            padded
        ), f"pad slide {i:02d}")

    padded_files.append(padded)
    print(f"  Slide {i:02d}: padded to {slide_dur}s  -> {os.path.basename(padded)}")

print()

# ── Step 4: Concatenate all padded segments into one 150s audio track ─────
print("Step 3/4: Concatenating all segments into 150s audio track...")
concat_list = os.path.join(TEMP_DIR, "concat_list.txt")
with open(concat_list, "w") as f:
    for p in padded_files:
        abs_path = os.path.abspath(p).replace("\\", "/")
        f.write(f"file '{abs_path}'\n")

final_audio = os.path.join(TEMP_DIR, "voiceover_full.wav")
run(ffmpeg(
    "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-ar", "44100", "-ac", "1",
    final_audio
), "concat audio")

# Verify final audio length
final_dur = get_duration(final_audio)
print(f"  Final audio duration: {final_dur:.2f}s  (target: {TOTAL_SECS}s)")
print()

# ── Step 5: Merge voiceover with the video ────────────────────────────────
print("Step 4/4: Merging voiceover into video...")
run(ffmpeg(
    "-i", VIDEO_IN,
    "-i", final_audio,
    "-c:v", "copy",            # copy video stream unchanged
    "-c:a", "aac",             # encode audio as AAC for MP4
    "-b:a", "192k",
    "-map", "0:v:0",           # video from input 0
    "-map", "1:a:0",           # audio from input 1 (our voiceover)
    "-shortest",               # end when shorter stream ends
    VIDEO_OUT
), "merge video+audio")

out_size = os.path.getsize(VIDEO_OUT)
print()
print("=" * 60)
print(f"  [DONE] Output: {VIDEO_OUT}")
print(f"         Size:   {out_size / 1_000_000:.1f} MB")
print(f"         Duration: ~{TOTAL_SECS}s (2 min 30 sec)")
print(f"         Voice:  Microsoft Aria (en-US Neural)")
print(f"         Slides: {NUM_SLIDES} x auto-advance")
print("=" * 60)

# ── Cleanup temp files ────────────────────────────────────────────────────
import shutil
shutil.rmtree(TEMP_DIR, ignore_errors=True)
print(f"\n[OK] Temp files cleaned up.")
print(f"[OK] Open: {VIDEO_OUT}")
