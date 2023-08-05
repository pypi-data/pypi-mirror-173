#!/usr/bin/env python
#-*- coding:utf-8 -*-



"""

                   _  _              _
                  | || |            | |
  ___ __   __ ___ | || |_  ___  ___ | |_
 / __|\ \ / // _ \| || __|/ _ \/ __|| __|
 \__ \ \ V /|  __/| || |_|  __/\__ \| |_
 |___/  \_/  \___||_| \__|\___||___/ \__|



"""


import unittest
from typing import NoReturn, Optional, overload

from sveltest.components.network import RequestBase


class TestCase(unittest.TestCase):
    """基础类"""

    def start_class(self) -> NoReturn:
        """"""
        pass

    def end_class(self) -> NoReturn:
        """
        """
        pass

    @classmethod
    def setUpClass(cls) -> NoReturn:
        cls().start_class()

    @classmethod
    def tearDownClass(cls) -> NoReturn :
        cls().end_class()

    def setUp(self) -> NoReturn :
        pass

    def tearDown(self) -> NoReturn :
        pass


class HttpTestCase(TestCase,RequestBase):
    """
    用于HTTP测试
    """

    def initizlize_request(self):
        return None


class WebsocketTestCase(TestCase,RequestBase):
    """
    用于websocket测试
    """



class TestCaseSet(HttpTestCase,WebsocketTestCase):
    """
    用于HTTP测试
    """


