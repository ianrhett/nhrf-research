"""Cut a versioned release of the workbook.

Usage: python3 release_workbook.py <commitments_dir> <version> "<one-line summary>"

NHRF_Commitments.xlsx stays the working copy that the add scripts edit. A release:
  1. writes <version> and today's date to commitments/VERSION (the About tab shows it),
  2. reruns cover_sheet.py so the About tab carries the version and current counts,
  3. copies the workbook to commitments/versions/NHRF_Commitments_v<version>_<date>.xlsx,
  4. appends an entry to commitments/CHANGELOG.md with the summary and key counts.
Share the file in versions/, never the working copy. Refuses to overwrite an existing version.
"""
import datetime, os, shutil, subprocess, sys
import openpyxl

CDIR, VERSION, SUMMARY = sys.argv[1:4]
VERSION = VERSION.lstrip('v')
today = datetime.date.today().isoformat()
work = f'{CDIR}/NHRF_Commitments.xlsx'
os.makedirs(f'{CDIR}/versions', exist_ok=True)
out = f'{CDIR}/versions/NHRF_Commitments_v{VERSION}_{today}.xlsx'
if any(f.startswith(f'NHRF_Commitments_v{VERSION}_') for f in os.listdir(f'{CDIR}/versions')):
    sys.exit(f'version {VERSION} already released')

with open(f'{CDIR}/VERSION', 'w', encoding='utf-8') as f:
    f.write(f'{VERSION} {today}\n')
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, '-I', f'{here}/cover_sheet.py', work], check=True)
shutil.copyfile(work, out)

wb = openpyxl.load_workbook(out, read_only=True)
about = {r[0]: r[1] for r in wb['About'].iter_rows(values_only=True) if r[0] and isinstance(r[1], int)}
counts = ', '.join(f'{k}: {v}' for k, v in about.items())
log = f'{CDIR}/CHANGELOG.md'
head = '' if os.path.exists(log) else '# Workbook changelog\n\nEach release is a dated copy in `versions/`. Newest first.\n'
old = open(log, encoding='utf-8').read() if os.path.exists(log) else head
lines = old.split('\n')
insert = 4 if old.startswith('# Workbook changelog') else 0
entry = [f'## v{VERSION} ({today})', '', SUMMARY, '', f'`versions/{os.path.basename(out)}`. {counts}.', '']
with open(log, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines[:insert] + entry + lines[insert:]))
print('released', out)
