# --------------------
class Cfg:
    # --------------------
    def __init__(self):
        ## the IP address to use for socket comms
        self.ip_address = '127.0.0.1'
        ## the IP port to use for socket comms
        self.ip_port = 5001
        ## whether logging is verbose or not
        self.verbose = False
        ## callback for server
        self.callback = None

    # --------------------
    def init(self):
        pass
