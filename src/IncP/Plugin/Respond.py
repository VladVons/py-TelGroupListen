#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import asyncio
import logging
#
from . import TPlugin

gCount = 0

class TPluginRespond(TPlugin):
    def __init__(self, aChat, aConf: dict):
        super().__init__(aConf)
        self.Chat = aChat

        self.Count = 0
        self.reTriggerWords = self.LoadFileWordsRe(aConf['trigger'])

    async def OnEvent(self, aEvent):
        global gCount
        gCount += 1

        self.Count += 1

        Highlighted, WordsCount = self.HighlightWords(self.reTriggerWords, aEvent.message.text)
        if (WordsCount):
            pass
            #Info = await self.GetSenderInfo(aEvent)
            #logging.info('%s: %s', self.Chat.username, Info)
            #logging.info(Highlighted)

            #await asyncio.sleep(20)
            #await aEvent.respond('text of delayed response')

        print(self.Chat.username, gCount, self.Count)
        print(aEvent.message.text)
