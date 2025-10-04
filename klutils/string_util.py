import hashlib
import re
import time
import random
from datetime import timedelta, datetime

import pytz
from dateutil import parser


class StringUtil:
    __version__ = '1.1.0'
    __name__ = 'StringUtil'

    @classmethod
    def is_string_empty(cls, string: str) -> bool:
        if string is None or not isinstance(string, str):
            return True

        return len(string) == 0

    @classmethod
    def int_string_zfill(cls, value: int, string_len: int) -> str:
        return str(value).zfill(string_len)

    @classmethod
    def equals_ignore_case(cls, str1: str, str2: str) -> bool:
        if cls.is_string_empty(str1) is True:
            return cls.is_string_empty(str2)

        if cls.is_string_empty(str2) is True:
            return cls.is_string_empty(str1)

        return str1.lower() == str2.lower()

    @classmethod
    def equals(cls, str1: str, str2: str) -> bool:
        if cls.is_string_empty(str1) is True:
            return cls.is_string_empty(str2)

        if cls.is_string_empty(str2) is True:
            return cls.is_string_empty(str1)

        return str1 == str2

    @classmethod
    def is_string_in_list(cls, string: str, str_list: list, ignore_case=False) -> bool:
        if cls.is_string_empty(string):
            return False

        if len(str_list) == 0:
            return False

        if ignore_case is False:
            return string in str_list

        result = False
        for str_in_list in str_list:
            if string.lower() == str_in_list.lower():
                result = True
                break

        return result

    @classmethod
    def get_random_number_string(cls, digits: int) -> str:
        """
        获取随机数字字符串
        :param digits: 几位数字
        :return: 生成的字符串
        """
        if digits is None or digits <= 0:
            return ''

        res = ''
        chars = '01234567890'

        count = 0
        while count < digits:
            res += random.choice(chars)
            count += 1

        return res

    @classmethod
    def get_random_alphabetic_string(cls, length: int, exceptions: list = None) -> str:
        if type(length) is not int or length <= 0:
            return ''

        res = ''
        chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if isinstance(exceptions, list) and len(exceptions) > 0:
            # 从chars中删除掉exceptions中字符
            exceptions_set = set(exceptions)  # 转换为集合以提高查找效率
            chars = ''.join([char for char in chars if char not in exceptions_set])

        count = 0
        while count < length:
            res += random.choice(chars)
            count += 1

        return res

    @classmethod
    def get_current_time_string(cls) -> str:
        timestamp = time.time()
        time_struct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d-%H_%M_%S', time_struct)

    @classmethod
    def get_current_time_str_standard(cls) -> str:
        timestamp = time.time()
        time_struct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)

    @classmethod
    def get_time_string_hour(cls, value: int) -> str:
        if type(value) is not int:
            return ''

        time_struct = time.localtime(value)
        return time.strftime('%02H:%02M:%02S', time_struct)

    @classmethod
    def get_time_string_full(cls, value: int) -> str:
        if type(value) is not int:
            return ''

        time_struct = time.localtime(value)
        return time.strftime('%Y-%m-%d-%H_%M_%S', time_struct)

    @classmethod
    def convert_time_str_to_seconds(cls, string: str) -> int:
        """
        将%02H:%02M:%02S格式的时间字符串转换为秒为单位的数值
        :param string:
        :return:
        """
        if cls.is_string_empty(string):
            return -1

        hours, minutes, seconds = map(int, re.split(r'\s*:\s*', string))
        return hours * 3600 + minutes * 60 + seconds

    @classmethod
    def get_number_string(cls, value: int, length: int) -> str:
        """
        将数字转换为字符串，空位补0
        :param value:
        :param length:
        :return:
        """
        return str(value).zfill(length)

    @classmethod
    def get_str_hash_hex_str(cls, string: str, encoding: str = 'UTF-8') -> str:
        """
        获得一个字符串的16进制编码的哈希值
        :param encoding:
        :param string:
        :return:
        """
        if not isinstance(string, str):
            return ''

        hash_obj = hashlib.sha256()
        try:
            hash_obj.update(string.encode(encoding=encoding if isinstance(encoding, str) else 'UTF-8'))
        except Exception as e:
            hash_obj.update(string.encode())

        return hash_obj.hexdigest()

    @classmethod
    def standard_readable_date_str(cls, time_str: str) -> str:
        """
        把September 16, 2022 at 6:38 pm格式的时间字符串转换成标准格式的
        :param time_str:
        :return:
        """
        if StringUtil.is_string_empty(time_str):
            return ''

        month_dict = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12,
        }

        # September 16, 2022 at 6:38 pm
        try:
            date_part, time_part = re.split(r'\s*at\s*', time_str)
            month_day_part, year_part = re.split(r'\s*,\s*', date_part)
            month, day = re.split(r'\s+', month_day_part)
            for key, value in month_dict.items():
                if month.lower() in key.lower():
                    month = value
                    break
            month = cls.get_number_string(month, 2)
            day = cls.get_number_string(int(day), 2)

            time_str = time_part.replace('pm', '').replace('am', '').replace('PM', '').replace('AM', '').strip()
            hour, minute = re.split(r':', time_str)
            hour = cls.get_number_string(int(hour), 2)
            minute = cls.get_number_string(int(minute), 2)
            second = '00'
            time_str = ':'.join([hour, minute, second])

            return '{}-{}-{} {}'.format(year_part, month, day, time_str)
        except Exception as e:
            print(e)
            return ''

    @classmethod
    def convert_with_timezone(cls, utc_string: str, local_timezone: int) -> str:
        """
        将带有时区的时间转换成本地时区时间。
        :param utc_string: 带有时区的时间字符串，格式：2024-01-03 12:14:08+00:00
        :param local_timezone:
        :return:
        """
        if StringUtil.is_string_empty(utc_string):
            return ''

        if not isinstance(local_timezone, int) or local_timezone < -11 or local_timezone > 11:
            print(u'时区【{}】有误，无法转换！'.format(local_timezone))
            return ''

        utc_time = parser.parse(utc_string)
        local_time = utc_time + timedelta(hours=local_timezone)

        return local_time.strftime('%Y-%m-%d %H:%M:%S%z')

    @classmethod
    def convert_hour_minute_with_timezone(cls, utc_string: str, local_timezone: int) -> str:
        """
        将带有时区的utc字符串进行时区转换，然后再提取其中的小时和分钟
        :param utc_string: 带有时区的时间字符串，格式：2024-01-03 12:14:08+00:00
        :param local_timezone:
        :return:
        """
        if StringUtil.is_string_empty(utc_string):
            return ''

        if not isinstance(local_timezone, int) or local_timezone < -11 or local_timezone > 11:
            print(u'时区【{}】有误，无法转换！'.format(local_timezone))
            return ''

        utc_time = parser.parse(utc_string)
        local_time = utc_time + timedelta(hours=local_timezone)

        return local_time.strftime('%H:%M')

    @classmethod
    def convert_seconds_to_days(cls, value: int) -> int:
        """
        把秒转换成天
        :param value:
        :return:
        """
        if not isinstance(value, int):
            return 0
        else:
            return int(round(value / (60 * 60 * 24), 0))

    @classmethod
    def convert_timestamp_to_str(cls, timestamp_ms: int) -> str:
        if not isinstance(timestamp_ms, (int, float)):
            return ''

        # 转换为秒（浮点数），保留毫秒信息
        timestamp_sec = timestamp_ms / 1000.0
        # 转换为datetime对象（UTC时间）
        dt = datetime.utcfromtimestamp(timestamp_sec)
        # 格式化为字符串：年-月-日 时:分:秒
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def convert_time_str_by_zone(cls, time_str, target_timezone: int, local_timezone: int = 8) -> str:
        """
        按照时区更改更改时间字符串
        :param time_str:
        :param target_timezone:
        :param local_timezone:
        :return:
        """
        if not isinstance(local_timezone, int) or not isinstance(target_timezone, int):
            return time_str

        if StringUtil.is_string_empty(time_str):
            return time_str

        if target_timezone == local_timezone:
            return time_str

        try:
            # 将字符串转换为datetime对象 (无时区信息)
            naive_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

            # 将原始时间视为UTC+8时区
            beijing_tz = pytz.timezone("Asia/Shanghai")
            beijing_time = beijing_tz.localize(naive_time)

            # 计算目标时区
            target_tz = pytz.timezone(f"Etc/GMT{'-' if target_timezone > 0 else '+'}{abs(target_timezone)}")

            # 转换时区
            target_time = beijing_time.astimezone(target_tz)

            # 格式化为字符串
            return target_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"Time zone conversion failed: {e}")
            return time_str  # 转换失败时返回原时间

    @classmethod
    def convert_to_utc8(cls, time_str: str, from_timezone: int) -> str:
        if from_timezone == 8:  # 已经是UTC+8，不需要转换
            return time_str

        try:
            # 解析原始时间字符串
            naive_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

            # 创建原始时区对象
            from_tz = pytz.FixedOffset(from_timezone * 60)  # 时区转换为分钟偏移

            # 将原始时间附加时区信息
            localized_time = from_tz.localize(naive_time)

            # 转换为UTC+8时区
            utc8_tz = pytz.FixedOffset(8 * 60)
            utc8_time = localized_time.astimezone(utc8_tz)

            # 格式化为字符串
            return utc8_time.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"时区转换失败: {e}")
            return time_str  # 转换失败时返回原时间


if __name__ == '__main__':
    print(StringUtil.standard_readable_date_str('September 2, 2022 at 6:38 pm'))
