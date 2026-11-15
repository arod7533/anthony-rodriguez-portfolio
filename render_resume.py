"""Render the original Dropbox résumé layout from the repository's Markdown."""
import re, html
from pathlib import Path

def render(source, inline, contact_html):
    parts = re.split(r'\n\s*\n|\n(?=\*\*\*)', source.strip())
    pages = [[], []]; page = 0; section = ''; skip = set()
    for i, part in enumerate(parts):
        part = part.strip()
        if i in skip or not part or part == '**Key Accomplishments:**': continue
        if part.startswith('**AI Squared**'): page = 1
        if i == 0: out = '<h1>'+inline(part)+'</h1>'
        elif i == 1: out = '<div class="contact">'+contact_html+'</div>'
        elif re.fullmatch(r'\*\*[A-Z &]+\*\*',part):
            section = part; out = '<h2>'+inline(part)+'</h2>'
        elif part.startswith('* '): out = '<div class="bullet"><span>•</span><div>'+inline(part[2:])+'</div></div>'
        elif '\t' in part and section == '**EXPERIENCE**':
            company, dates = part.split('\t',1)
            if company.startswith('**Optum'):
                out = '<header class="job"><div>'+inline(company)+'</div><time>'+inline(dates)+'</time></header>'
            else:
                role = parts[i+1].strip().replace('*',''); skip.add(i+1)
                title = re.sub(r'\s*\([^)]*\)\s*$','',role.split('|')[0]).strip()
                out = '<header class="job"><div>'+inline(company)+' - '+html.escape(title)+'</div><time>'+inline(dates)+'</time></header>'
        elif part.startswith('***'):
            role = part.replace('*',''); match = re.fullmatch(r'(.*?)\s*\(([^)]*)\)',role)
            if match: out='<div class="position"><span>'+html.escape(match[1].strip())+'</span><time>'+html.escape(match[2])+'</time></div>'
            else: out='<p class="detail">'+html.escape(role)+'</p>'
        else:
            kind = 'detail' if section == '**EXPERIENCE**' else 'skill' if section == '**SKILLS & TRAINING**' else 'body'
            if kind=='detail' and part.startswith('*') and part.endswith('*') and not part.startswith('**'):part=part[1:-1]
            if section=='**EDUCATION**': part=part.replace('\t',' | ')
            out='<p class="'+kind+'">'+inline(part)+'</p>'
        pages[page].append(out)
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anthony A. Rodriguez — Résumé</title><link rel="stylesheet" href="resume.css"></head><body><nav class="toolbar"><a href="index.html">← Portfolio</a><button onclick="window.print()">Print / save as PDF</button></nav><main class="pages">'''+''.join('<article class="page">'+''.join(p)+'</article>' for p in pages)+'''</main><script>function fit(){document.querySelectorAll('.page').forEach(p=>p.style.zoom=Math.min(1,(innerWidth-24)/816))}addEventListener('resize',fit);fit();addEventListener('beforeprint',()=>document.querySelectorAll('.page').forEach(p=>p.style.zoom=1));addEventListener('afterprint',fit);</script></body></html>'''
