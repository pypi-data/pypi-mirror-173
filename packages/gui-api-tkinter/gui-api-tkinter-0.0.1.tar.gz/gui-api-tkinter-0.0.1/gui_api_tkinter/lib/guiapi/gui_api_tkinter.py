import pynput

from . import services
from .cfg import Cfg
from .gui_api_server import GuiApiServer


# --------------------
class GuiApiTinker:
    # --------------------
    def __init__(self):
        self._windows = None
        self._screens = None
        self._menu = None

        services.guiapi = self
        services.server = GuiApiServer()

    # --------------------
    def init(self, ip_address=None, ip_port=None, logger=None, verbose=None, callback=None):
        services.cfg = Cfg()
        if logger is not None:
            services.logger = logger
        if verbose is not None:
            services.cfg.verbose = verbose
        if ip_address is not None:
            services.cfg.ip_address = ip_address
        if ip_port is not None:
            services.cfg.ip_port = ip_port
        if callback is not None:
            services.cfg.callback = callback

        services.server.init()
        self._windows = []

    # --------------------
    def add(self, window):
        self._windows.append(window)

    # --------------------
    def set_menu(self, menu):
        self._menu = menu

    # --------------------
    def set_name(self, widget, name):
        setattr(widget, 'guiapi_name', name)

    # --------------------
    def click_left(self, x, y):
        services.logger.info(f'click_left: {x} {y}')
        m = pynput.mouse.Controller()
        prev_posn = m.position
        m.position = (x, y)
        m.click(pynput.mouse.Button.left, 1)
        # restore previous mouse position
        m.position = prev_posn

    # --------------------
    def get_screen(self):
        services.logger.info('get_screen')
        self._screens = []
        for window in self._windows:
            n = self._report_window(window)
            self._screens.append(n)

        # services.logger.info(f'screen:\n{json.dumps(self._screens, indent=4)}')
        services.logger.info('get_screen done')
        return self._screens

    # --------------------
    def _report_window(self, w):
        n = {
            'class': w.winfo_class(),
            'name': getattr(w, 'guiapi_name', 'unknown'),
            'title': w.title(),
            'geometry': w.geometry(),
        }
        self._get_coordinates(w, n)

        n['children'] = []
        for frame in w.winfo_children():
            child = {}
            self._report_child(frame, child)
            n['children'].append(child)

        return n

    # --------------------
    def _report_child(self, f, n):
        n['class'] = f.winfo_class()
        n['name'] = getattr(f, 'guiapi_name', 'unknown')

        # menus are handled differently
        if f.winfo_class() in ['Menu']:
            n['menu'] = []
            for index in range(0, f.index('end') + 1):
                if f.type(index) in ['command', 'cascade']:
                    menuitem = {
                        'index': index,
                        'type': f.type(index),
                        'label': f.entrycget(index, 'label'),
                        'state': f.entrycget(index, 'state'),
                    }
                    n['menu'].append(menuitem)
        else:
            # text on the screen and the current enable/disable state
            if f.winfo_class() in ['Label', 'Button']:
                n['value'] = f.cget('text')
                n['state'] = f.cget('state')
            else:
                n['value'] = '<unknown>'
                n['state'] = '<unknown>'

        self._get_coordinates(f, n)

        n['children'] = []
        for c in f.winfo_children():
            child = {}
            self._report_child(c, child)
            n['children'].append(child)

    # --------------------
    def _get_coordinates(self, f, n):
        x1 = f.winfo_rootx()
        y1 = f.winfo_rooty()
        x2 = x1 + f.winfo_width()
        y2 = y1 + f.winfo_height()
        n['coordinates'] = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

    # --------------------
    def menu_invoke(self, menu_path):
        item = self._menu
        for index in menu_path:
            if index == menu_path[-1]:
                # TODO check if it is type == 'command'
                # this index is the last one in the menu_path so invoke it
                item.invoke(index)
            else:
                item = item.winfo_children()[0]
