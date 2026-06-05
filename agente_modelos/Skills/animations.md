# skill: animations

Animaciones y microinteracciones CSS listas para usar. Aplícalas con criterio: menos es más.

## Principios

- Duración: hover/foco → 150ms, entrada → 200-300ms, salida → 150ms.
- Curva por defecto: `ease` o `cubic-bezier(0.4, 0, 0.2, 1)` (Material).
- Respeta `prefers-reduced-motion` siempre.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Entrada de elementos (fade + slide)

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}

.animate-fade-up  { animation: fade-up  0.25s ease-out both; }
.animate-fade-in  { animation: fade-in  0.2s  ease-out both; }
.animate-scale-in { animation: scale-in 0.2s  ease-out both; }
```

Para animar lista de items con delay escalonado:
```css
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 60ms; }
.item:nth-child(3) { animation-delay: 120ms; }
/* o con JS: el.style.animationDelay = i * 60 + 'ms' */
```

---

## Hover en cards

```css
.card {
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.35);
  border-color: var(--color-accent);
}
```

---

## Botón con efecto ripple (CSS puro)

```css
.btn {
  position: relative;
  overflow: hidden;
}
.btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.12);
  opacity: 0;
  transition: opacity 0.15s;
}
.btn:active::after { opacity: 1; }
```

---

## Skeleton loader

```css
@keyframes shimmer {
  from { background-position: -200% center; }
  to   { background-position:  200% center; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 25%,
    rgba(255,255,255,0.05) 50%,
    var(--color-surface) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.4s ease infinite;
  border-radius: var(--radius);
}

/* Uso: */
.skeleton-text  { height: 14px; margin-bottom: 8px; }
.skeleton-title { height: 22px; width: 60%; margin-bottom: 12px; }
.skeleton-avatar { width: 40px; height: 40px; border-radius: 50%; }
```

---

## Spinner de carga

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
```

---

## Tooltip CSS puro

```html
<span class="tooltip-wrap">
  Hover me
  <span class="tooltip">Texto del tooltip</span>
</span>
```
```css
.tooltip-wrap { position: relative; display: inline-flex; }
.tooltip {
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: #1f2419;
  color: var(--color-text);
  font-size: 11px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.15s;
  border: 1px solid var(--color-border);
}
.tooltip-wrap:hover .tooltip { opacity: 1; }
```
