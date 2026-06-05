# skill: html-semantics

Reglas de HTML semántico y accesibilidad que debes aplicar siempre en el código generado.

## Estructura base de página

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Descripción de la página" />
  <title>Título — Sitio</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header>...</header>
  <nav>...</nav>
  <main>
    <section>...</section>
    <article>...</article>
    <aside>...</aside>
  </main>
  <footer>...</footer>
</body>
</html>
```

## Etiquetas correctas según contexto

| Contenido | Etiqueta correcta | Nunca usar |
|---|---|---|
| Navegación principal | `<nav>` | `<div class="nav">` |
| Encabezado de página/sección | `<header>` | `<div class="header">` |
| Contenido principal | `<main>` | `<div class="main">` |
| Pie de página | `<footer>` | `<div class="footer">` |
| Artículo independiente | `<article>` | `<div class="article">` |
| Sección temática | `<section>` | `<div class="section">` |
| Contenido lateral | `<aside>` | `<div class="sidebar">` |
| Botón que ejecuta acción | `<button>` | `<div onclick>` o `<a>` |
| Enlace de navegación | `<a href>` | `<button>` |
| Lista de items | `<ul>/<ol>+<li>` | `<div>` repetidos |
| Imagen decorativa | `<img alt="">` | omitir alt |
| Imagen informativa | `<img alt="descripción">` | alt vacío |

## Accesibilidad mínima

- Todo `<img>` debe tener `alt`. Si es decorativa: `alt=""`.
- Todo `<input>` debe tener un `<label>` asociado con `for` / `id` o estar dentro del label.
- Los botones de solo icono necesitan `aria-label`: `<button aria-label="Cerrar">✕</button>`.
- Los modales necesitan `role="dialog"` y `aria-modal="true"`.
- Nunca uses color como único diferenciador de estado (acompaña con texto o icono).
- Jerarquía de headings: solo un `<h1>` por página, no saltes niveles (`h1 → h2 → h3`).

## Formularios

```html
<form novalidate>
  <div class="field">
    <label for="nombre">Nombre completo</label>
    <input type="text" id="nombre" name="nombre"
           autocomplete="name" required
           aria-describedby="nombre-error" />
    <span id="nombre-error" class="field-error" role="alert" hidden>
      Este campo es requerido
    </span>
  </div>

  <div class="field">
    <label for="tipo">Tipo de cuenta</label>
    <select id="tipo" name="tipo">
      <option value="">Seleccionar...</option>
      <option value="personal">Personal</option>
      <option value="empresa">Empresa</option>
    </select>
  </div>

  <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

## Patrones a evitar

- ❌ `<div onclick="...">` — usa `<button>` o `<a>`
- ❌ `<br><br>` para espaciado — usa margin/padding en CSS
- ❌ `<b>` y `<i>` para estilo — usa `<strong>`, `<em>` o CSS
- ❌ `style="..."` inline — todo en la hoja de estilos
- ❌ `<table>` para layout — solo para datos tabulares
