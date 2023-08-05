import json
import sys
import time

sys.path.append('')
from sample.common.logger import Logger  # noqa: E402
from gui_api_tkinter.lib.testharness.cfg import Cfg  # noqa: E402
from gui_api_tkinter.lib.testharness.client import Client  # noqa: E402
from gui_api_tkinter.lib.testharness import services


# --------------------
## sample Test Harness used to communicate with GuiApi Server
class TestHarness:
    def __init__(self):
        self._content = None

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        services.cfg = Cfg()
        services.logger = Logger()
        services.client = Client()

    # --------------------
    def term(self):
        if services.client is not None:
            services.client.term()
            services.client = None

    # --------------------
    def connect(self):
        services.client.init()
        time.sleep(1.0)

    # --------------------
    def is_connected(self):
        return services.client.is_connected()

    # --------------------
    def get_screen(self):
        jsonstr = services.client.get_screen()
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
        # services.logger.info(f'DBG searching index={index} srch={search_name} {search_list}')
        for item in content:
            if item['name'] == search_name:
                if index == len(search_list) - 1:
                    # uncomment to debug
                    # services.logger.info(f'DBG found it  index={index} node={item}')
                    return item

                # it matched, but not at the end of the search list, so check the children
                # uncomment to debug
                # services.logger.info(f'DBG children  index={index} srch={search_name} curr={item["name"]}')
                node = self._search_content(item['children'], search_list, index + 1)
                if node is not None:
                    return node

        # uncoment to debug
        # services.logger.info(f'DBG not_found index={index} {search_name}')
        return None

    # --------------------
    def click_left_at(self, x, y):
        ack_nak = services.client.click_left(x, y)
        services.logger.info(f'click_left_at: {x}, {y}: {ack_nak}')

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
        ack_nak = services.client.menu_click(menu_path)
        services.logger.info(f'menu_click: {menu_path}: {ack_nak}')

    # --------------------
    def cmd01(self):
        ack_nak = services.client.cmd01()
        services.logger.info(f'cmd01: {ack_nak}')


th = TestHarness()
