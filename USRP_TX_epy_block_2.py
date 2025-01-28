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

    def __init__(self, preamble_len=12, syncword="1110010"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Packetize',   # will show up in GRC
            in_sig= None,
            out_sig= None
        )
        
        #Store Variables
        self.preamble = np.array(int((preamble_len+1)/2)*[1,0], dtype=np.uint8)[:preamble_len]
        self.syncword = np.array(list(syncword), dtype=np.uint8)
        
        #Make values are binary
        if np.any(self.syncword > 1):
        	print(np.any(self.syncword > 1))
        	raise ValueError("Inavlid Syncword")
        
        # Register port and handler
        self.message_port_register_in(pmt.intern('MSG_In'))
        self.message_port_register_out(pmt.intern('Packet'))
        self.set_msg_handler(pmt.intern('MSG_In'), self.handle_msg)
        
        
    def handle_msg(self, msg):
        #Get msg
        payload = pmt.to_python(msg)
        
        print(f"Syncword Len {len(self.syncword)} syncword: {self.syncword}")
        print(f"Payload: {payload}\n Payload type: {type(payload)}")
        
        payload = np.fromstring(payload[1], dtype=np.uint8)
        payload_len = np.array([len(payload)], dtype=np.uint8)
        print(f"payload_len {payload_len}")
        
        print(f"payload_len + payload: {np.unpackbits(np.concatenate((payload_len, payload)), bitorder='big')}")
        packet = np.concatenate((self.preamble, self.syncword, np.unpackbits(np.concatenate((payload_len, payload)), bitorder='big')))
        print(f"packet: {packet}")
     
        #Create PMT u8vector
        pmt_out = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet))
        self.message_port_pub(pmt.intern('Packet'), pmt_out)
