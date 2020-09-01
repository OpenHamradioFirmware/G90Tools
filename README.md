# Tools and guides for analyzing Xiegu G90 firmware

This repository contains tools and guides for working with the firmware for the Xiegu G90 HF radio.

## Getting started

Please check out the [wiki](https://github.com/OpenHamradioFirmware/G90Tools/wiki)!

## Hardware architecture

The Xiegu G90 is built with a detachable display unit and a main unit.

Main unit:
- STM32F429ZGT6

Display unit:
- STM32F103RCT6

## Firmware key extraction

The bootloader seems to be very similar in both units. It is able to read an encrypted firmware over UART, then decrypt and write it to the flash.

The firmware is encrypted with is AES256 ECB.

> :warning: The microcontroller has flash readout protection enabled, which means that if you try to disable it, the flash will be erased and your unit will be bricked (unless you can program a bootloader that you have recovered before).

The key can be extracted with the following method:
- Connect an SWD debugger (ST-Link, CMSIS-DAP, J-Link etc).
- Reset the device without attaching the debugger.
- Load a firmware over UART, e.g. using g90updatefw: 
```
# Use any official firmware
FIRMWARE=G90_MainUnit_FW_V1.74final.xgf

# Use the appropriate tty for your system
TTYUSB=/dev/ttyUSB0

g90updatefw $FIRMWARE $TTYUSB
```
- While the upload is running, attach openocd and dump the ram: 
```
# Use the appropriate interface that matches your SWD debugger
#INTERFACE=cmsis-dap.cfg
#INTERFACE=stlink.cfg

openocd -f interface/$INTERFACE -f target/stm32f1x.cfg -c "init; dump_image ramdump.bin 0x20000000 0x50000"
```
- Run [findaes](https://sourceforge.net/projects/findaes/) to find the key.
```
# Download https://sourceforge.net/projects/findaes/files/latest/download
unzip findaes-1.2.zip
cd findaes-1.2
make
./findaes ramdump.bin
```

To encrypt and decrypt firmware, see [encryption.py](encryption/encryption.py).

## Bootloader extraction

To extract the bootloader firmware:
- Build and flash the extract_bl firmware:
```
cd extract_bl
make KEY=... TTYUSB=/dev/ttyUSB0 flash-encrypted
```
- Log the uart output to a file: `cat /dev/ttyUSB0 > bl.hex`
- Power cycle the device.
- Wait for the dump to complete.
- Convert hex to bin: `xxd -g 1 -r < bl.hex > bl.bin`

Alternatively, an already encrypted binary is included and can be flashed to the target directly to simplify things. If going this route, simply run `make TTYUSB=/dev/ttyUSB0 flash-encrypted-prebuilt` from the `extract_bl` directory. Run the steps above to extract the bootloader binary. Then the key can then be recovered from the dump like so: `dd if=bl.bin skip=7496 bs=1 count=32 2> /dev/null > key.bin`.

## External tools

- [DaleFarnsworth/g90updatefw](https://github.com/DaleFarnsworth/g90updatefw)

## Disclaimer

> :warning: Warning :warning:

There is no warranty provided. Any damage caused by using any of these tools is your own responsibility.

## License

TBD.
