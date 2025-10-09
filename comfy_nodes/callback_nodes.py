# -*- coding: utf-8 -*-
import os
import time
from typing import Optional, Tuple

import requests

from ..klutils.picture_util import PictureUtils
from ..klutils.file_util import FileUtil
from ..klutils.klLog import Log
from ..klutils.string_util import StringUtil
from .basic_nodes import KLBasicNode


class KLCallbackVdImg(KLBasicNode):
    __name__ = 'KLCallbackVdImg'
    __version__ = '1.0.0'
    __logger__ = Log.get_logger(__name__)

    # 强制节点每次都运行
    # OUTPUT_NODE = True

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("RESULT_TXT", "RESULT_CODE", "PROMPT ID")
    FUNCTION = "commit_result"
    CATEGORY = "KLNodes/WorkflowCallback"
    OUTPUT_NODE = True  # 设置这个节点为输出节点，每次都会执行

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "callback_url": ("STRING", {}),
                "video": ("STRING", {}),
                'image': ("STRING", {}),
                'prompt_id': ("STRING", {}),
                # 添加一个随机种子参数，以便每次都会运行本节点
                # 去掉不要了
                # "random_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },

            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",  # 添加这个
            },
        }

        return inputs

    def __init__(self, *args, **kwargs):
        super(KLCallbackVdImg, self).__init__(*args, **kwargs)

        # Fixme
        self.set_all_log(False)

    def commit_result(self, callback_url: str, video: str, image: str, prompt_id: str,
                      extra_pnginfo=None, unique_id=None, *args, **kwargs) -> tuple:
        """
        回调
        :param callback_url: 回调地址
        :param video: 视频文件路径
        :param image: 图片文件路径
        :param prompt_id:
        :param extra_pnginfo:
        :param unique_id:
        :return: (err_msg, err_code, prompt id)
        """
        if StringUtil.is_string_empty(callback_url):
            self.__logger__.error(u'callback url is empty, cannot commit generated result!')
            return 'callback url is empty', 2, ''

        if StringUtil.is_string_empty(prompt_id):
            self.__logger__.error('prompt id is empty, cannot commit generated result!')
            return 'prompt id is empty', 2, ''

        # self.__logger__.info(u'本次prompt id：{}'.format(prompt_id))

        # 对于image和video，如果给过来的是list，那么就取第一个
        if isinstance(image, list) and len(image) > 0:
            image = image[0]
        if isinstance(video, list) and len(video) > 0:
            video = video[0]

        if StringUtil.is_string_empty(video):
            self.__logger__.error('video path is empty, cannot commit generated result!')
            return 'video path is empty', 2, ''

        if StringUtil.is_string_empty(image):
            self.__logger__.info('image type: {}'.format(image))
            self.__logger__.error('image path is empty, cannot commit generated result!')
            return 'image path is empty', 2, ''

        if not FileUtil.check_file_exist(video):
            self.__logger__.error('video[{}] not exist, cannot commit generated result!'.format(video))
            return 'video[{}] not exist, cannot commit generated result!'.format(video), 2, prompt_id

        if not FileUtil.check_file_exist(image):
            self.__logger__.error('tail frame image[{}] not exist!'.format(image))

        # commit the video and the image
        succeed, err_code, err_msg = self.__send_result_to_callback__(
            callback_url=callback_url, prompt_id=prompt_id, img_path=image, video_path=video
        )
        if not succeed:
            self.__logger__.error('failed to commit generated result: {}, {}'.format(err_code, err_msg))
            return 'failed', -1, prompt_id

        return 'succeed', 0, prompt_id

    @classmethod
    def __send_result_to_callback__(
            cls,
            callback_url: str,
            prompt_id: str,
            img_path: Optional[str] = None,
            video_path: Optional[str] = None,
            max_retries: int = 3
    ) -> Tuple[bool, str, str]:
        """
    向回调地址发送运算结果（使用表单形式）

    Args:
        callback_url: 回调地址URL
        prompt_id: 请求ID
        img_path: 图片文件路径
        video_path: 视频文件路径
        max_retries: 最大重试次数，默认为3

    Returns:
        Tuple[bool, str, str]: (是否成功, 错误代码, 错误信息)
    """
        if StringUtil.is_string_empty(callback_url):
            return False, '-1', 'the callback url is empty, stop commit the generated result!'

        if StringUtil.is_string_empty(prompt_id):
            return False, '-1', 'the prompt id is empty, stop commit the generated result!'

        if not FileUtil.check_file_exist(img_path):
            return False, '-1', 'the img[{}] not exists, stop committing the generated result!'.format(img_path)

        if not FileUtil.check_file_exist(video_path):
            return False, '-1', 'the video[{}] not exists, stop committing the generated result!'.format(video_path)

        if not isinstance(max_retries, int) or max_retries <= 0:
            max_retries = 3

        # 图片转换格式为jpg
        tmp_pic_path = ''
        try:
            pic_real_format = PictureUtils.get_image_real_format(image_file_path=img_path)
            if not StringUtil.is_string_empty(pic_real_format) \
                    and pic_real_format not in [PictureUtils.IMG_FORMAT_JPEG]:
                cls.__logger__.info(u'reformat img as jpg...')

                img_dir = os.path.split(img_path)[0]
                tmp_pic_path = os.path.join(
                    img_dir,
                    '{}-{}.jpg'.format(str(time.time()), StringUtil.get_random_number_string(6))
                )
                if not PictureUtils.convert_pic_format(
                        src_path=img_path,
                        output_path=tmp_pic_path,
                        output_format=PictureUtils.IMG_FORMAT_JPEG
                ):
                    # 转换失败就恢复空值，后面会改为原始图片
                    tmp_pic_path = ''
                else:
                    cls.__logger__.info('img reformatting succeed!')
        except Exception as e:
            cls.__logger__.exception('img reformatting failed!', e)
            tmp_pic_path = ''
        if StringUtil.is_string_empty(tmp_pic_path):
            tmp_pic_path = img_path

        # 准备表单数据
        files_to_send = {
            'image': (
                os.path.basename(tmp_pic_path),
                open(tmp_pic_path, 'rb'),
                'image/*'
            ),
            'video': (
                os.path.basename(video_path),
                open(video_path, 'rb'),
                'video/*'
            )
        }
        form_data = {'promptId': prompt_id}

        last_error_code = ""
        last_error_msg = ""

        for attempt in range(max_retries):
            try:
                # 重新打开文件（因为文件指针可能已经移动）
                if attempt > 0:
                    # 关闭之前打开的文件
                    for file_info in files_to_send.values():
                        file_info[1].close()

                    # 重新打开文件
                    files_to_send['image'] = (
                        os.path.basename(tmp_pic_path),
                        open(tmp_pic_path, 'rb'),
                        'image/*'
                    )
                    files_to_send['video'] = (
                        os.path.basename(video_path),
                        open(video_path, 'rb'),
                        'video/*'
                    )

                # 发送POST请求（表单形式）
                response = requests.post(
                    callback_url,
                    files=files_to_send,
                    data=form_data,
                    timeout=60  # 30秒超时
                )

                # 检查响应状态
                if response.status_code == 200:
                    # 成功，关闭所有文件
                    for file_info in files_to_send.values():
                        file_info[1].close()
                    return True, '200', ""

                # 处理不同的HTTP状态码
                error_handlers = {
                    400: ("BAD_REQUEST", f"请求参数错误: {response.text}"),
                    401: ("UNAUTHORIZED", "认证失败"),
                    403: ("FORBIDDEN", "权限不足"),
                    404: ("NOT_FOUND", "回调地址不存在"),
                    413: ("PAYLOAD_TOO_LARGE", "文件大小超过限制"),
                    415: ("UNSUPPORTED_MEDIA_TYPE", "不支持的媒体类型"),
                    500: ("SERVER_ERROR", "服务器内部错误"),
                    502: ("BAD_GATEWAY", "网关错误"),
                    503: ("SERVICE_UNAVAILABLE", "服务不可用"),
                    504: ("GATEWAY_TIMEOUT", "网关超时")
                }

                if response.status_code in error_handlers:
                    last_error_code, last_error_msg = error_handlers[response.status_code]
                else:
                    last_error_code = f"HTTP_{response.status_code}"
                    last_error_msg = f"HTTP错误: {response.status_code} - {response.text}"
            except requests.exceptions.Timeout:
                last_error_code = "TIMEOUT"
                last_error_msg = "请求超时"
            except requests.exceptions.ConnectionError:
                last_error_code = "CONNECTION_ERROR"
                last_error_msg = "连接错误"
            except requests.exceptions.RequestException as e:
                last_error_code = "REQUEST_ERROR"
                last_error_msg = f"请求异常: {str(e)}"
            except Exception as e:
                last_error_code = "UNKNOWN_ERROR"
                last_error_msg = f"未知错误: {str(e)}"

            # 如果不是最后一次尝试，等待后重试
            if attempt < max_retries - 1:
                # 指数退避策略，等待时间逐渐增加
                wait_time = 2 ** attempt
                time.sleep(wait_time)

        # 所有重试都失败，关闭所有文件
        for file_info in files_to_send.values():
            file_info[1].close()

        return False, last_error_code, last_error_msg




