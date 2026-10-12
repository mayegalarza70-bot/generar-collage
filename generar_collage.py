from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

# ---- CONFIGURACIÓN -------------------------------------------------
RUTA_ENTRADA   = "fotos"            # carpeta con 10 imágenes
ARCHIVO_SALIDA = "collage_1x8-verano.jpg"

COLS, ROWS = 1, 8                   # 1 columna × 8 filas
ANCHO_CELDA, ALTO_CELDA = 800, 800  # cuadradas; cambia a tu gusto
PADDING = 10                        # margen entre celdas

TAM_NUMERO = 80
COLOR_NUM  = (255, 255, 255)        # blanco
BG_NUM     = (200, 0, 0)            # rojo etiqueta

# --- FRANJA LATERAL DERECHA ----------------------------------------
FRANJA_ANCHO = 200
COLOR_FRANJA = (222, 49, 99)        # rojo cherry aprox
TAM_TEXTO_VERTICAL = 140           # tamaño del texto vertical
# -------------------------------------------------------------------

# Fuente para los numeritos
try:
    FUENTE = ImageFont.truetype("arial.ttf", TAM_NUMERO)
except OSError:
    FUENTE = ImageFont.load_default()

# Fuente para el texto vertical (emoji-friendly primero)
FUENTE_VERTICAL = None
for font_name in ["seguiemj.ttf", "arialbd.ttf", "arial.ttf"]:
    try:
        FUENTE_VERTICAL = ImageFont.truetype(font_name, TAM_TEXTO_VERTICAL)
        print("Usando fuente vertical:", font_name)
        break
    except OSError:
        continue
if FUENTE_VERTICAL is None:
    FUENTE_VERTICAL = ImageFont.load_default()
# --------------------------------------------------------------------

# ancho solo del collage (sin la franja)
ANCHO_COLLAGE = COLS * ANCHO_CELDA + (COLS + 1) * PADDING
ALTO_TOTAL    = ROWS * ALTO_CELDA  + (ROWS + 1) * PADDING

# ancho total incluyendo la franja de 200 px
ANCHO_TOTAL = ANCHO_COLLAGE + FRANJA_ANCHO

lienzo = Image.new("RGB", (ANCHO_TOTAL, ALTO_TOTAL), (255, 255, 255))

# extensiones admitidas
fotos = sorted([
    f for f in os.listdir(RUTA_ENTRADA)
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
])[:ROWS*COLS]

if len(fotos) < ROWS*COLS:
    raise ValueError(f"Se necesitan {ROWS*COLS} imágenes en la carpeta '{RUTA_ENTRADA}'.")

for idx, nombre in enumerate(fotos, start=1):
    # 1) Abrir y ajustar con recorte para ocupar la celda completa
    im = Image.open(os.path.join(RUTA_ENTRADA, nombre)).convert("RGB")
    im_fit = ImageOps.fit(im, (ANCHO_CELDA, ALTO_CELDA), Image.LANCZOS, centering=(0.5, 0.5))

    # 2) Etiqueta numérica sobre la propia imagen
    draw = ImageDraw.Draw(im_fit)
    numero = str(idx)
    try:
        bbox = draw.textbbox((0, 0), numero, font=FUENTE)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(numero, font=FUENTE)

    etiqueta_w = TAM_NUMERO + 30
    etiqueta_h = TAM_NUMERO + 30
    draw.rectangle([(0, 0), (etiqueta_w, etiqueta_h)], fill=BG_NUM)
    draw.text((15, 15), numero, font=FUENTE, fill=COLOR_NUM)

    # 3) Posición en el lienzo
    fila = (idx - 1) // COLS
    col  = (idx - 1) % COLS
    pos_x = PADDING + col  * (ANCHO_CELDA + PADDING)
    pos_y = PADDING + fila * (ALTO_CELDA + PADDING)
    lienzo.paste(im_fit, (pos_x, pos_y))

# --- FRANJA CHERRY CON TEXTO VERTICAL + EMOJIS ---------------------
franja = Image.new("RGB", (FRANJA_ANCHO, ALTO_TOTAL), COLOR_FRANJA)
draw_franja = ImageDraw.Draw(franja)

# Aquí pones tus emojis favoritos 😍
texto_vertical = "🍒 CHERRY MODA 🍒"

# 1) Medimos cada carácter para centrarlo mejor
char_metrics = []
h_max = 0

for ch in texto_vertical:
    if ch == " ":
        # el espacio no se dibuja, pero mantiene el alto
        char_metrics.append((0, 0))
        continue

    try:
        bbox = draw_franja.textbbox((0, 0), ch, font=FUENTE_VERTICAL)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw_franja.textsize(ch, font=FUENTE_VERTICAL)

    char_metrics.append((w, h))
    h_max = max(h_max, h)

# 2) Espaciado vertical y posición inicial (centrado vertical del bloque)
LINE_HEIGHT  = int(h_max * 1.8) if h_max > 0 else 0
num_lineas   = len(texto_vertical)
total_height = LINE_HEIGHT * num_lineas
start_y      = (ALTO_TOTAL - total_height) // 2

# 3) Dibujamos cada carácter centrado en la franja y con "negrita" simulada
y = start_y
for ch, (w, h) in zip(texto_vertical, char_metrics):
    if ch != " ":
        # centrado horizontal por carácter
        x = (FRANJA_ANCHO - w) // 2

        # "negrita" / stroke: varios trazos alrededor
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
            draw_franja.text((x + dx, y + dy), ch, font=FUENTE_VERTICAL, fill=(140, 0, 60))

        # texto principal blanco encima
        draw_franja.text((x, y), ch, font=FUENTE_VERTICAL, fill=(255, 255, 255))

    y += LINE_HEIGHT

# pegar franja ya con texto en el lienzo principal
lienzo.paste(franja, (ANCHO_COLLAGE, 0))
# -------------------------------------------------------------------

lienzo.save(ARCHIVO_SALIDA, quality=95)
print("✅ Collage generado:", ARCHIVO_SALIDA)
