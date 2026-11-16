# Agent instructions — Anthony Rodriguez portfolio

## Single editing entry point
This repository is the ONLY working source for résumé and website. Edit resume.md here, never Dropbox. Do not add Dropbox sync, copies, scheduled jobs, or another editable master. User will save PDFs from the website manually. Dropbox Current was verified on Nov 15, 2026: its Nov 13 Markdown matched the original local source; its HTML layout is the formatting reference.

## Update workflow
Read README. Edit resume.md, run `python3 build.py`, preview locally, report changes. `python3 dev.py` optionally watches source files and regenerates on save. It does not publish. Preserve Markdown section headings, employer/tab/date format, and role lines. Do not edit generated index.html or resume.html directly.

Both homepage and printable résumé derive from resume.md. Homepage roles show company, title, and dates ONLY—no summaries, bullet lists, or environment details. All employers and roles are visible; do not hide earlier experience. Full résumé keeps all details. No Key Accomplishments label. No homepage highlight markers needed.

Layout: index.template.html. Website style/behavior: styles.css, site.js. Featured apps: projects.json. Print renderer: render_resume.py, resume.css. Print layout follows Dropbox Current: centered name/contact, blue section headings, compact spacing, company/title and aligned dates, two pages with AI Squared starting page two. Recheck overflow after content changes; allow layout adjustments rather than clipping content.

## User constraints
- Feature Local AI Chat (arod7533/GradioChatBot) first, then Old Man United. User rejected Task Manager. Chatbot is now built; use the recorded demo, not a public live inference endpoint. Media in assets/chatbot comes from GradioChatBot commit aa9a01e556233da488ff3b4361a0076b261e1388. Do not autoplay or invent a hosted demo link.
- No invented credentials, claims, metrics, dates, or features. Project features were checked against README, not independently tested.
- Include clickable anthonyarodriguez.com with email, LinkedIn and GitHub at top of résumé. Phone omitted from public view.
- Consistent midnight/slate, white, cobalt surfaces; no abrupt color transitions, green/tan sections, or orbital AR logo. Name wordmark. Subtle motion with reduced-motion support.
- Dates need inset padding inside experience rows.
- No claim that career began in 2016; use SOFTWARE · DATA · SYSTEMS.

## Review and publishing
Preview: `python3 -m http.server 4173 --bind 127.0.0.1`. Reuse existing server. Check affected layout at desktop/mobile, links, résumé print page, disclosure, source/output consistency. For copy edits, direct output checks suffice. No dependencies needed.

The user approved the preview and authorized public repository creation, initial push, and GitHub Pages activation on November 15, 2026. DNS changes still require approval. Future pushes should follow the user’s request for the current task. Intended visibility PUBLIC, hosting GitHub Pages free. Include source and generated files in commits. GitHub CLI auth previously invalid: recheck. Domain anthonyarodriguez.com plus www; Squarespace registrar used custom nameservers, so identify authoritative DNS before changes. Preserve email and unrelated DNS. No paid APIs, backend inference, trackers, secrets, or .env files.

Experience layout: compact rows, 170px date column on desktop, abbreviated sans-serif dates without letter spacing. Split promotions into one position per line; role dates are smaller muted text, titles blue. Preserve all roles.
