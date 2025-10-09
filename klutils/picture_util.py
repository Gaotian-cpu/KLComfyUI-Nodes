# -*- coding: utf-8 -*-
import imghdr

from PIL import Image

from .klLog import Log
from .string_util import StringUtil
from .file_util import FileUtil


class PictureUtils:
    __version__ = '1.0.0'
    __name__ = 'PictureUtils'
    __logger__ = Log.get_logger(__name__)

    IMG_FORMAT_WEBP = "WEBP"
    IMG_FORMAT_GIF = 'GIF'
    IMG_FORMAT_JPEG = 'JPEG'
    IMG_FORMAT_PNG = 'PNG'
    IMG_FORMAT_BMP = 'BMP',
    IMG_FORMAT_UNKNOWN = 'unknown'

    @classmethod
    def get_supported_img_formats(cls) -> list:
        return [
            cls.IMG_FORMAT_WEBP, cls.IMG_FORMAT_GIF, cls.IMG_FORMAT_JPEG,
            cls.IMG_FORMAT_PNG, cls.IMG_FORMAT_BMP
        ]

    @classmethod
    def get_image_real_format(cls, image_file_path: str) -> str:
        """
        获取图片的真实格式
        :param image_file_path: 图片路径
        :return:
        """
        if FileUtil.check_file_exist(image_file_path) is False:
            cls.__logger__.error('图片文件【{}】不存在，无法检查其真实类型！'.format(image_file_path))
            return cls.IMG_FORMAT_UNKNOWN

        img_type = cls.get_image_real_format_with_imghdr(image_file_path=image_file_path)
        if StringUtil.is_string_empty(img_type):
            img_type = cls.get_image_real_format_with_pillow(image_file_path)

        if img_type.upper() in cls.get_supported_img_formats():
            return img_type.upper()
        else:
            cls.__logger__.error('图片文件【{}】检查到格式为【{}】，未知图片格式！'.format(image_file_path, img_type))
            return cls.IMG_FORMAT_UNKNOWN

    @classmethod
    def get_image_real_format_with_imghdr(cls, image_file_path: str) -> str:
        return imghdr.what(image_file_path)

    @classmethod
    def get_image_real_format_with_pillow(cls, image_file_path: str) -> str:
        try:
            image = Image.open(image_file_path)
            image_format = image.format
        except Exception as e:
            cls.__logger__.exception('', e)
            image_format = ''

        return image_format

    @classmethod
    def convert_pic_format(cls, src_path: str, output_path: str, output_format: str) -> bool:
        """
        简单的进行图片格式转换
        :param src_path: 图片源文件路径
        :param output_path: 输出图片路径
        :param output_format: 输出图片格式
        :return: 操作结果
        """
        if StringUtil.is_string_empty(src_path):
            cls.__logger__.error(u'原图片路径为空，无法进行格式转换！')
            return False

        if not FileUtil.check_file_exist(src_path):
            cls.__logger__.error(u'原图片【{}】不存在，无法进行格式转换！'.format(src_path))
            return False

        if StringUtil.equals(src_path, output_path):
            cls.__logger__.error(u'源图片和输出图片路径相同，无法进行格式转换！')
            return False

        if output_format not in cls.get_supported_img_formats():
            cls.__logger__.error(u'输出图片格式【{}】有误，无法进行格式转换'.format(output_format))
            return False

        # 取源图片的真实格式
        real_format = cls.get_image_real_format(image_file_path=src_path)
        if StringUtil.is_string_empty(real_format):
            cls.__logger__.error(u'原图片【{}】获取图片路径失败，无法进行格式转换！'.format(src_path))
            return False

        # 如果格式相同，则直接复制
        if StringUtil.equals_ignore_case(output_format, real_format):
            return FileUtil.copy_file(src_file=src_path, dst_file=output_path)

        try:
            with Image.open(src_path) as img:
                # 保存
                img.save(output_path, output_format.lower())
        except Exception as e:
            cls.__logger__.exception('', e)

        return FileUtil.check_file_exist(output_path)
