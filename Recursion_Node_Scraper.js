(async function exportChatGPT() {
  // 1) Derive labels from the tab title
  const fullTitleRaw = document.title.replace(/\s+[-–]\s*ChatGPT$/, '').trim();
  const [ASSISTANT_LABEL] = fullTitleRaw.split(/\s*[-–]\s*/);
  const SESSION_TITLE = fullTitleRaw;
  const USER_LABEL = 'Glen Allan';

  // 2) HTML scaffold with dark-mode & CSS
  const HTML_HEADER = `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
  <title>${SESSION_TITLE}</title>
  <style>
    body { background:#121212; color:#eee; font-family:sans-serif; padding:20px; line-height:1.5; }
    h1 { color:#fff; }
    .message { margin-bottom:1.5em; }
    .message pre { margin-left:2em; }       /* indent code blocks */
    .message.user::before {
      content: "${USER_LABEL} says:"; display:block; font-weight:bold; margin-bottom:0.3em;
    }
    .message.assistant::before {
      content: "${ASSISTANT_LABEL} says:"; display:block; font-weight:bold; margin-bottom:0.3em;
    }
    pre {
      font-family:monospace; padding:10px; border-radius:6px;
      overflow-x:auto; background:rgba(255,255,255,0.05);
    }
    code {
      font-family:monospace; padding:2px 4px; border-radius:4px;
      background:rgba(255,255,255,0.1);
    }
    /* Syntax highlighting */
    .hljs-comment    { color:#6A9955; }
    .hljs-built_in   { color:#569CD6; }
    .hljs-keyword    { color:#C586C0; }
    .hljs-string     { color:#CE9178; }
    .hljs-title,
    .hljs-function   { color:#DCDCAA; }
    .hljs-number     { color:#B5CEA8; }
    [data-type="rich"] { color:#ccc; }

    img { max-width:100%; display:block; margin:0.5em 0; }
    /* Generated images: rounded + viewport-limited */
    .message.assistant[data-type="image"] img {
      border-radius:8px;
      max-width:33vw;
      height:auto;
    }
  </style>
</head><body>
  <h1>Conversation: ${SESSION_TITLE}</h1>
`;
  const HTML_FOOTER = `</body></html>`;

  // 3) Normalize & inline all images

  document.querySelectorAll('canvas').forEach(c => {
    try {
      const img = document.createElement('img');
      img.src = c.toDataURL();
      c.replaceWith(img);
    } catch(e) {
      console.warn('canvas→img failed', e);
    }
  });

  document.querySelectorAll('div[role="img"]').forEach(div => {
    const bg = getComputedStyle(div).backgroundImage;
    const url = bg.slice(5, -2);
    const img = document.createElement('img');
    img.src = url;
    img.alt = div.getAttribute('aria-label') || '';
    div.replaceWith(img);
  });

  document.querySelectorAll('picture').forEach(pic => {
    const img = pic.querySelector('img');
    if (img) pic.replaceWith(img.cloneNode());
  });

  const imgs = Array.from(document.querySelectorAll('img'));
  await Promise.all(imgs.map(img => {
    if (img.src.startsWith('data:')) return;
    return fetch(img.src)
      .then(r => r.blob())
      .then(blob => new Promise(res => {
        const fr = new FileReader();
        fr.onloadend = () => { img.src = fr.result; res(); };
        fr.readAsDataURL(blob);
      }))
      .catch(e => console.warn('inline failed for', img.src, e));
  }));

  // 4) Remove non-functional Copy/Edit buttons
  document.querySelectorAll('pre button').forEach(btn => btn.remove());

  // 5) Collect chat bubbles + unique generated images in order
  const nodes = document.querySelectorAll(
    '[data-message-author-role], img[alt="Generated image"]'
  );
  const seen = new Set(), items = [];
  nodes.forEach(el => {
    if (el.tagName === 'IMG' && el.alt === 'Generated image') {
      if (!seen.has(el.src)) {
        seen.add(el.src);
        items.push(el);
      }
    } else {
      items.push(el);
    }
  });

  // 6) Build HTML with extra <br> between items
  let out = HTML_HEADER;
  items.forEach(el => {
    if (el.matches('[data-message-author-role]')) {
      const role    = el.getAttribute('data-message-author-role');
      const content = el.innerHTML;
      const isRich  = /<(h\d|ul|ol|table|blockquote|strong)>/.test(content);
      out += `<div class="message ${role}" data-type="${isRich?'rich':'plain'}">${content}</div><br><br>\n`;
    } else {
      out += `<div class="message assistant" data-type="image">${el.outerHTML}</div><br><br>\n`;
    }
  });
  out += HTML_FOOTER;

  // 7) Trigger download
  const blob = new Blob([out], { type: 'text/html' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `${SESSION_TITLE.replace(/\s+/g,'_')}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  console.log(`✅ Exported ${items.length} items as “${a.download}” with extra spacing.`);
})();