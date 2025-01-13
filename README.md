# BPSK

## Specifications
* Transmit at a distance of at least 30 meters
* 256 byte max data transmission
* BPSK Modulated
* Use HackRFOne (hardware rev r1-r8)
* Use the 915 Mhz band

## Derived Specifications
### Range
Max Transmi Power:
* RF Amplifier: 0 or ~11 -> 12.5 dB @ 1 Ghz
* LNA Amplifier 0 to 40 dB

Max theoretical per documentation: 5 to 15 dBm

#### Link Budget Analysis:
Prx = Ptx + Gtx - Ltx - -Lfs - Lm + Grx - Lrx
* Ptx = 5 dBm   *Transmitted Power - Using lower estimate provided by hackrf*   
* Gtx = 1.2 dBi *Tx antenna gain*
* Ltx = 0 dB    *Transmitter losses - approximate to 0*
* Lfs = 20*log(d) + 31.67        *Path loss 20*log(4*pi*d*f/c)*
* Lm = 0 dB     *Misc losses*
* Grx = 1.2dBi  *Rx antenna gain*
* Lrx = 0 dB    *Reciver losses - approximate to 0*

Prx = 5 + 1.2 - 0 - 20*log(d) - 31.67 - 0 + 1.2 - 0
Prx = -24.27 - 20*log(d)
For d = 30m -> Prx = -53.81

#### Noise Calculation: 
Use kTB approach
* K = -228.6 dBW/K/Hz (+30 for dBm)
* T = 295 deg. K (Room temp) -> 24.70 dBK
* B = 1e6 (1Mhz) -> 60 dBHz
Pnoise (dBm) = (-228.6 + 30) + 24.70 + 60
Pnoise (dBm) = -113.9

### SNR
SNR should be greater than 10dB (as a rule of thumb)
SNR @ 30m = -53.81 - (-113.9) = 60.09 

Solve for distance:
10 < -24.27 - 20*log(d) - (-113.9) = 60.09 
d < 1000 meters

*HackRF cannot receive more than -5 dBm (although it can rx 10dBm w/ rx amp disabled)* 

### Bandwidth
* Per documentation use a sample rate >= 8Mhz
* Baseband LPF exists in incrememnts of 1.75, 2.5, 3.5, 5, 5.5, ..., 14, 15, 20, 24, 28 MHz


### Digital Specifications
* sps = 8
* Fs: 8Mhz
* symbol/bit rate = 1Mbps
* Bandwidth = 1Mhz

### Packet Structure
| Byte 0          | Byte 1          | Byte 2          | Byte 3          | Byte 4          | Byte N          | Byte N+1          |
| --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- |
| Preamble: 0xAA  | Syncword: 0x39  | Data Length     | Data byte 0     | Data byte 1     | Data byte n     | CRC8            |

## Order of Operations
This section describes how I will create such a system
1. Determine feasablilty/do link budget
1. Create Transmitter
    1. Generate packet formatter
    1. Create a simulated transmitter. Write data to file
    1. Transmit data and be able to receive but not demodulate the signal
        1. Tune transmitter and receiver settings to be able to receive signal
1. Create receiver
    1. Demodulate statically
    1. Create GNUradio flowgraphs to demodulate live
        1. Course frequency correction
        1. Burst detection
        1. Symbol synchronization 
        1. Depacketization
1. Bonus: Modify system to transmit arbitary forms of data (not just ASCII)

## Useful Hackrf Commands:
* ```SoapySDRUtil --probe=driver=hackrf``` - Shows available commands for hackrf
