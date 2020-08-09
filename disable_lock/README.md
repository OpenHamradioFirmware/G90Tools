# Patch flash locking in bootloader

The bootloader contains code that will enable readout protection (lock level 1) after it has finished flashing the application code.

This patch will replace this call with NOPs.