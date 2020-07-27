
PREFIX ?= arm-none-eabi-
CC = $(PREFIX)gcc
OBJCOPY = $(PREFIX)objcopy

OPENOCD ?= openocd
LIBOPENCM3_ROOT = ../lib/libopencm3

FP_FLAGS = -msoft-float
ARCH_FLAGS = -mcpu=cortex-m3 -mthumb $(FP_FLAGS)

LD_SCRIPT = stm32f103xc_app.ld

LDFLAGS = -L$(LIBOPENCM3_ROOT)/lib
LDFLAGS += --static -nostartfiles
LDFLAGS += -T$(LD_SCRIPT)

CFLAGS = $(ARCH_FLAGS)
CFLAGS += -std=c11 -g3 -O0
CFLAGS += -I$(LIBOPENCM3_ROOT)/include
CFLAGS += -fno-common -ffunction-sections -fdata-sections
CFLAGS += -DSTM32F1

LDLIBS = -Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group
LDLIBS += -lopencm3_stm32f1

FIRMWARE_ELF = firmware.elf
FIRMWARE_BIN = firmware.bin
FIRMWARE_HEX = firmware.hex
FIRMWARE_ENC = firmware.enc

all: $(FIRMWARE_ELF) $(FIRMWARE_BIN) $(FIRMWARE_HEX)

$(FIRMWARE_ELF): main.c $(LIBOPENCM3_ROOT)/lib/libopencm3_stm32f1.a
	$(CC) $(CFLAGS) $(LDFLAGS) main.c $(LDLIBS) -o firmware.elf

$(LIBOPENCM3_ROOT)/Makefile:
	git submodule update --init

$(LIBOPENCM3_ROOT)/lib/libopencm3_%.a: $(LIBOPENCM3_ROOT)/Makefile
	$(MAKE) -C $(LIBOPENCM3_ROOT) TARGETS=stm32/f1

$(FIRMWARE_BIN): $(FIRMWARE_ELF)
	$(OBJCOPY) -O binary $< $@

$(FIRMWARE_HEX): $(FIRMWARE_ELF)
	$(OBJCOPY) -O ihex $< $@

$(FIRMWARE_ENC): $(FIRMWARE_BIN)
	python ../encryption/encryption.py $(KEY) encrypt $(FIRMWARE_BIN) $(FIRMWARE_ENC)

flash-encrypted: $(FIRMWARE_ENC)
	g90updatefw $(FIRMWARE_ENC) $(TTYUSB)

flash: $(FIRMWARE_ELF)
	$(OPENOCD) -f interface/jlink.cfg -c "transport select swd" -f target/stm32f1x.cfg -c "program $(FIRMWARE_ELF) verify reset exit"

clean:
	$(RM) $(FIRMWARE_ELF) $(FIRMWARE_BIN) $(FIRMWARE_HEX) $(FIRMWARE_ENC)

distclean: clean
	$(MAKE) -C $(LIBOPENCM3_ROOT) clean

.PHONY: all flash clean distclean
