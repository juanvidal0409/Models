# skill: layout-patterns

Patrones de layout CSS modernos que debes usar por defecto. Nunca uses `float` ni `position: absolute` para layout general.

## Grid vs Flexbox — cuándo usar cada uno

| Situación | Usa |
|---|---|
| Una sola fila/columna de elementos | Flexbox |
| Layout 2D (filas Y columnas) | CSS Grid |
| Centrar un elemento | Flexbox o Grid con `place-items: center` |
| Navegación horizontal | Flexbox |
| Card grid responsive | CSS Grid con `auto-fill` |

## Patrones más comunes

### Navbar horizontal
```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-6);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}
```

### Card grid responsive (sin media queries)
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}
```

### Sidebar + contenido principal
```css
.shell {
  display: grid;
  grid-template-columns: 260px 1fr;
  height: 100vh;
}
```

### Centrado absoluto
```css
.centered {
  display: grid;
  place-items: center;
  min-height: 100vh;
}
```

### Stack vertical con gap uniforme
```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
```

## Responsive

Usa siempre `min-width` (mobile-first):

```css
/* móvil por defecto */
.container { padding: var(--space-4); }

@media (min-width: 768px) {
  .container { padding: var(--space-8); }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1200px;
    margin-inline: auto;
  }
}
```

## Reglas

- El `box-sizing: border-box` siempre en `*, *::before, *::after`.
- Nunca uses `height` fijo en contenedores de texto; usa `min-height`.
- Para scroll interno usa `overflow-y: auto` + `max-height`, no `overflow: scroll`.
