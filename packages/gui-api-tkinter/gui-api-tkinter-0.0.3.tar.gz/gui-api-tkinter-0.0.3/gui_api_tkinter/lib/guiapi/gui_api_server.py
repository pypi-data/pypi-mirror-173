import json
import time

from socket_oneline import OnelineServer

from gui_api_tkinter.lib.guiapi import services


# --------------------
## sample Server that wraps the OnelineServer
class GuiApiServer:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to the Oneline Server
        self._server = OnelineServer()

    # --------------------
    ## initialize
    # Start the OnelineServer
    #
    # @return None
    def init(self):
        services.logger.info('server      : started')

        self._server.callback = self._callback
        self._server.ip_address = services.cfg.ip_address
        self._server.ip_port = services.cfg.ip_port
        self._server.verbose = services.cfg.verbose
        self._server.logger = services.logger

        if not self._server.start():
            services.logger.info('ERR failed to set params')
            return
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._server is not None:
            self._server.term()
            self._server = None

    # --------------------
    ## request shutdown and then wait until the server stops running
    #
    # @return None
    def shutdown(self):
        self.send('shutdown')
        while self._server.is_running:
            time.sleep(0.5)

    # --------------------
    def send_ack(self):
        self.send('ack')

    # --------------------
    def send_nak(self):
        self.send('nak')

    # --------------------
    def send(self, msg):
        self._server.send(msg)

    # --------------------
    ## callback function used by OnelineServer to handle incoming commands
    #
    # @param cmd         the incoming command from the client
    # @param is_invalid  indicates if the command is invalid
    # @return None
    def _callback(self, command, is_invalid):
        # all commands sent here should be json
        cmd = json.loads(command)
        services.logger.info(f'server      : callback: cmd="{cmd["cmd"]}" is_invalid={is_invalid}')
        if is_invalid:
            return

        if cmd['cmd'] == 'get_screen':
            screen = services.guiapi.get_screen()
            self.send(json.dumps(screen))
        elif cmd['cmd'] == 'click_left':
            services.guiapi.click_left(cmd['x'], cmd['y'])
            self.send_ack()
        elif cmd['cmd'] == 'menu_click':
            services.guiapi.menu_invoke(cmd['menu_path'])
            self.send_ack()
        elif services.cfg.callback is not None:
            rsp = services.cfg.callback(cmd)
            if rsp is None:
                self.send_ack()
            else:
                self.send(rsp)
        else:
            # unknown command, let client know
            services.logger.info(f'server      : nak unknown command: cmd="{cmd["cmd"]}" ')
            self.send_nak()
