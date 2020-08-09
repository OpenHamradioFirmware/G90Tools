import os
import sys
import json
import struct
import hashlib

def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <decrypted bootloader firmware to patch>')
        print(f'    note: only use on firmware 1.74')
        return

    decrypted_firmware = sys.argv[1]

    with open(decrypted_firmware, 'r+b') as f:
        m = hashlib.sha256()
        m.update(f.read())
        h = m.hexdigest()
        if h == 'e3654a811235a4eed139209df3636ee44324f8c9aab3e88141de93b40cf29706':
            print('Already patched')
            exit()
        elif h == '22c8b4a01f711063c254ce256ba19be864bb79c94894afb0655d870a9e0fa208':
            # Display Unit bootloader
            offset = 0x188e
        elif h == '7988d7fb5ba5a2738f1df57ad8a6cba6e625a66346de7ee1a91c4683a5480455':
            # Main Unit bootloader
            print('TODO: Main unit bootloader is not supported yet.')
            exit()
        else:
            print('Unsupported binary.')
            exit()

        f.seek(offset, os.SEEK_SET)
        f.write(bytes(b'\x00\xb0') * 11)

    print('done: Lock disabled')

if __name__ == '__main__':
    main()
