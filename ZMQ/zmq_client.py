'''
This file is supposed to handle the user interface b/t the user & gnuradio. It sends data that the user
inputs to the terminal over a REP-REQ ZMQ socket. It receives incoming data from gnuradio in a push-pull configuration

It has 2x threads: one for handling user input, and one for displaying gnuradio output.
'''

import signal
import pmt
import zmq
import threading
import time

class userInputHandler:
    def __init__(self, addr, zmq_context):
        
        #Create ZMQ Socket
        self.zmq_context = zmq_context
        self.zmq_sock = self.zmq_context.socket(zmq.REP)  #Use a REQ-REP socket
        self.zmq_sock.bind(addr)

    def teardown(self):
        ''' Used to teardown the zmq context & connects'''
        self.zmq_sock.close()
 
    def handler(self):
        while True:
            rx_data = self.zmq_sock.recv()                                # this is the non-standard "kludge"
            print(f"RX Data: {rx_data}")
            usr_input = input(">>")
            self.zmq_sock.send(pmt.serialize_str(pmt.to_pmt(usr_input)))       # send on the 'reply' socket
        
class Receiver:
    def __init__(self, addr, zmq_context):
        self.zmq_context = zmq_context
        self.zmq_sock = self.zmq_context.socket(zmq.PULL)  #Use a REQ-REP socket
        self.zmq_sock.connect(addr)

    def teardown(self):
        self.zmq_sock.close()
    
    def handler(self):
        while True:
            rx_data = self.zmq_sock.recv()
            print(rx_data)



    
# create socket
_PROTOCOL = "tcp://"
_SERVER = "127.0.0.1"          # localhost
_PORT = ":50123"
_ADDR = _PROTOCOL + _SERVER + _PORT

RX_ADDR = "tcp://127.0.0.1:50124"
if __name__ == "__main__":
    zmq_context = zmq.Context()
    userHandler = userInputHandler(_ADDR, zmq_context)
    print ("zmqREP connecting to:", _ADDR)

    rx = Receiver(RX_ADDR, zmq_context)

    rx_thread = threading.Thread(target=rx.handler)
    rx_thread.start()
    try:
        userHandler.handler()
    except KeyboardInterrupt:
        # clean up
        rx_thread.join()
        rx.teardown()
        userHandler.teardown()
        zmq_context.term()