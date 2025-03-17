#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import asyncio
import logging
#
from . import TPlugin

class TPluginRespond(TPlugin):
    def __init__(self, aConf: dict):
        super().__init__(aConf)
        self.reTriggerWords = self.LoadFileWordsRe(aConf['trigger'])

    async def OnEvent(self, aEvent):
        Highlighted, WordsCount = self.HighlightWords(self.reTriggerWords, aEvent.message.text)
        if (WordsCount):
            Info = await self.GetSenderInfo(aEvent)
            logging.info(Info)
            logging.info(Highlighted)

            #await asyncio.sleep(20)
            #await aEvent.respond('text of delayed response')
