#!/usr/bin/env python3
"""Build the Stomp, Tiptoe, Wiggle Zoo video from 5 stills + song.mp3 with ffmpeg."""
import os, subprocess, sys

D = sys.argv[1]  # working dir with images + song.mp3
OUT = sys.argv[2]
FPS, W, H = 30, 1920, 1080
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
IMG = {
    "bush": "db4ded95-b182-49aa-91be-7a49f03b5b14.jpeg",
    "ele": "d7a6e489-c258-4467-ab91-a2258aa65ec7.jpeg",
    "mouse": "f97f4cdf-640a-4ac3-abdf-ad770381b5d8.jpeg",
    "snake": "90adb7f7-4d93-4d34-94b3-200a0fdcd5fe.jpeg",
    "all": "02a7ce54-85c7-4172-b834-6f192b509ceb.jpeg",
}
SEG = os.path.join(D, "seg"); os.makedirs(SEG, exist_ok=True)

def seg(i, img, dur, motion):
    """motion: zin, zout, panl, panr, shake, still"""
    n = max(1, round(dur * FPS))
    src = os.path.join(D, IMG[img])
    if motion == "still":
        vf = f"scale={W}:{H}"
    elif motion == "shake":
        # bush shaking: small horizontal jitter on a slightly zoomed frame
        vf = (f"scale=2112:1188,crop={W}:{H}:'96+40*sin(n*0.9)':'54+12*sin(n*1.7)'")
    else:
        z = {"zin": f"1+0.15*on/{n}", "zout": f"1.15-0.15*on/{n}",
             "panl": "1.12", "panr": "1.12"}[motion]
        x = {"panl": f"(iw-iw/zoom)*(1-on/{n})", "panr": f"(iw-iw/zoom)*on/{n}"}.get(
            motion, "iw/2-(iw/zoom/2)")
        vf = (f"scale=3840:-1,zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':"
              f"d={n}:s={W}x{H}:fps={FPS}")
    out = os.path.join(SEG, f"{i:03d}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-vf",
                    vf + ",format=yuv420p", "-frames:v", str(n), "-r", str(FPS),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out], check=True)
    return out

# ---- timeline (seconds) ----
plan = [("bush", 9, "shake"), ("bush", 7, "zin")]                       # 0-16 hook + turn
plan += [("ele", 6.5, "zin"), ("ele", 6, "panr"), ("ele", 6.5, "zout")]  # 16-35
plan += [("mouse", 6.5, "panl"), ("mouse", 6, "zin"), ("mouse", 6.5, "panr")]  # 35-54
plan += [("snake", 6.5, "panr"), ("snake", 6, "zout"), ("snake", 6.5, "panl")]  # 54-73
plan += [("all", 4.5, "zin"), ("all", 4.5, "zout")]                      # 73-82 chorus
plan += [("bush", 8, "shake")]                                           # 82-90 faster!
r2 = ["ele", "mouse", "snake"]
plan += [(r2[k % 3], 2, ["zin", "zout"][k % 2]) for k in range(9)]       # 90-108 round 2
plan += [("all", 4.5, "zin"), ("all", 4.5, "zout")]                      # 108-117 chorus
plan += [(r2[k % 3], 1, ["zin", "zout"][k % 2]) for k in range(19)]      # 117-136 round 3
plan += [("all", 14.2, "still")]                                         # 136-150.2 FREEZE

files, t = [], 0.0
for i, (img, dur, m) in enumerate(plan):
    files.append(seg(i, img, dur, m)); t += dur
lst = os.path.join(D, "list.txt")
open(lst, "w").write("".join(f"file '{f}'\n" for f in files))

# ---- text overlays ----
def txt(s, a, b, size=120, y="h*0.72", color="white"):
    s = s.replace("'", "’").replace(":", "\\:")
    return (f"drawtext=fontfile={FONT}:text='{s}':fontsize={size}:fontcolor={color}:"
            f"borderw=10:bordercolor=0x1a1a1a:x=(w-text_w)/2:y={y}:"
            f"enable='between(t,{a},{b})'")

def counter(s, a, b):
    s = s.replace(":", "\\:")
    return (f"drawtext=fontfile={FONT}:text='{s}':fontsize=54:fontcolor=white:"
            f"borderw=6:bordercolor=0x1a1a1a:box=1:boxcolor=0xff8c00@0.85:boxborderw=18:"
            f"x=w-text_w-60:y=50:enable='between(t,{a},{b})'")

ov = [
    txt("WHO’S STOMPING?", 1.5, 8.5, 130, "h*0.08"),
    txt("STAND UP!", 11, 16, 150),
    counter("ANIMALS FOUND: 0/3", 1.5, 16),
    counter("ANIMALS FOUND: 1/3", 16, 35),
    counter("ANIMALS FOUND: 2/3", 35, 54),
    counter("ANIMALS FOUND: 3/3", 54, 136),
    txt("STOMP!", 18, 34, 140),
    txt("TIPTOE… shhh", 37, 53, 120, color="0xfff3b0"),
    txt("WIGGLE!", 56, 72, 140, color="0xc8ff6a"),
    txt("STOMP! TIPTOE! WIGGLE!", 73, 82, 104),
    txt("FASTER!", 83, 90, 170, "(h-text_h)/2", "0xffe14d"),
    txt("STOMP! TIPTOE! WIGGLE!", 108, 117, 104),
    txt("SUPER FAST!", 117, 121, 150, "h*0.08", "0xff5a5a"),
    txt("FREEZE!", 136, 141.5, 220, "(h-text_h)/2", "0x7fdcff"),
    txt("YOU FOUND ALL 3!", 141.5, 146, 130, "h*0.72", "0xffe14d"),
    txt("PLAY AGAIN?", 146, 150.2, 140, "h*0.72"),
]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                "-i", os.path.join(D, "song.mp3"), "-vf", ",".join(ov),
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT],
               check=True)
print("built", OUT, "timeline", round(t, 2), "s")
