import argparse
from Crypto.Cipher import AES

def do_encrypt(cipher, args):
    with args.fw_plaintext as f_in, args.fw_encrypted as f_out:
        while f_in.readable():
            block_in = f_in.read(16)
            block = cipher.encrypt(block_in.ljust(16, b'\x00'))
            f_out.write(block)
            if len(block_in) != 16:
                break
        print(f'success: encrypted firmware written to {f_out.name}')

def do_decrypt(cipher, args):
    with args.fw_encrypted as f_in, args.fw_plaintext as f_out:
        f_out.write(cipher.decrypt(f_in.read()))
        print(f'success: plaintext firmware written to {f_out.name}')

def main():
    parser = argparse.ArgumentParser(description='xiegu g90 firmware encryption/decryption utility')
    parser.add_argument('key', help='256-bit AES key in hex')

    subparsers = parser.add_subparsers(title='mode', dest='mode', required=True)

    parser_encrypt = subparsers.add_parser('encrypt', help='encrypt a plaintext firmware file')
    parser_encrypt.add_argument(
        'fw_plaintext', type=argparse.FileType('rb'),
        help='path to read the plaintext firmware file from'
    )
    parser_encrypt.add_argument(
        'fw_encrypted', type=argparse.FileType('wb'),
        help='path to write the encrypted firmware file to'
    )
    parser_encrypt.set_defaults(mode_func=do_encrypt)

    parser_decrypt = subparsers.add_parser('decrypt', help='decrypt an encrypted firmware file')
    parser_decrypt.add_argument(
        'fw_encrypted', type=argparse.FileType('rb'),
        help='path to read the encrypted firmware file from'
    )
    parser_decrypt.add_argument(
        'fw_plaintext', type=argparse.FileType('wb'),
        help='path to write the plaintext firmware file to'
    )
    parser_decrypt.set_defaults(mode_func=do_decrypt)

    args = parser.parse_args()

    try:
        key = bytes.fromhex(args.key)
        assert len(key) == 256 // 8
    except:
        print('error: could not parse provided key as a 256-bit hexidecimal number')
        return

    cipher = AES.new(key, AES.MODE_ECB)
    args.mode_func(cipher, args)

if __name__ == '__main__':
    main()
