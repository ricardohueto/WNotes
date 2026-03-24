# convert_icon.py
from PIL import Image
from pathlib import Path

PNG_PATH = Path("assets/icons/icon.png")

def to_ico(png_path: Path) -> None:
    img = Image.open(png_path).convert("RGBA")
    ico_path = png_path.with_suffix(".ico")
    img.save(ico_path, format="ICO", sizes=[
        (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
    ])
    print(f"ICO saved: {ico_path}")

def to_icns(png_path: Path) -> None:
    from struct import pack
    import io
    img = Image.open(png_path).convert("RGBA")
    icns_path = png_path.with_suffix(".icns")
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    icons = {}
    for size in sizes:
        resized = img.resize((size, size), Image.LANCZOS)
        buffer = io.BytesIO()
        resized.save(buffer, format="PNG")
        icons[size] = buffer.getvalue()

    with open(icns_path, "wb") as f:
        icon_data = b""
        type_map = {
            16: b"icp4", 32: b"icp5", 64: b"icp6",
            128: b"ic07", 256: b"ic08", 512: b"ic09", 1024: b"ic10"
        }
        for size, data in icons.items():
            type_code = type_map[size]
            length = len(data) + 8
            icon_data += type_code + pack(">I", length) + data
        total_length = len(icon_data) + 8
        f.write(b"icns" + pack(">I", total_length) + icon_data)
    print(f"ICNS saved: {icns_path}")

if __name__ == "__main__":
    to_ico(PNG_PATH)
    to_icns(PNG_PATH)
