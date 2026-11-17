from pathlib import Path
from PIL import Image

p = Path(__file__).resolve().parent / "sample.png"
Image.new("RGB", (500, 400), (30, 100, 180)).save(p)
print(p)
