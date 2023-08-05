import json
import time

from socket_oneline import OnelineClient

from .. import services


# --------------------
## sample Client that wraps the OnelineClient
class Client:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to Oneline Client
        self._client = OnelineClient()

    # --------------------
    ## initialize the OnelineClient and connect to the server
    #
    # @return None
    def init(self):
        services.logger.info('client      : started')

        self._client.ip_address = services.cfg.ip_address
        self._client.ip_port = services.cfg.ip_port
        self._client.logger = services.logger
        self._client.verbose = False
        if not self._client.init():
            services.logger.info('ERR failed to set params')
            return

        self._client.connect()
        # TODO replace with wait_until... with timeout
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._client is not None:
            self._client.disconnect()
            self._client = None

    # --------------------
    ## ping the Server
    #
    # @return the response (should be 'pong')
    def is_connected(self):
        # no json, this is a builtin command to OnelineClient
        rsp = self.send_recv('ping')
        return rsp == 'pong'

    # --------------------
    ## get screen content
    #
    # @return the response
    def get_screen(self):
        cmd = {
            'cmd': 'get_screen'
        }
        screen = self.send_recv(json.dumps(cmd))
        return screen

    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x  the x value in screen coordinates
    # @param y  the y value in screen coordinates
    # @return the response
    def click_left(self, x, y):
        cmd = {
            'cmd': 'click_left',
            'x': x,
            'y': y,
        }
        ack_nak = self.send_recv(json.dumps(cmd))
        return ack_nak

    # --------------------
    ## select menu in the given menu path
    #
    # @param menu_path  a list of indicies indicating the menu path
    # @return the response
    def menu_click(self, menu_path):
        cmd = {
            'cmd': 'menu_click',
            'menu_path': menu_path,
        }
        ack_nak = self.send_recv(json.dumps(cmd))
        return ack_nak

    # --------------------
    ## send a command to the Server, wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd):
        self._send(cmd)
        rsp = self._recv()
        return rsp

    # === Private

    # --------------------
    ## send a disconnect ocmmand to the Server
    #
    # @return None
    def _disconnect(self):
        # no json, this is a builtin command to OnelineClient
        self._send('disconnect')

    # --------------------
    ## send a shutdown command to the Server
    #
    # @return None
    def _shutdown(self):
        # no json, this is a builtin command to OnelineClient
        self._send('shutdown')

    # --------------------
    ## send a command to the Server
    #
    # @param cmd  the command to send
    # @return None
    def _send(self, cmd):
        services.logger.info(f'client      : tx: {cmd}')
        self._client.send(cmd)

    # --------------------
    ## wait for a response from the Server
    #
    # @return the response
    def _recv(self):
        rsp = self._client.recv()
        # uncomment for debugging
        # services.logger.info(f'client      : rx: {rsp}')
        return rsp
