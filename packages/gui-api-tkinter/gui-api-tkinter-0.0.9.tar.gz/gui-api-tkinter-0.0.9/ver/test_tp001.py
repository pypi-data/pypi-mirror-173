import json
import sys
import unittest

from pytest_ver import pth

sys.path.append('.')

from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.mock_logger import MockLogger
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness  # noqa: E402


# -------------------
class TestTp001(unittest.TestCase):
    page1 = None
    logger = None
    helper = None
    th = None

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        services.th = GuiApiHarness()
        services.th.init()
        services.logger = MockLogger()
        services.helper = Helper()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        services.helper.kill_process()
        self.assertFalse(services.helper.gui_process.is_alive())

        print(f'DBG {services.logger.lines}')

    # --------------------
    @classmethod
    def tearDownClass(cls):
        services.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_overall(self):
        pth.proto.protocol('tp-001', 'basic server tests')

        pth.proto.step('start gui')
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected(), reqids='SRS-009')

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected(), reqids=['SRS-001', 'SRS-009'])

        pth.proto.step('get page content')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0, reqids='SRS-006')

        pth.proto.step('check initial state of the label')
        pth.ver.verify_equal(services.helper.label1_text, 'state: 0', reqids='SRS-007')

        pth.proto.step('click a button')
        services.helper.click_button1()
        services.th.get_screen()
        pth.ver.verify_equal(services.helper.label1_text, 'state: 1', reqids='SRS-007')

        pth.proto.step('click "Clear" menu item')
        services.helper.click_clear_menuitem()
        services.th.get_screen()
        pth.ver.verify_equal(services.helper.label1_text, 'state: 0', reqids='SRS-008')

        pth.proto.step('send "cmd01" command')
        cmd = {
            'cmd': 'cmd01',
            'param1': 'some parameter1',
            'param2': 'some parameter2',
        }
        rsp = services.th.send_recv(cmd)
        pth.ver.verify_equal(rsp['value'], 'ack', reqids='SRS-004')

        pth.proto.step('disconnect from GUI API server')
        services.th.term()
        pth.ver.verify_false(services.th.is_connected(), reqids='SRS-003')

        # # check root frame title
        # item = services.th.search(['window1'])
        # self.assertEqual(item['title'], 'Sample Version: v1.0.1')
        #
        # # check page title
        # item = services.th.search(self.page1.title)
        # self.assertEqual(item['value'], 'Page : ')
        #
        # # check current page
        # item = services.th.search(self.page1.page)
        # self.assertEqual(item['value'], 'page1')
        #
        # # enabled state of button1
        # item = services.th.search(self.page1.button1)
        # self.assertEqual(item['state'], 'normal')
        #
        # item = services.th.search(self.page1.button2)
        # self.assertEqual(item['state'], 'normal')
        #
        # # check if 1st item is not found
        # item = services.th.search(['windowx', 'page1_frame', 'page'])
        # self.assertIsNone(item)
        #
        # # check if middle item is not found
        # item = services.th.search(['window1', 'pagex_frame', 'page'])
        # self.assertIsNone(item)
        #
        # # check if last item is not found
        # item = services.th.search(['window1', 'page_frame', 'pagex'])
        # self.assertIsNone(item)
        #
        # # check if empty list
        # item = services.th.search([])
        # self.assertIsNone(item)
        #
        # # check if search list is None
        # item = services.th.search(None)
        # self.assertIsNone(item)
        #
        # # check button text
        # item = services.th.search(self.page1.button1)
        # self.assertEqual(item['value'], 'press me!')
        # item = services.th.search(self.page1.button2)
        # self.assertEqual(item['value'], 'press me!')
        #
        # # check label text
        # item = services.th.search(self.page1.label1)
        # self.assertEqual(item['value'], 'state: 0')
        # item = services.th.search(self.page1.label2)
        # self.assertEqual(item['value'], 'state: 0')
