Encrypts/decrypts `xgf` firmware files.

# Usage
## Decryption
```
# given an encrypted firmware fw_encrypted.xgf, decrypt to fw_plaintext.bin
encryption.py <key in hex> decrypt fw_encrypted.xgf fw_plaintext.bin
```

## Encryption
```
# given a plaintext firmware fw_plaintext.bin, encrypt to fw_encrypted.xgf
encryption.py <key in hex> encrypt fw_plaintext.bin fw_encrypted.xgf
```
