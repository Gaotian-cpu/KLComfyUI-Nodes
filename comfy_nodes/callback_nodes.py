# -*- coding: utf-8 -*-
from ..klutils.klLog import Log
from ..klutils.string_util import StringUtil


class KLCallbackVdImg:
    __name__ = 'KLCallbackVdImg'
    __version__ = '1.0.0'
    __logger__ = Log.get_logger(__name__)

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("RESULT_TXT", "RESULT_CODE")
    FUNCTION = "commit_result"
    CATEGORY = "KLNodes/WorkflowCallback"

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "callback_url": ("STRING", {}),
                "video": ("STRING", {}),
                'image': ("STRING", {})
            }
        }
        return inputs

    def commit_result(self, callback_url: str, video: str, image: str) -> tuple:
        """
        回调
        :param callback_url: 回调地址
        :param video: 视频文件路径
        :param image: 图片文件路径
        :return: (err_msg, err_code)
        """
        if StringUtil.is_string_empty(callback_url):
            self.__logger__.error(u'callback url is empty, cannot commit generated result!')
            return 'callback url is empty', 2

        if StringUtil.is_string_empty(video):
            self.__logger__.error('video path is empty, cannot commit generated result!')
            return 'video path is empty', 2

        if StringUtil.is_string_empty(image):
            self.__logger__.error('image path is empty, cannot commit generated result!')
            return 'image path is empty', 2

        # TODO commit the video and the image

        return 'succeed', 0
