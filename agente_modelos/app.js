/*
 * app.js — Ollama Dev
 *
 * Maneja el ciclo completo de una conversación con Ollama:
 * construcción del payload, lectura del stream NDJSON,
 * renderizado incremental en el DOM y gestión del historial.
 */

// Atajo para no repetir document.getElementById en cada referencia al DOM
const SEL = id => document.getElementById(id);

// Referencias centralizadas a todos los nodos que se tocan en tiempo de ejecución
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
  tokenCounter:  SEL('token-counter'),
  skillsDrop:    SEL('skills-drop'),
  skillsInput:   SEL('skills-input'),
  skillsList:    SEL('skills-list'),
};

// Estado global mutable de la sesión actual
let state = {
  history: [],      // acumulado de turnos {role, content} para enviar como contexto
  streaming: false, // bloquea envíos mientras hay una respuesta en curso
  totalTokens: 0,   // estimación acumulada de tokens consumidos en la sesión
  skills: {},       // mapa nombre -> contenido de cada skill cargada desde .md
};


// Escapa caracteres HTML conflictivos antes de insertar texto arbitrario en el DOM.
// Necesario para evitar inyecciones cuando el modelo devuelve < > & en su respuesta.
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Convierte un subconjunto de Markdown a HTML.
// Solo cubre los patrones más frecuentes en respuestas técnicas:
// bloques de código con etiqueta de lenguaje, código inline y negrita.
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

// Lleva el scroll del contenedor de mensajes al fondo.
// Se llama después de cada inserción o actualización de contenido.
function scrollBottom() {
  dom.messages.scrollTop = dom.messages.scrollHeight;
}

// Elimina el placeholder vacío que se muestra cuando no hay mensajes.
// Se invoca antes de insertar el primer mensaje real de la sesión.
function clearEmptyState() {
  const empty = dom.messages.querySelector('.empty-state');
  if (empty) empty.remove();
}

// Suma delta al contador de tokens y actualiza el texto visible en la topbar.
// Cuando delta es 0 se usa para resetear la etiqueta sin modificar el acumulado.
function updateTokens(delta = 0) {
  state.totalTokens += delta;
  dom.tokenCounter.textContent = `${state.totalTokens} tokens`;
}


// Construye e inserta un bubble de mensaje en el DOM.
// Devuelve el nodo .msg-content para que streamResponse pueda actualizarlo
// token a token sin recrear toda la estructura.
function appendMessage(role, content) {
  clearEmptyState();

  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = role === 'user' ? 'tú' : 'jt';

  const body = document.createElement('div');
  body.className = 'msg-body';

  const roleLabel = document.createElement('div');
  roleLabel.className = 'msg-role';
  roleLabel.textContent = role === 'user' ? 'usuario' : 'javatutor';

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

// Muestra un mensaje de error inline con estilo diferenciado.
// Se usa cuando el fetch falla o el servidor devuelve un código de error.
function showError(msg) {
  clearEmptyState();
  const el = document.createElement('div');
  el.className = 'msg-error';
  el.textContent = `error: ${msg}`;
  dom.messages.appendChild(el);
  scrollBottom();
}


// Concatena todas las skills cargadas en un bloque de texto con separadores,
// replicando el comportamiento de load_all_skills() del agente Python.
// Devuelve string vacío si no hay skills activas.
function buildSkillsBlock() {
  const entries = Object.entries(state.skills);
  if (entries.length === 0) return '';

  const parts = entries.map(([name, content]) => `### skill: ${name}\n${content}`);
  return parts.join('\n\n---\n\n');
}

// Construye el system prompt final combinando el texto base del textarea
// con el bloque de skills inyectado al inicio, igual que build_system_prompt()
// en el agente Python. Si no hay skills, devuelve solo el prompt base.
function buildSystemPrompt() {
  const base   = dom.systemPrompt.value.trim();
  const skills = buildSkillsBlock();

  if (!skills) return base;

  return `A continuación se presentan las skills disponibles para este agente:\n\n${skills}\n\n---\n\n${base}`;
}

// Lee un archivo .md como texto y lo registra en state.skills.
// Al terminar, renderiza la etiqueta visual en la lista de skills activas.
function loadSkillFile(file) {
  const reader = new FileReader();
  reader.onload = e => {
    const name = file.name.replace(/\.md$/, '');
    state.skills[name] = e.target.result;
    renderSkillTag(name);
  };
  reader.readAsText(file, 'utf-8');
}

// Inserta una etiqueta visual en el panel de skills con botón para eliminarla.
// Al pulsar el botón se borra la skill del estado y se remueve la etiqueta del DOM.
function renderSkillTag(name) {
  // evitar duplicados si el mismo archivo se carga dos veces
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



// incrementalmente mientras llegan los chunks NDJSON.
//
// Ollama devuelve una línea JSON por chunk; cada línea tiene la forma:
//   { message: { role, content }, done: false }
// y la última tiene done:true. Se acumula el contenido y se vuelca al DOM
// en cada iteración para dar la sensación de escritura en tiempo real.
async function streamResponse(prompt) {
  const endpoint = dom.endpointInput.value.replace(/\/$/, '');
  const model    = dom.modelSelect.value;
  const temp     = parseFloat(dom.tempSlider.value);
  // Combinar system prompt base con las skills cargadas antes de armar el payload
  const system = buildSystemPrompt();

  // Armar el array de mensajes: system (opcional) + historial previo + turno actual
  const messages = [];
  if (system) messages.push({ role: 'system', content: system });
  messages.push(...state.history);
  messages.push({ role: 'user', content: prompt });

  // Crear el bubble del asistente vacío con cursor parpadeante antes de recibir datos
  const contentNode = appendMessage('assistant', '');
  const cursor = document.createElement('span');
  cursor.className = 'cursor-blink';
  contentNode.appendChild(cursor);
  scrollBottom();

  let accumulated  = '';
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

      // Un chunk puede contener varias líneas NDJSON; se procesan una por una
      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n').filter(Boolean);

      for (const line of lines) {
        let parsed;
        try { parsed = JSON.parse(line); } catch { continue; }

        const token = parsed?.message?.content ?? '';
        accumulated  += token;
        tokenEstimate += token.split(/\s+/).length;

        // Re-renderizar solo el innerHTML del nodo de contenido (no todo el bubble)
        // para no perder la referencia al cursor ni forzar reflow innecesarios
        contentNode.innerHTML = renderMarkdown(accumulated);
        contentNode.appendChild(cursor);
        scrollBottom();

        if (parsed.done) {
          cursor.remove();
          state.history.push({ role: 'user',      content: prompt });
          state.history.push({ role: 'assistant', content: accumulated });
          updateTokens(tokenEstimate);
          break;
        }
      }
    }

  } catch (err) {
    cursor.remove();
    // Si no llegó ningún token, eliminar el bubble vacío que se creó anticipadamente
    if (contentNode.textContent.trim() === '') {
      contentNode.closest('.msg')?.remove();
    }
    showError(err.message);
  }
}


// Consulta /api/tags para saber si Ollama está activo y qué modelos tiene instalados.
// Si la respuesta es válida, repuebla el <select> con los modelos reales del sistema.
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


// Serializa el historial de la sesión a un archivo .txt descargable.
// Cada turno queda separado por un divisor para facilitar lectura posterior.
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
  a.download = `chat-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}

// Ajusta la altura del textarea al contenido escrito, con techo en 160px.
// Se llama en cada evento 'input' para que el campo crezca de forma natural.
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}


// Submit del formulario: valida, bloquea envíos concurrentes,
// muestra el mensaje del usuario y lanza el stream.
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

// Enter sin Shift envía; con Shift inserta salto de línea normal
dom.input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    dom.form.requestSubmit();
  }
});

dom.input.addEventListener('input', () => autoResize(dom.input));

// Actualiza la etiqueta numérica del slider de temperatura en tiempo real
dom.tempSlider.addEventListener('input', () => {
  dom.tempVal.textContent = parseFloat(dom.tempSlider.value).toFixed(2);
});

dom.checkBtn.addEventListener('click', checkConnection);

// Clic en el área de drop abre el selector de archivos del sistema operativo
dom.skillsDrop.addEventListener('click', () => dom.skillsInput.click());

// Drag & drop de archivos .md directamente sobre el área de skills
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

// Procesamiento de archivos seleccionados desde el selector nativo
dom.skillsInput.addEventListener('change', () => {
  [...dom.skillsInput.files].forEach(loadSkillFile);
  dom.skillsInput.value = ''; // reset para permitir recargar el mismo archivo
});

// Limpia el historial en memoria y restaura el estado visual inicial
dom.clearBtn.addEventListener('click', () => {
  state.history = [];
  state.totalTokens = 0;
  updateTokens(0);
  dom.messages.innerHTML = `
    <div class="empty-state">
      <p class="empty-label">pega tu código Java o describe el error</p>
    </div>`;
});

dom.exportBtn.addEventListener('click', exportChat);

// Verificación inicial al cargar la página
checkConnection();