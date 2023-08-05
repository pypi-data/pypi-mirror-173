# --------------------
## holds the configuration information for the test harness
class Cfg:
    # --------------------
    ## constructor
    def __init__(self):
        ## the IP address to use for socket comms
        self.ip_address = '127.0.0.1'
        ## the IP port to use for socket comms
        self.ip_port = 5001
        ## whether logging is verbose or not
        self.verbose = True
