# -*- coding: utf-8 -*-
from .comfy_nodes.callback_nodes import KLCallbackVdImg

NODE_CLASS_MAPPINGS = {
    "singleVideoImgCallback": KLCallbackVdImg
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "singleVideoImgCallback": "Single Video_Img Callback"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAMES_MAPPINGS']

