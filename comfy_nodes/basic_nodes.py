# -*- coding: utf-8 -*-
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

    def get_prompt_id(self, prompt=None, extra_pnginfo=None, unique_id=None) -> str:
        if not StringUtil.is_string_empty(self.__prompt_id__):
            return self.__prompt_id__

        # 获取 workflow_id
        if self.__all_log__:
            self.__logger__.info('prompt: {}'.format(prompt))
            self.__logger__.info('extra_pnginfo: {}'.format(extra_pnginfo))
            self.__logger__.info('unique_id: {}'.format(unique_id))

        workflow_id = None

        if extra_pnginfo and 'workflow' in extra_pnginfo:
            workflow_id = extra_pnginfo['workflow'].get('id')

        if not workflow_id and prompt:
            workflow_id = prompt.get('workflow', {}).get('id')

        self.__prompt_id__ = workflow_id

        return self.__prompt_id__

