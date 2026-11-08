import sys, re
# Convert YouTube auto-caption VTT to deduplicated "HH:MM:SS text" lines.
src, dst = sys.argv[1], sys.argv[2]
out, last = [], None
ts = None
for line in open(src, encoding="utf-8"):
    line = line.rstrip("\n")
    m = re.match(r"(\d\d:\d\d:\d\d)\.\d+ -->", line)
    if m:
        ts = m.group(1); continue
    if not line.strip() or line.startswith(("WEBVTT", "Kind:", "Language:")) or "<c>" in line or "align:" in line:
        continue
    t = re.sub(r"<[^>]+>", "", line).strip()
    if t and t != last:
        out.append(f"{ts} {t}"); last = t
open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
