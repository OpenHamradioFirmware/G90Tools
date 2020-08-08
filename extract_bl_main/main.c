
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>

static void clock_setup(void)
{
	rcc_clock_setup_pll(&rcc_hse_8mhz_3v3[RCC_CLOCK_3V3_168MHZ]);

	rcc_periph_clock_enable(RCC_GPIOA);
	rcc_periph_clock_enable(RCC_USART1);
}

static void usart_setup(void)
{
	usart_set_baudrate(USART1, 115200);
	usart_set_databits(USART1, 8);
	usart_set_stopbits(USART1, USART_STOPBITS_1);
	usart_set_mode(USART1, USART_MODE_TX);
	usart_set_parity(USART1, USART_PARITY_NONE);
	usart_set_flow_control(USART1, USART_FLOWCONTROL_NONE);

	usart_enable(USART1);
}

static void gpio_setup(void)
{
	/* Setup GPIO pins for USART1 transmit. */
	gpio_mode_setup(GPIOA, GPIO_MODE_AF, GPIO_PUPD_NONE, GPIO9);

	gpio_mode_setup(GPIOA, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO8);

	/* Setup USART1 TX pin as alternate function. */
	gpio_set_af(GPIOA, GPIO_AF7, GPIO9);
}

size_t _write(int fd, char *ptr, int len)
{
	int i = 0;

	if (fd > 2) {
		return -1;
	}

	while (*ptr && (i < len)) {
		usart_send_blocking(USART1, *ptr);
		i++;
		ptr++;
	}
	return i;
}

int main(void)
{
	uint8_t buf[32];
	int i, j;

	clock_setup();
	gpio_setup();
	usart_setup();

	// Dump only the bootloader
	const uint32_t dump_size = 0x4000;
	uint8_t *flash = (uint8_t *) 0x08000000;

	for (uint32_t i = 0; i < dump_size; i++) {
		uint8_t c = flash[i];

		// Blink the blue led
		if (i % 0x100 == 0) {
			gpio_toggle(GPIOA, GPIO8);
		}

		if (i % 16 == 0) {
			printf("%08X: ", i);
		}

		printf("%02X", c);

		if (i % 16 == 15) {
			printf("\n");
		} else {
			printf(" ");
		}
	}

	while (true) {
		__asm__("nop");
	}
}
