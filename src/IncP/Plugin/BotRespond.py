#Created:     2025.03.19
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import os
import asyncio
import logging
#
from IncP.Common import DbLog
from . import TPlugin

gCount = 0

class TPluginBotRespond(TPlugin):
    def __init__(self, aChat, aConf: dict):
        super().__init__(aConf)

    async def OnEvent(self, aEvent):
        logging.info(f'got it: {aEvent.message.text}')
        await aEvent.respond(f'got it: {aEvent.message.text}')