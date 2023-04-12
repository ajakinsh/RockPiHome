/* 
 * "Small Hello World" example. 
 * 
 * This example prints 'Hello from Nios II' to the STDOUT stream. It runs on
 * the Nios II 'standard', 'full_featured', 'fast', and 'low_cost' example 
 * designs. It requires a STDOUT  device in your system's hardware. 
 *
 * The purpose of this example is to demonstrate the smallest possible Hello 
 * World application, using the Nios II HAL library.  The memory footprint
 * of this hosted application is ~332 bytes by default using the standard 
 * reference design.  For a more fully featured Hello World application
 * example, see the example titled "Hello World".
 *
 * The memory footprint of this example has been reduced by making the
 * following changes to the normal "Hello World" example.
 * Check in the Nios II Software Developers Manual for a more complete 
 * description.
 * 
 * In the SW Application project (small_hello_world):
 *
 *  - In the C/C++ Build page
 * 
 *    - Set the Optimization Level to -Os
 * 
 * In System Library project (small_hello_world_syslib):
 *  - In the C/C++ Build page
 * 
 *    - Set the Optimization Level to -Os
 * 
 *    - Define the preprocessor option ALT_NO_INSTRUCTION_EMULATION 
 *      This removes software exception handling, which means that you cannot 
 *      run code compiled for Nios II cpu with a hardware multiplier on a core 
 *      without a the multiply unit. Check the Nios II Software Developers 
 *      Manual for more details.
 *
 *  - In the System Library page:
 *    - Set Periodic system timer and Timestamp timer to none
 *      This prevents the automatic inclusion of the timer driver.
 *
 *    - Set Max file descriptors to 4
 *      This reduces the size of the file handle pool.
 *
 *    - Check Main function does not exit
 *    - Uncheck Clean exit (flush buffers)
 *      This removes the unneeded call to exit when main returns, since it
 *      won't.
 *
 *    - Check Don't use C++
 *      This builds without the C++ support code.
 *
 *    - Check Small C library
 *      This uses a reduced functionality C library, which lacks  
 *      support for buffering, file IO, floating point and getch(), etc. 
 *      Check the Nios II Software Developers Manual for a complete list.
 *
 *    - Check Reduced device drivers
 *      This uses reduced functionality drivers if they're available. For the
 *      standard design this means you get polled UART and JTAG UART drivers,
 *      no support for the LCD driver and you lose the ability to program 
 *      CFI compliant flash devices.
 *
 *    - Check Access device drivers directly
 *      This bypasses the device file system to access device drivers directly.
 *      This eliminates the space required for the device file system services.
 *      It also provides a HAL version of libc services that access the drivers
 *      directly, further reducing space. Only a limited number of libc
 *      functions are available in this configuration.
 *
 *    - Use ALT versions of stdio routines:
 *
 *           Function                  Description
 *        ===============  =====================================
 *        alt_printf       Only supports %s, %x, and %c ( < 1 Kbyte)
 *        alt_putstr       Smaller overhead than puts with direct drivers
 *                         Note this function doesn't add a newline.
 *        alt_putchar      Smaller overhead than putchar with direct drivers
 *        alt_getchar      Smaller overhead than getchar with direct drivers
 *
 */

#include "sys/alt_stdio.h"
#include "system.h"
#include "altera_avalon_pio_regs.h"

void delay(void) {
	for(int j = 0; j <=1000; j++){
		for(int i = 0; i <=1000; i++);
	}
}

int read(){
	return IORD_ALTERA_AVALON_PIO_DATA(PIO_IN_BASE);
}

int main()
{ 
	/* Event loop never exits. */
	int value;
	printf("begin\n");
	while (1) {
		IOWR_ALTERA_AVALON_PIO_DATA(PIO_OUT_BASE, 0b0001);
		value = read();
		for(int j = 0; j <=1000; j++){  // extra software delay loops
			for(int i = 0; i <=1000; i++);
		}

		if(value) {
			switch (value) {
			case 0b0001:
				alt_putstr("D\n");
				break;
			case 0b0010:
				alt_putstr("#\n");
				break;
			case 0b0100:
				alt_putstr("0\n");
				break;
			case 0b1000:
				alt_putstr("*\n");
				break;
			default:
				break;
			}
			while(read() == value);
			delay();
		}

		IOWR_ALTERA_AVALON_PIO_DATA(PIO_OUT_BASE, 0b0010);
		value = read();
		delay();
		if(value) {
			switch (value) {
			case 0b0001:
				alt_putstr("C\n");
				break;
			case 0b0010:
				alt_putstr("9\n");
				break;
			case 0b0100:
				alt_putstr("8\n");
				break;
			case 0b1000:
				alt_putstr("7\n");
				break;
			default:
				break;
			}
			while(read() == value);
			delay();
		}

		IOWR_ALTERA_AVALON_PIO_DATA(PIO_OUT_BASE, 0b0100);
		value = read();
		delay();
		if(value) {
			delay();

			switch (value) {
			case 0b0001:
				alt_putstr("B\n");
				break;
			case 0b0010:
				alt_putstr("6\n");
				break;
			case 0b0100:
				alt_putstr("5\n");
				break;
			case 0b1000:
				alt_putstr("4\n");
				break;
			default:
				break;
			}
			while(read() == value);
			delay();
		}

		IOWR_ALTERA_AVALON_PIO_DATA(PIO_OUT_BASE, 0b1000);
		value = read();
		delay();
		if(value) {
			switch (value) {
			case 0b0001:
				alt_putstr("A\n");
				break;
			case 0b0010:
				alt_putstr("3\n");
				break;
			case 0b0100:
				alt_putstr("2\n");
				break;
			case 0b1000:
				alt_putstr("1\n");
				break;
			default:
				break;
			}
			while(read() == value);
			delay();
		}
	}
	return 0;
}


