#!/usr/bin/env python3
"""Generate both résumé views from resume.md. Standard library only."""
from pathlib import Path
import re, html, hashlib
ROOT = Path(__file__).resolve().parent
source = (ROOT / 'resume.md').read_text()
def inline(text):
    text = html.escape(re.sub(r'<!--.*?-->', '', text, flags=re.S).strip())
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
def plain(text):
    return re.sub(r'\*', '', text).strip()
def blocks(text):
    result=[]
    for part in re.split(r'\n\s*\n', text.strip()):
        part=part.strip()
        if not part: continue
        if part.startswith('* '): result.append('<ul>'+''.join('<li>'+inline(x.strip()[2:])+'</li>' for x in part.splitlines() if x.strip())+'</ul>')
        else: result.append('<p>'+inline(part).replace('\n','<br>')+'</p>')
    return ''.join(result)
sections = re.split(r'^\*\*([A-Z &]+)\*\*\s*$', source, flags=re.M)
content = dict(zip(sections[1::2], sections[2::2]))
for required in ['PROFESSIONAL SUMMARY','SKILLS & TRAINING','EXPERIENCE','EDUCATION']:
    if required not in content: raise ValueError('Missing résumé section: '+required)
summary = plain(content['PROFESSIONAL SUMMARY'])
experience = content['EXPERIENCE'].strip()
starts = list(re.finditer(r'^\*\*([^*\n]+)\*\*[ \t]+([A-Z][a-z]+ \d{4}[^\n]*)$',experience,re.M))
if not starts: raise ValueError('No employers found. Use **Company** followed by a tab and dates.')
def compact_dates(text):
    months = {'January':'Jan','February':'Feb','March':'Mar','April':'Apr','June':'Jun','July':'Jul','August':'Aug','September':'Sep','October':'Oct','November':'Nov','December':'Dec'}
    for full, short in months.items(): text = re.sub(r'\b'+full+r'\b', short, text)
    return re.sub(r'\s*-\s*', ' – ', text.strip())

def homepage_roles(roles):
    output = []
    for line in roles:
        for entry in line.split('|'):
            match = re.fullmatch(r'(.*?)\s*\(([^()]*)\)\s*', entry.strip())
            title, dates = (match[1].strip(), match[2]) if match else (entry.strip(), '')
            output.append('<div class="position-row"><span class="position-title">'+html.escape(title)+'</span>'+(' <span class="position-dates">'+html.escape(compact_dates(dates))+'</span>' if dates else '')+'</div>')
    return ''.join(output)

articles=[]
current_role=''; current_company=''
for i,match in enumerate(starts):
    company, dates = match.groups()
    body=experience[match.end():starts[i+1].start() if i+1<len(starts) else len(experience)].strip()
    role_match=re.match(r'\*\*\*(.+?)\*\*\*',body)
    role=role_match.group(1) if role_match else ''
    if role_match: body=body[role_match.end():].strip()
    if i==0: current_role=plain(role);current_company=company
    # Every position is visible; descriptions remain exclusive to the full résumé.
    roles = re.findall(r'^\*\*\*(.+?)\*\*\*', experience[match.end():starts[i+1].start() if i+1<len(starts) else len(experience)], re.M)
    role_html = homepage_roles(roles)
    articles.append('<article><div class="time">'+html.escape(compact_dates(dates))+'</div><div><h3>'+inline(company)+'</h3>'+role_html+'</div></article>')
timeline='<div class="timeline">'+''.join(articles)+'</div>'
skills = content['SKILLS & TRAINING'].strip()
training=re.search(r'^\*\*Training:\*\*\s*(.+)$',skills,re.M)
skill_display=re.sub(r'^\*\*Training:\*\*.*$', '',skills,flags=re.M)
education_items = []
for item in re.split(r'\n\s*\n', content['EDUCATION'].strip()):
    match = re.fullmatch(r'\*\*(.*?)\s*-\*\*\s*(.*?)\t(.*)', item.strip())
    if not match: raise ValueError('Education entries need **School -** Degree followed by a tab and date')
    school, degree, date = match.groups()
    education_items.append('<div class="education-item"><h4>'+html.escape(degree)+'</h4><p>'+html.escape(school)+'</p><time>'+html.escape(date)+'</time></div>')
skills_education = '<section class="about-panel skills-panel" aria-labelledby="skills-title"><h3 id="skills-title">Tools of the trade</h3>'+blocks(skill_display)+'</section><section class="about-panel education-panel" aria-labelledby="education-title"><h3 id="education-title">Education</h3>'+''.join(education_items)+'</section>'
values={'SUMMARY':html.escape(summary),'EXPERIENCE':timeline,'CURRENT_ROLE':html.escape(current_role),'CURRENT_COMPANY':html.escape(current_company),'SKILLS_EDUCATION':skills_education,'TRAINING':html.escape(training.group(1) if training else '')}
values['AUTOMATION_METRIC'] = '$500K+' if '$500K' in source else 'Automation'
values['RETENTION_METRIC'] = '$1M+' if '$1MM' in source else 'Reliability'
page=(ROOT/'index.template.html').read_text()
for key,value in values.items(): page=page.replace('{{'+key+'}}',value)
if re.search(r'\{\{\w+\}\}',page):raise ValueError('Unresolved template field')
# Give changed assets a new URL so cached CSS cannot mismatch fresh markup.
for asset in ['styles.css', 'site.js']:
    version = hashlib.sha256((ROOT/asset).read_bytes()).hexdigest()[:12]
    page = page.replace('"'+asset+'"', '"'+asset+'?v='+version+'"')
(ROOT/'index.html').write_text(page)
header=sections[0].strip().split('\n',1)
contact_parts = (header[1] if len(header)>1 else '').strip().split('|')
contact_links = []
for part in contact_parts:
    label = part.strip()
    if not label: continue
    target = 'mailto:'+label if '@' in label else 'https://'+label
    contact_links.append('<a href="'+html.escape(target, quote=True)+'">'+html.escape(label)+'</a>')
contact_html = ' <span aria-hidden="true"> | </span> '.join(contact_links)
from render_resume import render
(ROOT/'resume.html').write_text(render(source, inline, contact_html))
print('Generated index.html and resume.html from resume.md')
