import json
import time

from gui_api_tkinter.lib.harness.cfg import Cfg
from gui_api_tkinter.lib.harness.client import Client


# --------------------
## sample Test Harness used to communicate with GuiApi Server
class GuiApiHarness:
    def __init__(self):
        self._content = None
        self.cfg = None
        self.logger = None
        self.client = None

    # --------------------
    ## initialize
    #
    # @return None
    def init(self, logger=None):
        self.cfg = Cfg()
        self.logger = logger
        self.client = Client()

    # --------------------
    def term(self):
        if self.client is not None:
            self.client.term()
            self.client = None

    # --------------------
    def connect(self):
        self.client.init()
        time.sleep(1.0)

    # --------------------
    def is_connected(self):
        return self.client.is_connected()

    # --------------------
    def get_screen(self):
        jsonstr = self.client.get_screen()
        self._content = json.loads(jsonstr)
        return self._content

    # --------------------
    @property
    def content(self):
        return self._content

    # --------------------
    def search(self, search_list):
        return self._search_content(self._content, search_list, 0)

    # --------------------
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
    def click_left_at(self, x, y):
        ack_nak = self.client.click_left(x, y)
        self.logger.info(f'click_left_at: {x}, {y}: {ack_nak}')

    # --------------------
    def click_left_on(self, item):
        x = int((item['coordinates']['x1'] + item['coordinates']['x2']) / 2)
        y = int((item['coordinates']['y1'] + item['coordinates']['y2']) / 2)
        self.click_left_at(x, y)

    # --------------------
    def click_left(self, location):
        item = self.search(location)
        self.click_left_on(item)

    # --------------------
    def menu_click(self, menu_path):
        ack_nak = self.client.menu_click(menu_path)
        self.logger.info(f'menu_click: {menu_path}: {ack_nak}')



th = TestHarness()
