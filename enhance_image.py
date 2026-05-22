"""
Enhance fig_desenho_experimental.png:
  1. Load source image.
  2. Apply mild noise reduction.
  3. Apply unsharp mask for edge/text sharpening.
  4. Boost contrast/saturation slightly.
  5. Resample to 4K (3840 wide, height keeps aspect ratio) with LANCZOS.
  6. Save high-quality PNG (and a JPEG copy).
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

SRC = Path(r"C:\Users\t-ddasilva\FilesPersonal\Trabalho de Conclusão de Curso\tcc_img_assets\new_assets\fig_desenho_experimental.png")
OUT_DIR = SRC.parent
OUT_PNG = OUT_DIR / "fig_desenho_experimental_4k.png"
OUT_JPG = OUT_DIR / "fig_desenho_experimental_4k.jpg"

TARGET_W = 3840  # 4K UHD width; height derived from aspect ratio


def main() -> None:
    img = Image.open(SRC)
    print(f"Source: {img.size} mode={img.mode}")

    # Flatten alpha onto white to avoid edge halos after sharpening.
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        rgba = img.convert("RGBA")
        bg.paste(rgba, mask=rgba.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")

    # 1) Mild denoise to reduce any compression speckle while preserving edges.
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # 2) Unsharp mask: restore crispness of text and box borders.
    #    radius small enough not to ring, percent moderate, threshold preserves flat regions.
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=160, threshold=2))

    # 3) Subtle tonal lift.
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.15)

    # 4) Resample to 4K while keeping aspect ratio.
    w, h = img.size
    new_h = round(h * TARGET_W / w)
    img_4k = img.resize((TARGET_W, new_h), Image.LANCZOS)
    print(f"Resampled: {img_4k.size}")

    # 5) Final light sharpen after downscale to recover micro-detail.
    img_4k = img_4k.filter(ImageFilter.UnsharpMask(radius=0.8, percent=110, threshold=1))

    img_4k.save(OUT_PNG, format="PNG", optimize=True, compress_level=9, dpi=(300, 300))
    img_4k.save(OUT_JPG, format="JPEG", quality=95, subsampling=0, dpi=(300, 300))

    print(f"Saved: {OUT_PNG} ({OUT_PNG.stat().st_size/1024:.1f} KB)")
    print(f"Saved: {OUT_JPG} ({OUT_JPG.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
