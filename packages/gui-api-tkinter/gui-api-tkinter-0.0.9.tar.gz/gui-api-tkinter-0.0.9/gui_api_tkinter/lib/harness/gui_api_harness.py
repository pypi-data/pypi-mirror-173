import time

from .client import Client
from .. import services
from ..cfg import Cfg
from ..logger_null import LoggerNull


# --------------------
## test harness used to communicate with GuiApi Server
class GuiApiHarness:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to common configuration information
        self.cfg = None
        ## holds reference to logger object
        self.logger = None
        ## holds current screen content
        self._content = None
        ## holds reference to the socket client
        self._client = None

    # --------------------
    ## initialize
    #
    # @param logger   (optional) a reference to a logger object
    # @return None
    def init(self, logger=None):
        self.cfg = Cfg()
        services.cfg = self.cfg
        if logger is None:
            self.logger = LoggerNull()
        else:
            self.logger = logger
        services.logger = self.logger
        self._client = Client()

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._client is not None:
            self._client.term()
            self._client = None

    # --------------------
    ## connect to the GUI API server running inside the GUI
    #
    # @return None
    def connect(self):
        self._client.init()
        time.sleep(0.5)

    # --------------------
    ## check if connected to the server
    #
    # @return True if connected, False otherwise
    def is_connected(self):
        if self._client is None:
            return False

        return self._client.is_connected()

    # --------------------
    ## send a command and wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd: dict) -> dict:
        return self._client.send_recv(cmd)

    # --------------------
    ## get the current screen contents in JSON format
    #
    # @return screen content in JSON format
    def get_screen(self) -> list:
        screen = self._client.get_screen()
        # currently can only handle 1 root window,
        # therefore content is a list of one item
        self._content = [screen]
        return self._content

    # --------------------
    ## the current screen contents in JSON format
    #
    # @return the current screen contents in JSON format
    @property
    def content(self) -> dict:
        return self._content

    # --------------------
    ## find the widget matching the path given in the search list
    #
    # @param search_list  a list of widget names
    # @return the widget item if found, None otherwise
    def search(self, search_list: list):
        return self._search_content(self._content, search_list, 0)

    # --------------------
    ## recursive function to find the widget item that matches the search list
    #
    # @param content      the screen content to search
    # @param search_list  the list of widget names to search
    # @param index        the current entry in the search_list
    # @return the widget item if matches the last entry in search_list, None otherwise
    def _search_content(self, content, search_list, index=0):
        if content is None or \
                search_list is None or \
                len(search_list) == 0:
            return None

        search_name = search_list[index]
        # uncomment to debug
        # self.logger.info(f'DBG searching index={index} srch={search_name} {search_list}')
        for item in content:
            if item['name'] == search_name:
                if index == len(search_list) - 1:
                    # uncomment to debug
                    # self.logger.info(f'DBG found it  index={index} node={item}')
                    return item

                # it matched, but not at the end of the search list, so check the children
                # uncomment to debug
                # self.logger.info(f'DBG children  index={index} srch={search_name} curr={item["name"]}')
                node = self._search_content(item['children'], search_list, index + 1)
                if node is not None:
                    return node

        # uncoment to debug
        # self.logger.info(f'DBG not_found index={index} {search_name}')
        return None

    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x   the x value in screen coordinates
    # @param y   the y value in screen coordinates
    # @return None
    def click_left_at(self, x: int, y: int):
        ack_nak = self._client.click_left(x, y)
        self.logger.info(f'click_left_at: {x}, {y}: {ack_nak}')

    # --------------------
    ## click the left mouse button on the given widget item
    #
    # @param item  the widget item to click on
    # @return None
    def click_left_on(self, item: dict):
        x = int((item['coordinates']['x1'] + item['coordinates']['x2']) / 2)
        y = int((item['coordinates']['y1'] + item['coordinates']['y2']) / 2)
        self.click_left_at(x, y)

    # --------------------
    ## click the left mouse button on the widget at the given search list
    #
    # @param search_list  the path to the widget
    # @return None
    def click_left(self, search_list: list):
        item = self.search(search_list)
        self.click_left_on(item)

    # --------------------
    ## select the menu item at the given menu path
    #
    # @param menu_path   the list of menu indicies to search
    # @return None
    def menu_click(self, menu_path: list):
        ack_nak = self._client.menu_click(menu_path)
        self.logger.info(f'menu_click: {menu_path}: {ack_nak}')
