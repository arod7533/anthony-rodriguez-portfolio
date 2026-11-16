# Anthony Rodriguez — résumé and website

This repository is the sole editing entry point. Dropbox was used once to verify the original content and layout; it is not a source to edit or sync going forward.

## Daily workflow

1. Open this folder as your Codex project.
2. Edit `resume.md`, or ask an agent to update it.
3. Run `python3 build.py` to regenerate the website and printable résumé.
4. Preview with `python3 -m http.server 4173 --bind 127.0.0.1`, then visit http://127.0.0.1:4173.
5. Review, then commit and push the approved source and generated files. Once GitHub Pages is configured, pushing updates the public site.

For automatic regeneration while editing, run `python3 dev.py` in a second terminal. Saving resume.md updates both generated views; refresh the browser to see them. This never pushes or publishes.

Save a PDF manually using the résumé page's Print / save as PDF button. Dropbox is untouched. Saved PDFs are snapshots.

## Files

- `resume.md`: sole source of résumé content.
- `index.template.html`: website layout; experience shows company, title, dates only; all experience visible.
- `projects.json`: featured project data; Local AI Chat first, then Old Man United.
- `styles.css` / `site.js`: website styling and behavior.
- `render_resume.py` / `resume.css`: printable layout modeled on Dropbox Current.
- `build.py`: generates `index.html` and `resume.html`; do not edit generated files.
- `AGENTS.md`: instructions for future agents.

Suggested prompt: “Read AGENTS.md. Update resume.md with [changes], regenerate, and preview. Do not push yet.”

No dependencies, APIs, model charges, Dropbox synchronization, or automatic publishing. Public repository and GitHub Pages publication were approved on November 15, 2026. Domain DNS is configured separately.

Chatbot demo media: assets/chatbot, copied from arod7533/GradioChatBot commit aa9a01e556233da488ff3b4361a0076b261e1388 (owner arod7533). Video playback is static; no model inference is hosted or called.
