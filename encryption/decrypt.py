import sys

if len(sys.argv) != 4:
    print("Usage: {} <key in hex> <encrypted.bin> <decrypted.bin>".format(sys.argv[0]))
    exit(1)

KEY = bytes.fromhex(sys.argv[1])

from Crypto.Cipher import AES
cipher = AES.new(KEY, AES.MODE_ECB)

import sys
with open(sys.argv[2], 'rb') as f_in:
    with open(sys.argv[3], 'wb') as f_out:
        while True:
            block = f_in.read(16)
            if len(block) != 16:
                break
            
            block_decrypted = cipher.decrypt(block)
            f_out.write(block_decrypted)