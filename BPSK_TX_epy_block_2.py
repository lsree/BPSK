"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='MSG2U8_Vector',   # will show up in GRC
            in_sig= None,
            out_sig= None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_in(pmt.intern('PDU_in'))
        self.message_port_register_out(pmt.intern('PDU_out'))
        self.set_msg_handler(pmt.intern('PDU_in'),self.handle_msg)
        
    def handle_msg(self, msg):
        #Get msg
        payload = pmt.to_python(msg)
        
        #print(f"Payload: {payload}\n Payload type: {type(payload)}")
        
        payload = np.fromstring(payload[1], dtype=np.uint8)
        print(f"Payload: {payload}")

     
        #Create PMT u8vector
        pmt_out = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(payload), payload))
        self.message_port_pub(pmt.intern('PDU_out'), pmt_out)
