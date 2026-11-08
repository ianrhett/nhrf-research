import sys
# usage: segment.py transcript.txt video_id start(HH:MM:SS) end(HH:MM:SS) title out.txt
src, vid, start, end, title, dst = sys.argv[1:7]
def sec(t): h, m, s = map(int, t.split(":")); return h*3600+m*60+s
a, b = sec(start), sec(end)
lines = [l for l in open(src, encoding="utf-8") if l[:8].count(":") == 2 and a <= sec(l[:8]) <= b]
hdr = (f"{title}\nSOURCE: YouTube AUTO-CAPTIONS (machine-generated, unverified; not a quotation source)\n"
       f"Video: https://www.youtube.com/watch?v={vid}\nSegment: {start} - {end}\n"
       f"Start link: https://www.youtube.com/watch?v={vid}&t={a}s\n\n")
open(dst, "w", encoding="utf-8").write(hdr + "".join(lines))
print(dst, len(lines), a)
