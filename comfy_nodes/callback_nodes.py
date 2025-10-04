# -*- coding: utf-8 -*-
from ..klutils.file_util import FileUtil
from ..klutils.klLog import Log
from ..klutils.string_util import StringUtil
from .basic_nodes import KLBasicNode


class KLCallbackVdImg(KLBasicNode):
    __name__ = 'KLCallbackVdImg'
    __version__ = '1.0.0'
    __logger__ = Log.get_logger(__name__)

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("RESULT_TXT", "RESULT_CODE", "PROMPT ID")
    FUNCTION = "commit_result"
    CATEGORY = "KLNodes/WorkflowCallback"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "callback_url": ("STRING", {}),
                "video": ("STRING", {}),
                'image': ("STRING", {})
            },

            "hidden": {"prompt": "PROMPT", "unique_id": "UNIQUE_ID"},
        }

        return inputs

    def __init__(self, *args, **kwargs):
        super(KLCallbackVdImg, self).__init__(*args, **kwargs)

        # Fixme
        self.set_all_log(True)

    def commit_result(self, callback_url: str, video: str, image: str,
                      prompt=None, unique_id=None) -> tuple:
        """
        回调
        :param callback_url: 回调地址
        :param video: 视频文件路径
        :param image: 图片文件路径
        :param prompt:
        :param unique_id:
        :return: (err_msg, err_code, prompt id)
        """
        if StringUtil.is_string_empty(callback_url):
            self.__logger__.error(u'callback url is empty, cannot commit generated result!')
            return 'callback url is empty', 2, ''

        if StringUtil.is_string_empty(video):
            self.__logger__.error('video path is empty, cannot commit generated result!')
            return 'video path is empty', 2, ''

        if StringUtil.is_string_empty(image):
            self.__logger__.error('image path is empty, cannot commit generated result!')
            return 'image path is empty', 2, ''

        self.__logger__.info('prompt: {}'.format(prompt))

        if StringUtil.is_string_empty(prompt):
            self.__logger__.error('prompt is empty, cannot commit generated result!')
            return 'prompt id is empty', 2, ''

        # 解析prompt id
        prompt_id = None

        if not FileUtil.check_file_exist(video):
            self.__logger__.error('video[{}] not exist, cannot commit generated result!'.format(video))
            return 'video[{}] not exist, cannot commit generated result!'.format(video), 2, ''

        if not FileUtil.check_file_exist(image):
            self.__logger__.error('tail frame image[{}] not exist!'.format(image))

        # TODO commit the video and the image

        return 'succeed', 0, prompt_id
