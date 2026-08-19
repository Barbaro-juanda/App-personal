# App de Hábitos y Finanzas

Prototipo de app móvil en español que combina seguimiento de hábitos con control
de finanzas personales (tarjetas de crédito, cupos, cortes, abonos y metas de ahorro).

## Pantallas

| Tab | Contenido |
|---|---|
| **Hoy** | Resumen del día: hábitos pendientes, racha y presupuesto diario disponible |
| **Hábitos** | Lista de hábitos activos con rachas y % de constancia semanal |
| **Dinero** | Disponible vs. deuda, tarjetas con cupo/corte/pago, abonos y meta de ahorro |
| **Progreso** | Constancia y gasto variable de las últimas 6 semanas + correlación hábitos × dinero |

## Pantalla completa

La app ocupa todo el viewport: no dibuja marco de teléfono ni barra de estado simulada
(hora, señal, batería). Usa `100dvh` y `env(safe-area-inset-*)`, así que respeta la
Dynamic Island y el indicador de inicio del iPhone 16 Pro (402 × 874 pt).

Para que quede sin las barras de Safari, ábrela en el iPhone y usa
**Compartir → Añadir a pantalla de inicio**. Se lanza a pantalla completa.

## Archivos

- **`index.html`** — build autocontenido. React, el runtime y las fuentes IBM Plex Sans
  van embebidos, así que abre sin dependencias externas ni servidor. Es lo que sirve
  GitHub Pages. **Generado — no editarlo a mano.**
- **`build.py`** — regenera `index.html` desde el fuente: `python3 build.py`
- **`App Habitos y Finanzas.dc.html`** — el fuente editable (Claude Design Component):
  plantilla `<x-dc>` + la lógica en `<script type="text/x-dc">`. Carga React y las
  fuentes por CDN.
- **`src/support.js`** — el runtime `dc-runtime` que compila la plantilla y monta el
  componente. Generado; no editar a mano.

## Uso

Abre `index.html` en el navegador — no requiere build.

Para trabajar sobre el fuente hace falta un servidor local (el runtime hace `fetch`
de la plantilla, que `file://` bloquea):

```
python3 -m http.server 8000
```

Luego entra a `http://localhost:8000/App%20Habitos%20y%20Finanzas.dc.html`.

## Nota

Todos los datos son de demostración y están escritos en el propio componente.
No hay backend ni persistencia.
