"""Genera assets/css/incisioni.css: i disegni degli ingredienti come data URI.
Un'immagine usata come maschera CSS da file separato non si carica aprendo la pagina
con doppio clic (file://): incorporata qui funziona sia in locale sia online.
Per la maschera conta solo l'alpha, quindi la compressione dell'alpha può essere decisa."""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets/img/incisioni"
TARGET = ROOT / "assets/css/incisioni.css"
MAX_SIDE = 320       # i disegni non superano i ~200 px a schermo: 320 basta anche sui retina
ALPHA_QUALITY = 50

rules = [
    "/* Generato da tools/genera-incisioni.py: non modificare a mano. */",
    ".inc { -webkit-mask-image: var(--m); mask-image: var(--m); }",
]
for image_path in sorted(SOURCE.glob("*.webp")):
    image = Image.open(image_path).convert("RGBA")
    image.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    mask = Image.new("RGBA", image.size, (255, 255, 255, 0))
    mask.putalpha(image.getchannel("A"))
    buffer = io.BytesIO()
    mask.save(buffer, "WEBP", quality=60, alpha_quality=ALPHA_QUALITY, method=6)
    data = base64.b64encode(buffer.getvalue()).decode()
    rules.append(f'.inc-{image_path.stem} {{ --m: url("data:image/webp;base64,{data}"); }}')

TARGET.write_text("\n".join(rules) + "\n")
print(TARGET, TARGET.stat().st_size, "byte")
