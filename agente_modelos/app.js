/*
 * app.js — WebForge
 *
 * Generador de HTML y CSS a partir de descripciones en lenguaje natural.
 * Extiende el ciclo base de Ollama con extracción de bloques de código,
 * preview en iframe y descarga de archivos.
 */

const SEL = id => document.getElementById(id);

const dom = {
  messages:      SEL('messages'),
  form:          SEL('compose-form'),
  input:         SEL('input-box'),
  sendBtn:       SEL('send-btn'),
  modelSelect:   SEL('model-select'),
  endpointInput: SEL('endpoint-input'),
  tempSlider:    SEL('temp-slider'),
  tempVal:       SEL('temp-val'),
  systemPrompt:  SEL('system-prompt'),
  statusDot:     SEL('status-dot'),
  statusText:    SEL('status-text'),
  checkBtn:      SEL('check-btn'),
  clearBtn:      SEL('clear-btn'),
  exportBtn:     SEL('export-btn'),
  downloadBtn:   SEL('download-btn'),
  previewBtn:    SEL('preview-btn'),
  previewModal:  SEL('preview-modal'),
  previewClose:  SEL('preview-close'),
  previewFrame:  SEL('preview-frame'),
  tokenCounter:  SEL('token-counter'),
  skillsDrop:    SEL('skills-drop'),
  skillsInput:   SEL('skills-input'),
  skillsList:    SEL('skills-list'),
};

// Estado global de la sesión
let state = {
  history:     [],
  streaming:   false,
  totalTokens: 0,
  skills:      {},
  // Último HTML y CSS generado por el modelo (para preview y descarga)
  lastHtml:    '',
  lastCss:     '',
};


//  Utilidades DOM 

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Convierte Markdown a HTML con soporte para bloques de código con lenguaje
function renderMarkdown(raw) {
  let out = escapeHtml(raw);

  out = out.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
    const tag = lang
      ? `<span style="font-size:10px;color:var(--text-2);letter-spacing:.06em">${lang}</span>\n`
      : '';
    return `<pre>${tag}<code>${code.trimEnd()}</code></pre>`;
  });

  out = out.replace(/`([^`\n]+)`/g, '<code>$1</code>');
  out = out.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  return out;
}

function scrollBottom() {
  dom.messages.scrollTop = dom.messages.scrollHeight;
}

function clearEmptyState() {
  const empty = dom.messages.querySelector('.empty-state');
  if (empty) empty.remove();
}

function updateTokens(delta = 0) {
  state.totalTokens += delta;
  dom.tokenCounter.textContent = `${state.totalTokens} tokens`;
}


//  Extracción de código 

// Extrae el primer bloque ```html ... ``` de un string dado
function extractBlock(text, lang) {
  const re = new RegExp('```' + lang + '\\s*\\n?([\\s\\S]*?)```', 'i');
  const match = text.match(re);
  return match ? match[1].trim() : '';
}

// Parsea la respuesta completa del modelo y actualiza state.lastHtml / lastCss
function extractCode(fullText) {
  const html = extractBlock(fullText, 'html');
  const css  = extractBlock(fullText, 'css');
  if (html) state.lastHtml = html;
  if (css)  state.lastCss  = css;
}


//  Preview 

// Combina el HTML y CSS extraídos e inyecta el resultado en el iframe del modal
function openPreview() {
  if (!state.lastHtml && !state.lastCss) return;

  // Construir documento completo si el HTML generado no tiene <style> embebido
  const hasStyle = state.lastHtml.includes('<style');
  const doc = hasStyle
    ? state.lastHtml
    : `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
${state.lastCss}
  </style>
</head>
<body>
${state.lastHtml}
</body>
</html>`;

  // Escribir directamente en el iframe para evitar restricciones de URL
  dom.previewFrame.srcdoc = doc;
  dom.previewModal.hidden = false;
}

function closePreview() {
  dom.previewModal.hidden = true;
}

dom.previewBtn.addEventListener('click', openPreview);
dom.previewClose.addEventListener('click', closePreview);


//  Descarga 

// Descarga los archivos HTML y CSS generados como archivos separados
function downloadFiles() {
  if (!state.lastHtml && !state.lastCss) return;

  const timestamp = Date.now();

  if (state.lastHtml) {
    // Incluir referencia al CSS en el HTML descargado
    const fullHtml = state.lastHtml.includes('<link')
      ? state.lastHtml
      : state.lastHtml.replace('</head>', `  <link rel="stylesheet" href="styles.css" />\n</head>`);

    const blobHtml = new Blob([fullHtml], { type: 'text/html' });
    const aHtml = document.createElement('a');
    aHtml.href = URL.createObjectURL(blobHtml);
    aHtml.download = `index-${timestamp}.html`;
    aHtml.click();
    URL.revokeObjectURL(aHtml.href);
  }

  if (state.lastCss) {
    const blobCss = new Blob([state.lastCss], { type: 'text/css' });
    const aCss = document.createElement('a');
    aCss.href = URL.createObjectURL(blobCss);
    aCss.download = `styles-${timestamp}.css`;
    aCss.click();
    URL.revokeObjectURL(aCss.href);
  }
}

dom.downloadBtn.addEventListener('click', downloadFiles);


//  Mensajes 

function appendMessage(role, content) {
  clearEmptyState();

  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = role === 'user' ? 'tú' : 'wf';

  const body = document.createElement('div');
  body.className = 'msg-body';

  const roleLabel = document.createElement('div');
  roleLabel.className = 'msg-role';
  roleLabel.textContent = role === 'user' ? 'usuario' : 'webforge';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'msg-content';
  contentDiv.innerHTML = renderMarkdown(content);

  body.appendChild(roleLabel);
  body.appendChild(contentDiv);
  wrap.appendChild(avatar);
  wrap.appendChild(body);
  dom.messages.appendChild(wrap);
  scrollBottom();

  return contentDiv;
}

function showError(msg) {
  clearEmptyState();
  const el = document.createElement('div');
  el.className = 'msg-error';
  el.textContent = `error: ${msg}`;
  dom.messages.appendChild(el);
  scrollBottom();
}


//  Skills 

function buildSkillsBlock() {
  const entries = Object.entries(state.skills);
  if (entries.length === 0) return '';
  return entries
    .map(([name, content]) => `### skill: ${name}\n${content}`)
    .join('\n\n---\n\n');
}

function buildSystemPrompt() {
  const base   = dom.systemPrompt.value.trim();
  const skills = buildSkillsBlock();
  if (!skills) return base;
  return `A continuación se presentan las skills disponibles para este agente:\n\n${skills}\n\n---\n\n${base}`;
}

function loadSkillFile(file) {
  const reader = new FileReader();
  reader.onload = e => {
    const name = file.name.replace(/\.md$/, '');
    state.skills[name] = e.target.result;
    renderSkillTag(name);
  };
  reader.readAsText(file, 'utf-8');
}

function renderSkillTag(name) {
  const existing = dom.skillsList.querySelector(`[data-skill="${name}"]`);
  if (existing) return;

  const tag = document.createElement('div');
  tag.className = 'skill-tag';
  tag.dataset.skill = name;
  tag.innerHTML = `<span>${name}</span><button title="quitar skill">x</button>`;

  tag.querySelector('button').addEventListener('click', () => {
    delete state.skills[name];
    tag.remove();
  });

  dom.skillsList.appendChild(tag);
}


//  Stream 

async function streamResponse(prompt) {
  const endpoint = dom.endpointInput.value.replace(/\/$/, '');
  const model    = dom.modelSelect.value;
  const temp     = parseFloat(dom.tempSlider.value);
  const system   = buildSystemPrompt();

  const messages = [];
  if (system) messages.push({ role: 'system', content: system });
  messages.push(...state.history);
  messages.push({ role: 'user', content: prompt });

  const contentNode = appendMessage('assistant', '');
  const cursor = document.createElement('span');
  cursor.className = 'cursor-blink';
  contentNode.appendChild(cursor);
  scrollBottom();

  let accumulated   = '';
  let tokenEstimate = 0;

  try {
    const res = await fetch(`${endpoint}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        messages,
        stream: true,
        options: { temperature: temp },
      }),
    });

    if (!res.ok) {
      const err = await res.text().catch(() => res.statusText);
      throw new Error(`HTTP ${res.status}: ${err}`);
    }

    const reader  = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n').filter(Boolean);

      for (const line of lines) {
        let parsed;
        try { parsed = JSON.parse(line); } catch { continue; }

        const token = parsed?.message?.content ?? '';
        accumulated  += token;
        tokenEstimate += token.split(/\s+/).length;

        contentNode.innerHTML = renderMarkdown(accumulated);
        contentNode.appendChild(cursor);
        scrollBottom();

        if (parsed.done) {
          cursor.remove();
          // Extraer bloques de código para preview y descarga
          extractCode(accumulated);

          state.history.push({ role: 'user',      content: prompt });
          state.history.push({ role: 'assistant', content: accumulated });
          updateTokens(tokenEstimate);
          break;
        }
      }
    }

  } catch (err) {
    cursor.remove();
    if (contentNode.textContent.trim() === '') {
      contentNode.closest('.msg')?.remove();
    }
    showError(err.message);
  }
}


//  Conexión 

async function checkConnection() {
  const endpoint = dom.endpointInput.value.replace(/\/$/, '');
  dom.statusDot.className    = 'status-dot';
  dom.statusText.textContent = 'verificando…';

  try {
    const res = await fetch(`${endpoint}/api/tags`, { signal: AbortSignal.timeout(4000) });
    if (!res.ok) throw new Error();

    const data   = await res.json();
    const models = data?.models?.map(m => m.name) ?? [];

    if (models.length > 0) {
      const current = dom.modelSelect.value;
      dom.modelSelect.innerHTML = '';
      models.forEach(name => {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        if (name === current) opt.selected = true;
        dom.modelSelect.appendChild(opt);
      });
    }

    dom.statusDot.className    = 'status-dot online';
    dom.statusText.textContent = `conectado · ${models.length} modelo${models.length !== 1 ? 's' : ''}`;

  } catch {
    dom.statusDot.className    = 'status-dot error';
    dom.statusText.textContent = 'sin conexión';
  }
}


//  Export chat 

function exportChat() {
  if (state.history.length === 0) return;

  const lines = state.history.map(msg => {
    const prefix = msg.role === 'user' ? '[usuario]' : `[${dom.modelSelect.value}]`;
    return `${prefix}\n${msg.content}`;
  });

  const blob = new Blob([lines.join('\n\n---\n\n')], { type: 'text/plain' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `webforge-chat-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}


//  Textarea autoresize 

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}


//  Event listeners 

dom.form.addEventListener('submit', async e => {
  e.preventDefault();
  if (state.streaming) return;

  const text = dom.input.value.trim();
  if (!text) return;

  dom.input.value = '';
  autoResize(dom.input);
  dom.sendBtn.disabled = true;
  state.streaming = true;

  appendMessage('user', text);
  await streamResponse(text);

  state.streaming = false;
  dom.sendBtn.disabled = false;
  dom.input.focus();
});

dom.input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    dom.form.requestSubmit();
  }
});

dom.input.addEventListener('input', () => autoResize(dom.input));

dom.tempSlider.addEventListener('input', () => {
  dom.tempVal.textContent = parseFloat(dom.tempSlider.value).toFixed(2);
});

dom.checkBtn.addEventListener('click', checkConnection);

dom.skillsDrop.addEventListener('click', () => dom.skillsInput.click());

dom.skillsDrop.addEventListener('dragover', e => {
  e.preventDefault();
  dom.skillsDrop.style.borderColor = 'var(--accent)';
});

dom.skillsDrop.addEventListener('dragleave', () => {
  dom.skillsDrop.style.borderColor = '';
});

dom.skillsDrop.addEventListener('drop', e => {
  e.preventDefault();
  dom.skillsDrop.style.borderColor = '';
  const files = [...e.dataTransfer.files].filter(f => f.name.endsWith('.md'));
  files.forEach(loadSkillFile);
});

dom.skillsInput.addEventListener('change', () => {
  [...dom.skillsInput.files].forEach(loadSkillFile);
  dom.skillsInput.value = '';
});

dom.clearBtn.addEventListener('click', () => {
  state.history    = [];
  state.totalTokens = 0;
  state.lastHtml   = '';
  state.lastCss    = '';
  updateTokens(0);
  dom.messages.innerHTML = `
    <div class="empty-state">
      <p class="empty-label">describe el componente o página que quieres generar</p>
    </div>`;
});

dom.exportBtn.addEventListener('click', exportChat);

// Init
checkConnection();