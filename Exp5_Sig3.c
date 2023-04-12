/*
 * File:   Exp5_Sig3.c
 * Author: ajakinsh
 *
 * Created on November 16, 2022, 8:04 PM
 */

// PIC16F1769 Configuration Bit Settings

// 'C' source line config statements

// CONFIG1
#pragma config FOSC = INTOSC    // Oscillator Selection Bits (INTOSC oscillator: I/O function on CLKIN pin)
#pragma config WDTE = OFF       // Watchdog Timer Enable (WDT disabled)
#pragma config PWRTE = OFF      // Power-up Timer Enable (PWRT disabled)
#pragma config MCLRE = ON       // MCLR Pin Function Select (MCLR/VPP pin function is MCLR)
#pragma config CP = OFF         // Flash Program Memory Code Protection (Program memory code protection is disabled)
#pragma config BOREN = ON       // Brown-out Reset Enable (Brown-out Reset enabled)
#pragma config CLKOUTEN = OFF   // Clock Out Enable (CLKOUT function is disabled. I/O or oscillator function on the CLKOUT pin)
#pragma config IESO = ON        // Internal/External Switchover Mode (Internal/External Switchover Mode is enabled)
#pragma config FCMEN = ON       // Fail-Safe Clock Monitor Enable (Fail-Safe Clock Monitor is enabled)

// CONFIG2
#pragma config WRT = OFF        // Flash Memory Self-Write Protection (Write protection off)
#pragma config PPS1WAY = ON     // Peripheral Pin Select one-way control (The PPSLOCK bit cannot be cleared once it is set by software)
#pragma config ZCD = OFF        // Zero-cross detect disable (Zero-cross detect circuit is disabled at POR)
#pragma config PLLEN = ON       // Phase Lock Loop enable (4x PLL is always enabled)
#pragma config STVREN = ON      // Stack Overflow/Underflow Reset Enable (Stack Overflow or Underflow will cause a Reset)
#pragma config BORV = LO        // Brown-out Reset Voltage Selection (Brown-out Reset Voltage (Vbor), low trip point selected.)
#pragma config LPBOR = OFF      // Low-Power Brown Out Reset (Low-Power BOR is disabled)
#pragma config LVP = ON         // Low-Voltage Programming Enable (Low-voltage programming enabled)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>

void timer2(void) {      
    INTCONbits.GIE = 1; // enable global interrupts
    INTCONbits.PEIE = 1;
    T2CLKCON = 0b00000001; // 2 MHz / 4 = 500kHz
    T2CON = 0b11111111; // (500 kHz / 128) = 3906.25 Hz 
    T2PR = 244; // 3906.25 Hz / 16 = 244 Hz
    
    PIR1bits.TMR2IF = 0;
    PIE1bits.TMR2IE = 1;
}

void setup_spi_main(void){
    TRISBbits.TRISB6 = 0; // RB6 SPI SCLK output
    TRISBbits.TRISB4 = 0; // RB4 SPI MOSI output
    TRISCbits.TRISC3 = 1; // Make SPI MISO input
    TRISCbits.TRISC4 = 0; // Make SPI SS output

    ANSELCbits.ANSC3 = 0; // Make SPI MISO digital
    
    SSPDATPPS = 0b00010011; // PPS input for MISO
    RB6PPS = 0b00010010; // PPS output for SCLK (SCK)
    RB4PPS = 0b00010100; // PPS output for MOSI (SDO)
    
    SSP1CON1 = 0b00100001; // Enable, idle state low clock polarity, SPI main, Fosc/16 clock
    SSP1STAT = 0b00000000;// Choose sample mode and edge mode
    PIR1bits.SSP1IF = 0; // Clear SPI flag
}

int transfer_spi_main(int t) {
    int r;
    SSP1BUF = t;
    while (!PIR1bits.SSP1IF);
    PIR1bits.SSP1IF = 0;
    r = SSP1BUF;
    return r;
}

void main(void) {
    OSCCON = 0b01100000; // 2 MHz oscillator
    
    timer2();
    setup_spi_main();
    
    int write_data = 0;
    
    while(1) {   
        if (PIR1bits.TMR2IF == 1) {
            LATCbits.LATC4 = 0; // SS go low before transfer
            transfer_spi_main(write_data);
            if(write_data == 255){
                write_data = 0;
            }
            write_data += 1;
            PIR1bits.TMR2IF = 0;
            LATCbits.LATC4 = 1; // SS high after
        }
    }
    return;
}
