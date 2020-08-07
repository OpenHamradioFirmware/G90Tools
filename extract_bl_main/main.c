
#include <stdint.h>
#include <string.h>

// Do a ramdump easily assuming buf ended up @0x20000000 (too lazy to write a proper linker script)
// export INTERFACE=cmsis-dap.cfg
// export INTERFACE=stlink.cfg
// openocd -f interface/$INTERFACE -f target/stm32f4x.cfg -c "init; dump_image mainunit_bl.bin 0x20000000 0x4000; shutdown"
uint8_t buf[1024*16] __attribute__((aligned (1024)));

int main(void)
{
	uint8_t *flash = (uint8_t *) 0x08000000;
	memcpy(buf, flash, sizeof(buf));

	while (1) {
		__asm__("NOP");
	}
}
