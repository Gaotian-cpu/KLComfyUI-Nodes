# -*- coding: utf-8 -*-
from .comfy_nodes.callback_nodes import KLCallbackVdImg
from .comfy_nodes.misc_nodes import PromptIdFetcher

NODE_CLASS_MAPPINGS = {
    "singleVideoImgCallback": KLCallbackVdImg,
    'Prompt ID Fetcher': PromptIdFetcher
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "singleVideoImgCallback": "Single Video_Img Callback",
    'Prompt ID Fetcher': 'Prompt ID Fetcher'
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAMES_MAPPINGS']

