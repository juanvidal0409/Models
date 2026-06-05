# skill: ui-components

Recetas HTML + CSS para los componentes más solicitados. Úsalos como base y adáptalos al contexto del usuario.

---

## Botón primario

```html
<button class="btn btn-primary">Acción</button>
```
```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: var(--transition);
}
.btn-primary {
  background: var(--color-accent);
  color: #0d0f0c;
}
.btn-primary:hover { filter: brightness(1.1); }
.btn-primary:active { transform: scale(0.97); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }
```

---

## Input de texto

```html
<div class="field">
  <label class="field-label" for="email">Email</label>
  <input class="input" type="email" id="email" placeholder="tu@email.com" />
</div>
```
```css
.field { display: flex; flex-direction: column; gap: var(--space-1); }
.field-label {
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}
.input {
  padding: var(--space-2) var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  color: var(--color-text);
  font-size: var(--text-sm);
  outline: none;
  transition: border-color var(--transition);
}
.input:focus { border-color: var(--color-accent); }
.input::placeholder { color: var(--color-text-muted); }
```

---

## Card

```html
<div class="card">
  <h3 class="card-title">Título</h3>
  <p class="card-body">Descripción del contenido.</p>
</div>
```
```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  transition: border-color var(--transition), box-shadow var(--transition);
}
.card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow);
}
.card-title { font-size: var(--text-lg); font-weight: 600; }
.card-body  { font-size: var(--text-sm); color: var(--color-text-muted); line-height: 1.6; }
```

---

## Badge / Etiqueta

```html
<span class="badge badge-green">Activo</span>
```
```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: 0.04em;
}
.badge-green { background: var(--color-accent-dim); color: var(--color-accent); }
.badge-red   { background: rgba(224,112,112,0.14);  color: #e07070; }
.badge-gray  { background: rgba(255,255,255,0.06);  color: var(--color-text-muted); }
```

---

## Modal / Dialog

```html
<div class="overlay" id="overlay">
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-title">Título del modal</h2>
      <button class="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <p>Contenido del modal.</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-primary">Confirmar</button>
    </div>
  </div>
</div>
```
```css
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: grid;
  place-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}
.modal {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  width: min(480px, 90vw);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  box-shadow: var(--shadow-lg);
}
.modal-header { display: flex; align-items: center; justify-content: space-between; }
.modal-title  { font-size: var(--text-lg); font-weight: 600; }
.modal-close  {
  background: none; border: none; color: var(--color-text-muted);
  font-size: 18px; cursor: pointer; transition: color var(--transition);
}
.modal-close:hover { color: var(--color-text); }
.modal-footer { display: flex; justify-content: flex-end; gap: var(--space-2); }
```

---

## Tabla de datos

```html
<div class="table-wrap">
  <table class="table">
    <thead>
      <tr><th>Nombre</th><th>Estado</th><th>Fecha</th></tr>
    </thead>
    <tbody>
      <tr><td>Item 1</td><td><span class="badge badge-green">Activo</span></td><td>2024-01-15</td></tr>
    </tbody>
  </table>
</div>
```
```css
.table-wrap { overflow-x: auto; border-radius: var(--radius-lg); border: 1px solid var(--color-border); }
.table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); }
.table th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: var(--text-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}
.table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
.table tbody tr:last-child td { border-bottom: none; }
.table tbody tr:hover { background: rgba(255,255,255,0.02); }
```
