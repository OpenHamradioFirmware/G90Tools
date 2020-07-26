from PIL import Image
import os
import sys

def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <new bootlogo image> <decrypted dispunit firmware to patch>')
        print(f'    note: converts image to black and white before patching')
        return

    new_bootlogo_image = sys.argv[1]
    decrypted_firmware = sys.argv[2]

    img = Image.open(new_bootlogo_image).convert('L')
    img_data = img.load()

    width, height = img.size
    if width != 48 or height != 48:
        print(f'new bootlogo image width and height must be 48x48 (was {width}x{height})')
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

    with open(decrypted_firmware, 'r+b') as f:
        f.seek(0x20854, os.SEEK_SET)
        f.write(bytes(img_bytes))

    print('done: new bootlogo image patched')

if __name__ == '__main__':
    main()
