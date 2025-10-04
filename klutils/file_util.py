import os
import sys
if __name__ == '__main__':
    sys.path.append(os.getcwd())

import shutil
import hashlib
from urllib.parse import urlparse
from .klLog import Log
from .string_util import StringUtil


class FileUtil:
    """
        文件工具类
        author: Alex
        date: 2020-12-08
        version: 1.1

        Modifications:
        developer: Alex
        date:2020-12-22
        details: 增加了计算文件哈希值的方法
    """
    __version__ = '1.3.0'
    __name__ = "FileUtil"
    __logger = Log.get_logger(__name__)

    @classmethod
    def check_file_exist(cls, file_path: str) -> bool:
        """
        检查文件是否存在
        :param file_path: 文件路径
        :return: True / False
        """
        if file_path is None or file_path == '':
            return False

        if os.path.exists(file_path) is False:
            return False

        if os.path.isfile(file_path) is False:
            return False

        return True

    @classmethod
    def check_directory_exist(cls, dir_path: str) -> bool:
        """
        检查目录是否存在
        :param dir_path: 目录路径
        :return: True / False
        """
        if dir_path is None or dir_path == '':
            return False

        if os.path.exists(dir_path) is False:
            return False

        if os.path.isdir(dir_path) is False:
            return False

        return True

    @staticmethod
    def get_file_or_directory_name(path):
        """
        获取文件或目录名称
        :param path: 文件或目录的路径
        :return: 结果或None
        """
        if path is None or path == '':
            return None

        return os.path.split(path)[1]

    @staticmethod
    def get_file_name_from_url(file_url: str) -> str:
        """
        从url中解析出文件名
        :param file_url:
        :return:
        """
        if StringUtil.is_string_empty(file_url):
            return ''

        parsed_url = urlparse(file_url)
        return parsed_url.path.split('/')[-1]

    @staticmethod
    def get_parent_directory(path: str):
        """
        获取目录或文件的父目录
        :param path: 文件或目录的路径
        :return: 结果或None
        """
        if path is None or path == '':
            return None

        if path.startswith('/'):
            return os.path.split(path)[0]
        else:
            abs_path = os.path.join(os.getcwd(), path)
            return os.path.split(abs_path)[0]

    @classmethod
    def copy_file(cls, src_file: str, dst_file: str) -> bool:
        """
        拷贝文件
        :param src_file: 源文件
        :param dst_file: 目的文件
        :return: True / False
        """
        if cls.check_file_exist(src_file) is False:
            cls.__logger.error('src file[{}] not exist, cannot copy'.format(src_file))
            return False

        if os.path.exists(dst_file):
            if os.path.isfile(dst_file) is False:
                cls.__logger.error('dst file[{}] exist, but is not a file. stop copying'.format(dst_file))
                return False
            os.remove(dst_file)

        shutil.copyfile(src_file, dst_file)

        return True

    @classmethod
    def move_file(cls, src_file_path: str, target_file_path: str) -> bool:
        if StringUtil.is_string_empty(src_file_path):
            cls.__logger.error('未设定源文件，无法移动！')
            return False

        if StringUtil.is_string_empty(target_file_path):
            cls.__logger.error('未设定目标文件，无法移动！')
            return False

        if cls.check_file_exist(src_file_path) is False:
            cls.__logger.error('源文件【{}】不存在，无法移动！'.format(src_file_path))
            return False

        target_dir = cls.get_parent_directory(target_file_path)
        if cls.check_directory_exist(target_dir) is False:
            if cls.create_directory(target_dir) is False:
                cls.__logger.error('创建目标目录【{}】失败，无法移动！'.format(target_dir))
                return False

        if cls.check_file_exist(target_file_path) is True:
            if cls.delete_file(target_file_path) is False:
                cls.__logger.error('目标文件【{}】存在，但是删除失败，无法移动！'.format(target_file_path))
                return False

        shutil.move(src_file_path, target_file_path)

        return cls.check_file_exist(target_file_path) is True and cls.check_file_exist(src_file_path) is False

    @classmethod
    def get_file_hash_sha1(cls, file_path: str) -> str:
        """
            获取文件sha1
            :param file_path: 文件路径
            :return: 16进制sha1或空字符串
        """
        if cls.check_file_exist(file_path) is False:
            cls.__logger.error('the file[{}] not exists, cannot calculate it\'s sha1'.format(file_path))
            return ''

        sha1obj = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break

                sha1obj.update(data)

        return sha1obj.hexdigest()

    @classmethod
    def get_file_hash_md5(cls, file_path: str) -> str:
        """
            获取文件md5
            :param file_path: 文件路径
            :return: 16进制md5或空字符串
        """
        md5obj = hashlib.md5()

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break

                md5obj.update(data)

        return md5obj.hexdigest()

    @classmethod
    def get_file_ext_name(cls, file_path: str) -> str:
        if len(file_path) == 0:
            return ''

        slices = os.path.splitext(file_path)
        if len(slices) < 2:
            return ''
        else:
            return slices[-1]

    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """
            刪除文件
            :param file_path: 文件路徑
            :return: 操作結果
        """
        if len(file_path) == 0:
            cls.__logger.error('為設定文件路徑，無法刪除！')
            return False

        if cls.check_file_exist(file_path) is False:
            return True

        os.remove(file_path)

        return not cls.check_file_exist(file_path)

    @classmethod
    def delete_directory(cls, file_path: str) -> bool:
        if len(file_path) == 0:
            cls.__logger.error('dir path not set, cannot remove!')
            return False

        if cls.check_directory_exist(file_path) is False:
            return True

        shutil.rmtree(file_path)

        return not cls.check_directory_exist(file_path)

    @classmethod
    def create_directory(cls, file_path: str, exist_ok=True) -> bool:
        if len(file_path) == 0:
            cls.__logger.error('dir path not set, cannot create')
            return False

        if cls.check_directory_exist(file_path) is False:
            os.makedirs(file_path)
            return cls.check_directory_exist(file_path)

        if exist_ok is True:
            return True

        if cls.delete_directory(file_path) is False:
            cls.__logger.error('the dir[{}] exists, but failed to delete, cannot create new one!'.format(file_path))
            return False

        os.makedirs(file_path)

        return cls.check_directory_exist(file_path)

    @classmethod
    def create_file(cls, file_path: str) -> bool:
        """
        创建文件
        :param file_path: 文件路径
        :return: 操作结果
        """
        if StringUtil.is_string_empty(file_path):
            cls.__logger.error('文件路径未设定，无法创建文件！')
            return False

        if cls.check_file_exist(file_path):
            return True

        with open(file_path, 'w') as file:
            file.flush()

        return cls.check_file_exist(file_path)

    @classmethod
    def get_file_size(cls, file_path: str) -> int:
        """
        获取文件大小
        :param file_path: 文件路径
        :return: 正确值>=0，错误值<0
        """
        if StringUtil.is_string_empty(file_path):
            return -1

        if FileUtil.check_file_exist(file_path) is False:
            return -1

        return os.path.getsize(file_path)

    @classmethod
    def clear_dir(cls, dir_path: str) -> bool:
        """
        清空目录
        :param dir_path:
        :return:
        """
        if StringUtil.is_string_empty(dir_path):
            cls.__logger.error(u'目录路径为空，无法清理！')
            return False

        if not cls.check_directory_exist(dir_path):
            cls.__logger.error(u'目录【{}】不存在，无法清理！'.format(dir_path))
            return False

        already_clean = True
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除目录及其所有内容

                return True
            except Exception as e:
                cls.__logger.exception(f'Failed to delete {file_path}. Reason: {e}')
                return False

        return already_clean

        # try:
        #     shutil.rmtree(dir_path)
        #     return True
        # except Exception as e:
        #     cls.__logger.exception(u'目录清理出错：{}'.format(dir_path), e)
        #     return False
