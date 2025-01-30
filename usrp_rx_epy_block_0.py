"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from gnuradio import filter
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, threshold_db=-65, alpha=.00001, burst_tag_name = "rx_sob"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Burst Detect & Squelch',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.threshold = 10**(threshold_db/10)
        self.alpha = alpha
        self.prev_filt = 0  #Save previous value of the filter
        self.tag_key = pmt.intern(burst_tag_name)
        self.burst_occurring = False #Holds state on if we're in a burst or not

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        input_samp = input_items[0]
        mag2 = input_samp * np.conj(input_samp)
        
        output = np.zeros(len(input_samp), dtype=complex)
        # Apply Filter
        for i in range(0, len(mag2)):
            self.prev_filt = self.alpha*mag2[i] + (1-self.alpha)*self.prev_filt 
            
            if (self.prev_filt >= self.threshold):
                if (not self.burst_occurring):  #Add tag if we're not in a burst
                    self.add_item_tag(0, self.nitems_written(0) + i, self.tag_key, pmt.PMT_T)
                    self.burst_occurring = True
                output[i] = input_samp[i]
            else:
                self.burst_occurring = False
                
        output_items[0][:] = output
        return len(output_items[0])
