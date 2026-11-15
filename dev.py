#!/usr/bin/env python3
"""Rebuild local résumé views on save; never commit, push, or sync externally."""
from pathlib import Path
import subprocess,sys,time
root=Path(__file__).resolve().parent
files=['resume.md','build.py','render_resume.py','index.template.html']
previous=None
print('Watching résumé sources. Preview: http://127.0.0.1:4173 (start a local HTTP server separately). Ctrl-C stops.')
try:
    while True:
        signature=tuple((root/name).stat().st_mtime_ns for name in files)
        if signature!=previous:
            result=subprocess.run([sys.executable,str(root/'build.py')],cwd=root)
            previous=signature
            if result.returncode:print('Build failed. Fix the source and save again.',file=sys.stderr)
        time.sleep(0.5)
except KeyboardInterrupt:pass
