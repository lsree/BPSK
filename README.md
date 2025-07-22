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

### Relevant SDR specs for USRP B200/B210
* Clock PPM +/- 2 PPM -> @915Mhz the frequency can deviate +/- 1830 Hz


### Digital Specifications
* Baud Rate: 19.2 Kbd / 19.2k samples/symbol

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

## Useful Links/Articles
### Frequency Correction
* Frequency Locked Loop
  * https://dsp.stackexchange.com/questions/42239/how-does-this-fll-work
  * [Paper on the Subject](Freq_Locked_Loop-Asilomar_2012_BE_PLL.pdf)
* Angle-based coarse frequency correction
   * https://openofdm.readthedocs.io/en/latest/freq_offset.html
   *

### Phase locked Loop
    * Tuning loop filter https://dsp.stackexchange.com/questions/64108/designing-a-pi-filter-for-a-costas-loop

## Notes for Debugging
### Timing Recovery
After timing recovery the IQ plot should look like a clean-ish circle

The following Timing Recovery Methods are available. They are broken into 2 categories: PLL-based feedback systems, and correlation based feed-forward systems. 

#### PLL Timing Error Detctors
1. Maximum Liklihood Detector
1. Early-Late
    * A special case of the generic maximum liklihood detector where there are 2 SPS
    * Compares the the previous symbol and next symbol and multiplies it by the value of the  current symbol and tries to drive that value to zero
    ``` interp_signal[i] * (interp_signal[i+dt] - interp_signal[i-dt]) ```
1. Gardner/Zero Crossing
    * Also a special case of the generic maximum liklihood detector where there are 2 SPS
    * Does not require future samples, only needs the current and previous symbol.
    * Works by comparing the previous symbol with the current symbol and multiplying it by a sample located between them
    ```phase_offset = interp_signal[i-dt] * (interp_signal[i] - interp_signal[i-interp_sps])```
    

1. Mueller & Meuller


#### Relevant Articles/Videos
* [GRCon17 Lecture on Symbol Clock Recovery Block](https://youtu.be/uMEfx_l5Oxk)
* [wirelesspi.com](wirelesspi.com)
* [fred harris slides on polyphase timing sync](https://s3.amazonaws.com/embeddedrelated/user/124841/synchronization_qualcomm_2018_4_11449.pdf)
* [Paper on PLL TEDs](https://s3.amazonaws.com/embeddedrelated/user/6420/part%20of%20timing%20error%20detectors_92419.pdf)


### Fine Frequency Correction (PLL)
* The PLL should turn the event circle into a cluster of points
* The PLL requires the preamble to syncronize and lock onto the frequency
* In BPSK the Q component of the signal should be diven to 0. If it is beginning to be unstable again, it could mean that the timing syncronization is off or that the PLL is tuned too aggressively. 
