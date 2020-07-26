
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>


static void initUsart(void) {
	// Enable peripheral clock
	rcc_periph_clock_enable(RCC_USART3);

	// Setup USART3 on PB10
	gpio_set_mode(GPIOB, GPIO_MODE_OUTPUT_2_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO10);

	// Handle the baud settings
	usart_set_mode(USART3, USART_MODE_TX);
	usart_set_baudrate(USART3, 115200);
	usart_set_databits(USART3, 8);
	usart_set_parity(USART3, USART_PARITY_NONE);
	usart_set_stopbits(USART3, USART_STOPBITS_1);
	usart_set_flow_control(USART3, USART_FLOWCONTROL_NONE);
	usart_enable(USART3);
}

size_t _write(int fd, char *ptr, int len)
{
	int i = 0;

	if (fd > 2) {
		return -1;
	}

	while (*ptr && (i < len)) {
		usart_send_blocking(USART3, *ptr);
		i++;
		ptr++;
	}
	return i;
}

int main(void)
{
	// There is an 8MHz external clock
	rcc_clock_setup_in_hse_8mhz_out_72mhz();
	uint8_t *flash = (uint8_t *) 0x08000000;

	initUsart();

	while (true) {
		for (uint32_t i = 0; i < (1 << 18); i++) {
			__asm__("nop");
		}

		for (uint32_t i = 0; i < 0x4000; i++) {
			uint8_t c = flash[i];

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
}
