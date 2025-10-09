# -*- coding: utf-8 -*-
import base64
import os
import socket
import sys

import requests

from ..klutils.klLog import Log
from ..klutils.string_util import StringUtil


class KLBasicNode:
    __version__ = '1.0.0'
    __name__ = 'KLBasicNode'
    __logger__ = Log.get_logger(__name__)

    def __init__(self, *args, **kwargs):
        self.__prompt_id__: str = ''
        self.__all_log__ = False

    def set_all_log(self, value):
        if isinstance(value, bool):
            self.__all_log__ = value





