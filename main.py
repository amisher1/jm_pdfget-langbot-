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
        
    @on(NormalMessageResponded)
    def optimize_message(self, event: EventContext):
        msg = event.event.text_message
        parts = []
        parts.append(platform_types.Image(path="D:/github/jm_pdfget-langbot-/img/test.png"))
        parts.append(msg)
        event.add_return('reply', parts)

    def __del__(self):
        pass