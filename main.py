from PIL import Image
from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

import re
import pkg.platform.types as platform_types

"""
收到消息，输出jmcomic的漫画pdf文件
"""

# 注册插件
@register(name="jmcomic", description="收到消息，输出jmcomic的漫画pdf文件", version="0.1",
          author="idk")
class BotMessageOptimizerPlugin(Plugin):

    def __init__(self, plugin_host: PluginHost):
        super().__init__(plugin_host)
        # 匹配图片 URL 的正则表达式
        self.image_pattern = re.compile(r'!\[.*?\]\((https?://\S+)\)')

    @on(NormalMessageResponded)
    def optimize_message(self, ctx: EventContext, **kwargs): # kwargs很重要
        msg = ctx.event.text_message
        parts = []
        parts.append(platform_types.Image(path="D:/github/jm_pdfget-langbot-/img/test.png"))
        parts.append(msg)
        ctx.add_return('reply', parts)       

    def __del__(self):
        pass