
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>

/*
	Pinout for the screen KD018QQTBN009
	Screen uses a ST7735S controller
	Resolution: 128 x 160, 16b colors

	FLEX   MCU      Function     Peripheral
	31     17 PA3   WR(SPI-RS)
	29     20 PA4   Reset        SPI1_NSS 
	28     21 PA5   Clock        SPI1_SCK
	26     23 PA7   Serial in    D0 (32R) SPI1_MOSI
	2-3    62 PB9   Backlight
*/

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

void initGPIO(void)
{
	rcc_periph_clock_enable(RCC_GPIOA);
	rcc_periph_clock_enable(RCC_GPIOB);

	gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_10_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO3);
	gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_10_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO4);
	gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_10_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO5);
	gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_10_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO7);

	gpio_set_mode(GPIOB, GPIO_MODE_OUTPUT_10_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO9);

	gpio_set(GPIOA, GPIO3);
	gpio_set(GPIOB, GPIO9);

	gpio_clear(GPIOA, GPIO4);
	gpio_clear(GPIOA, GPIO5);
	gpio_clear(GPIOA, GPIO7);
}

int main(void)
{
	// There is an 8MHz external clock
	rcc_clock_setup_in_hse_8mhz_out_72mhz();

	initUsart();
	initGPIO();

	for (uint32_t i = 0; i < (1 << 18); i++) {
		__asm__("nop");
	}

	printf("Boot!\n");

	while (true) {
		__asm__("nop");
	}
}
