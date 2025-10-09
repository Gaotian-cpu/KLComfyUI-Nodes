# -*- coding: utf-8 -*-
import base64
import os
import socket
import sys

import requests

from ..klutils.string_util import StringUtil
from ..klutils.klLog import Log


class PromptIdFetcher:
    __version__ = '1.0.0'
    __name__ = 'PromptIdFetcher'
    __logger__ = Log.get_logger(__name__)

    __ENV_USERNAME__ = 'COMFYUI_USERNAME'
    __ENV_PASSWD__ = 'COMFYUI_PASSWORD'

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("PROMPT ID",)
    FUNCTION = "get_prompt_id"
    CATEGORY = "KLNodes/misc"
    OUTPUT_NODE = True  # 设置这个节点为输出节点，每次都会执行

    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
            },

        }

        return inputs

    def get_prompt_id(self) -> tuple:
        """
        获取工作流的prompt id
        :return:
        """
        return self.get_prompt_id_by_request(),

    def get_prompt_id_by_request(self) -> str:
        username, passwd = self.get_auth_info()
        if not StringUtil.is_string_empty(username) and not StringUtil.is_string_empty(passwd):
            headers = {
                'Authorization': self.__generate_auth_token__(username, passwd)
            }
        else:
            headers = None

        try:
            local_ip = self.get_local_ip()
            port = self.get_local_port()
            url = f"http://{local_ip}:{port}/queue"

            response = requests.get(url, headers=headers)
            # 检查响应状态
            if response.status_code == 200:
                queue_running = response.json().get("queue_running")
                if queue_running and len(queue_running) > 0 and len(queue_running[0]) > 1:
                    # self.__logger__.info('queue-running: {}'.format(queue_running))
                    # self.__logger__.info('Response Content in queue_running: {}'.format(queue_running[0][1]))
                    prompt_id = queue_running[0][1]
                    # self.__logger__.info(u'获取到prompt id: {}'.format(prompt_id))
                    return prompt_id
                else:
                    return ''
            else:
                self.__logger__.error(f"Failed to receive a successful response, status code: {response.status_code}")
                return ''
        except requests.exceptions.RequestException as e:
            self.__logger__.exception('', e)
            return ''
        except ValueError as e:
            self.__logger__.exception('', e)
            return ''

    # 从环境变量中获取用户名和密码
    def get_auth_info(self) -> tuple:
        return os.getenv(self.__ENV_USERNAME__, ''), os.getenv(self.__ENV_PASSWD__, '')

    # 获取当前程序运行的ip地址
    @staticmethod
    def get_local_ip():
        # 获取主机名
        hostname = socket.gethostname()
        # 获取本地主机的 IPv4 地址
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    # 获取当前运行程序的端口号
    @staticmethod
    def get_local_port():
        # 打印所有传递的命令行参数
        # print("所有命令行参数:", sys.argv)
        args = sys.argv
        if '--port' in args:
            port_index = args.index('--port')  # 获取 --port 的索引
            if port_index + 1 < len(args):  # 确保后面还有一个值
                # print(f"port有值{args[port_index + 1] }")
                return args[port_index + 1]  # 获取 --port 后面的值
            else:
                return '8188'
        else:
            return '8188'

    @classmethod
    def __generate_auth_token__(cls, user_name, passwd) -> str:
        token = base64.b64encode('{}:{}'.format(user_name, passwd).encode()).decode()
        return 'Basic {}'.format(token)
