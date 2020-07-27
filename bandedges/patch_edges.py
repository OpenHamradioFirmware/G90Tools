import os
import sys
import json
import struct

def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <decrypted dispunit firmware to patch> <channel_file.json>')
        print(f'    note: only use on firmware 1.74')
        print(f'    note: exactly 10 channels must be defined')
        return

    decrypted_firmware = sys.argv[1]

    with open(sys.argv[2], "r") as channel_file:
        channels = json.loads(channel_file.read())
    if len(channels) != 10:
        raise ValueError("Must have 10 channels")

    channel_data = b''
    for channel in channels:
        print(f'Low: {channel["low"]} High: {channel["high"]} Enabled: {channel["enabled"]}')
        channel_struct = struct.pack('iii', int(channel['low'] * 1000000), int(channel['high'] * 1000000), int(channel['enabled']))
        channel_data += channel_struct
    
    with open(decrypted_firmware, 'r+b') as f:
        f.seek(0x20120, os.SEEK_SET)
        f.write(bytes(channel_data))

    print('done: band edges patched')

if __name__ == '__main__':
    main()
