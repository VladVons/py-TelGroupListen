# Created:     2025.03.17
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


import re
import asyncio
import logging
from telethon import TelegramClient
#
from IncP.Common import DbLog, LoadFileConf
from IncP.Plugin import TPlugin

gCount = 0

class TPMessageFilter(TPlugin):
    def __init__(self, aConf: dict, aClient: TelegramClient):
        super().__init__(aConf, aClient)

        self.Count = 0
        self.reTriggerWords = self.LoadFileWordsRe(aConf['trigger'])

    @staticmethod
    def HighlightWords(aRe, aText: str) -> tuple:
        def _Highlight(aMatch):
            return f'\033[91m{aMatch.group()}\033[0m'

        Text = aRe.sub(_Highlight, aText)
        return (Text, Text.count('[0m'))

    @staticmethod
    def LoadFileWordsRe(aFile: str) -> object:
        Words = LoadFileConf(aFile)
        Pattern = r'\b(' + '|'.join(map(re.escape, set(Words))) + r')\b'
        return re.compile(Pattern, flags=re.IGNORECASE)

    async def OnNewMessage(self, aEvent):
        global gCount
        gCount += 1
        self.Count += 1

        Highlighted, WordsCount = self.HighlightWords(self.reTriggerWords, aEvent.message.text)
        if (WordsCount):
            pass
            #Info = await self.GetSenderInfo(aEvent)
            #logging.info('%s: %s', self.Chat.username, Info)
            #logging.info(Highlighted)

            DbLog.Add(self.Conf['class'], self.Conf['group'], aEvent.chat.username, aEvent.message.text)

            #await asyncio.sleep(20)
            #await aEvent.respond('text of delayed response')

        logging.info('plugin class: %s, user: %s, total count: %d, count: %d', self.Conf['class'], aEvent.chat.username, gCount, self.Count)
        logging.info(aEvent.message.text)
