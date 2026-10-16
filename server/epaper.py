"""Convert a Pillow image into the PhotoPainter's 4 bpp Spectra 6 frame format."""

from PIL import Image

WIDTH, HEIGHT = 800, 480
FRAME_SIZE = WIDTH * HEIGHT // 2

# (RGB used for dithering, panel code). Order defines the palette index.
PALETTE = [
    ((0, 0, 0), 0x0),        # black
    ((255, 255, 255), 0x1),  # white
    ((255, 255, 0), 0x2),    # yellow
    ((255, 0, 0), 0x3),      # red
    ((0, 0, 255), 0x5),      # blue
    ((0, 255, 0), 0x6),      # green
]

_palette_image = Image.new("P", (1, 1))
_palette_image.putpalette([c for rgb, _ in PALETTE for c in rgb] + [0, 0, 0] * (256 - len(PALETTE)))
# Unused palette slots are black, so map them to the black code.
_INDEX_TO_CODE = bytes([code for _, code in PALETTE] + [0x0] * (256 - len(PALETTE)))


def quantize(img: Image.Image) -> Image.Image:
    """Fit to 800x480 and Floyd-Steinberg dither to the six panel colours."""
    img = img.convert("RGB")
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return img.quantize(palette=_palette_image, dither=Image.Dither.FLOYDSTEINBERG)


def to_frame(img: Image.Image) -> bytes:
    """Return the 192000-byte frame: byte y*400 + x/2, even x in the high nibble."""
    codes = quantize(img).tobytes().translate(_INDEX_TO_CODE)
    frame = bytearray(FRAME_SIZE)
    frame[:] = bytes((hi << 4) | lo for hi, lo in zip(codes[0::2], codes[1::2]))
    return bytes(frame)


def preview(img: Image.Image) -> Image.Image:
    """RGB image of what the panel will show (with the idealised palette)."""
    return quantize(img).convert("RGB")
