# skill: design-tokens

Cuando generes CSS, usa siempre custom properties (variables CSS) para colores, tipografía, espaciado y radios. Nunca escribas valores hardcoded repetidos.

## Paleta base recomendada

```css
:root {
  /* Colores */
  --color-bg:        #0d0f0c;
  --color-surface:   #181c15;
  --color-border:    rgba(255, 255, 255, 0.07);
  --color-accent:    #6abf69;
  --color-accent-dim:rgba(106, 191, 105, 0.14);
  --color-text:      #eef2eb;
  --color-text-muted:#525c4a;
  --color-error:     #e07070;
  --color-warning:   #e8a455;

  /* Tipografía */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-display: 'Syne', sans-serif;

  /* Tamaños de fuente */
  --text-xs:   11px;
  --text-sm:   13px;
  --text-base: 15px;
  --text-lg:   18px;
  --text-xl:   24px;
  --text-2xl:  32px;

  /* Espaciado (escala de 4px) */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-6:  24px;
  --space-8:  32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radios */
  --radius-sm: 4px;
  --radius:    8px;
  --radius-lg: 12px;
  --radius-xl: 20px;
  --radius-full: 9999px;

  /* Sombras */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow:    0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.5);

  /* Transiciones */
  --transition: 0.15s ease;
  --transition-slow: 0.3s ease;
}
```

## Reglas de uso

- Usa `var(--color-accent)` para elementos interactivos (botones primarios, links, foco).
- Usa `var(--color-text-muted)` para labels, placeholders y texto secundario.
- Usa `var(--space-*)` para margin, padding y gap — nunca px sueltos.
- Todos los `border-radius` deben usar `var(--radius-*)`.
- Animaciones y hover siempre con `transition: var(--transition)`.
