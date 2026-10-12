# generar-collage

Script en Python que genera un collage vertical de 8 imágenes (1 columna × 8 filas), con número en cada foto y una franja lateral con texto.

## Requisitos

- Python 3
- Pillow:

```
pip install pillow
```

- Fuentes `arial.ttf` y `seguiemj.ttf` (vienen con Windows). Si no las encuentra, usa una fuente por defecto.

## Uso

1. Descarga `generar_collage.py` y ponlo en una carpeta.
2. Crea una carpeta llamada `fotos` junto al script y copia dentro **al menos 8 imágenes** (.jpg, .jpeg, .png o .webp). Usa las primeras 8 por orden alfabético.
3. Abre una terminal en esa carpeta y ejecuta:

```
python generar_collage.py
```

4. El collage se guarda como `collage_1x8-verano.jpg` en la misma carpeta.

## Personalización

Al inicio del script, en la sección de configuración, puedes cambiar:

- `COLS, ROWS`: columnas y filas (la cantidad de fotos es `COLS * ROWS`).
- `ANCHO_CELDA, ALTO_CELDA`: tamaño de cada foto.
- `PADDING`: margen entre fotos.
- `COLOR_FRANJA` y `FRANJA_ANCHO`: color y ancho de la franja lateral.
- `texto_vertical`: el texto de la franja.

## Nota

Este repositorio no incluye imágenes. Usa tus propias fotos o fotos libres de derechos.
