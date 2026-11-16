const container = document.querySelector('#project-list');
const el = (tag, text, className) => {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
};
async function loadProjects() {
  try {
    const response = await fetch('projects.json', { cache: 'no-cache' });
    if (!response.ok) throw new Error('Projects unavailable');
    const projects = await response.json();
    container.replaceChildren();
    for (const project of projects) {
      const article = el('article', '', 'project');
      let art;
      if (project.video) {
        art = el('figure', '', 'project-video');
        const video = el('video');
        video.controls = true;
        video.preload = 'none';
        video.playsInline = true;
        video.poster = project.poster;
        video.setAttribute('aria-label', project.title + ' recorded demonstration');
        const source = el('source');
        source.src = project.video;
        source.type = 'video/mp4';
        video.append(source, document.createTextNode('Your browser does not support embedded video.'));
        const caption = el('figcaption', project.videoCaption || 'Recorded demo · Play to watch');
        art.append(video, caption);
      } else {
      art = el('div', '', 'project-art football-art');
      art.setAttribute('aria-hidden', 'true');
      art.innerHTML = '<div class="pitch"><div class="pitch-circle"></div><div class="pitch-box box-top"></div><div class="pitch-box box-bottom"></div><span class="pitch-name">OLD MAN<br>UNITED<span>THE SEASON. AT A GLANCE.</span></span><div class="pitch-badge">OMU<span>EST. ON THE PITCH</span></div></div><span class="art-caption">TEAM STATS / A LIVING DASHBOARD</span>';
      }
      const info = el('div', '', 'project-info');
      info.append(el('span', project.label, 'eyebrow'), el('h3', project.title), el('p', project.description), el('p', project.details));
      const tags = el('div', '', 'tags');
      for (const tag of project.tags) tags.append(el('span', tag));
      info.append(tags);
      const links = el('div', '', 'actions');
      for (const [label, url, className] of [['Visit live site ↗', project.liveUrl, 'button'], ['View source ↗', project.sourceUrl, 'text-link']]) {
        if (!url) continue;
        const parsed = new URL(url);
        if (parsed.protocol !== 'https:') continue;
        const link = el('a', label, className); link.href = parsed.href; links.append(link);
      }
      info.append(links); article.append(art, info); container.append(article);
    }
  } catch {
    container.replaceChildren(el('p', 'Explore my projects on GitHub.'));
    const link = el('a', 'github.com/arod7533 ↗', 'text-link');
    link.href = 'https://github.com/arod7533'; container.append(link);
  }
}
loadProjects();
document.getElementById('year').textContent = new Date().getFullYear();
const motionAllowed = !matchMedia('(prefers-reduced-motion: reduce)').matches;
if (motionAllowed && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in-view'); observer.unobserve(entry.target); } });
  }, { threshold: 0.08 });
  document.querySelectorAll('.section-heading, .timeline article, .impact, .about-right').forEach(node => { node.classList.add('reveal'); observer.observe(node); });
}
