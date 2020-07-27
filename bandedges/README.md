Updates the bandedges for firmware 1.74 only.

```
'Usage: patch_edges.py <decrypted dispunit firmware to patch> <channel_file.json>
```
Remember to encrypt the firmware after running this with `encryption/encryption.py`

JSON syntax is as follows (must have exactly 10 channels):

```
[
    {"low":1.8, "high": 1.875, "enabled": true},
    {"low":3.5, "high": 3.7, "enabled": true},
    {"low":3.776, "high": 3.8, "enabled": true},
    {"low":7, "high": 7.3, "enabled": true},
    {"low":10.1, "high": 10.15, "enabled": true},
    {"low":14, "high": 14.35, "enabled": true},
    {"low":18.068, "high": 18.168, "enabled": true},
    {"low":21, "high": 21.45, "enabled": true},
    {"low":24.89, "high": 24.99, "enabled": true},
    {"low":28, "high": 29.7, "enabled": true}
]
```
