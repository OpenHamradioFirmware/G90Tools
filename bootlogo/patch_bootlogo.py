from PIL import Image
import os
import sys
import hashlib

offsets = {
    "486d8c1cb135ef1cbdaa15d50ad28d54fd99ac711dd9763c2d49b48d818b7ac6": 0x20854, # G90_DispUnit_FW_V1.74final.xgf.decrypt
    "0e9023ecc41d017d96143fa955c5ac74646bf7ad4f6347a359e013e5160c9fc2": 0x20530, # G90_DispUnit_FW_V1.75final2020090501.xgf.decrypt
    "9a23e1c36afd2348f43157cbbf62235e6e1070ef807ded3926b18320ce1f22b7": 0x1C6F8, # G90_DispUnit_Fw_V1.80.xgf.decrypt
}

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <new bootlogo image> <decrypted dispunit firmware to patch>")
        print(f"    note: converts image to black and white before patching")
        return

    new_bootlogo_image = sys.argv[1]
    decrypted_firmware = sys.argv[2]

    img = Image.open(new_bootlogo_image).convert("L")
    img_data = img.load()

    width, height = img.size
    if width != 48 or height != 48:
        print(f"new bootlogo image width and height must be 48x48 (was {width}x{height})")
        return

    img_bytes = []
    for y in range(48):
        for x in range(48 // 8):
            b = 0
            for i in range(8):
                pixel = img_data[x * 8 + i, y]
                bit = 1 if pixel == 255 else 0
                b = (b << 1) | bit
            img_bytes.append(b)

    with open(decrypted_firmware, "r+b") as f:
        data = f.read()

        m = hashlib.sha256()
        m.update(data)
        h = m.hexdigest()

        if h in offsets:
            offset = offsets[h]
            print(f"Found matching hash {h}, using offset 0x{offset:x}")
            f.seek(offset, os.SEEK_SET)
            f.write(bytes(img_bytes))

            print("done: new bootlogo image patched")
        else:
            print(f"Unknown hash {h}")
            print("error: Offset unknown for provided firmware (use find_offset.py to try to find the offset)")

if __name__ == "__main__":
    main()
