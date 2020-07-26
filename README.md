# Tools and guides for analyzing Xiegu G90 firmware

This repository contains tools and guides for working with the firmware for the Xiegu G90 HF radio.

## Hardware architecture

The Xiegu G90 is built with a detachable display unit and a main unit.

Main unit:
- STM32F429ZGT6

Display unit:
- STM32F103RCT6

## Bootloader

The bootloader seems to be very similar in both units. It is able to read an encrypted firmware over UART, then decrypt and write it to the flash.

The firmware is encrypted with is AES256 ECB.

The key can be extracted with the following method:
- Connect an SWD debugger (ST-Link, CMSIS-DAP, J-Link etc).
- Reset the device without attaching the debugger.
- Load a firmware over UART
- While the upload is running, attach openocd (e.g. `openocd -f interface/cmsis-dap.cfg -f target/stm32f1x.cfg -c "init;"`)
- Dump the ram
- Run [findaes](https://sourceforge.net/projects/findaes/) on the dump to find the key

To encrypt and decrypt firmware, see encryption/decrypt.py and encryption/encrypt.py.

To extract the bootloader firmware:
- Build and flash the extract_bl firmware:
```
cd extract_bl
make KEY=... TTYUSB=/dev/ttyUSB0 flash-encrypted
# Power-cycle the device
```
- Log the uart output to a file

## External tools

- [DaleFarnsworth/g90updatefw](https://github.com/DaleFarnsworth/g90updatefw)

## License

TBD.
