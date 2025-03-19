#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import os
import asyncio
import logging
#
from IncP.Common import DbLog
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

            DbLog.Add(self.Conf['class'], self.Conf['group'], self.Chat.username, aEvent.message.text)

            #await asyncio.sleep(20)
            #await aEvent.respond('text of delayed response')

        logging.info('plugin class: %s, user: %s, total count: %d, count: %d', self.Conf['class'], self.Chat.username, gCount, self.Count)
        logging.info(aEvent.message.text)
