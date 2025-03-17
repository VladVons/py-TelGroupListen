#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import re
import logging
#
from IncP.Common import LoadFileTxt


class TPlugin():
    def __init__(self, aConf: dict):
        self.Conf = aConf

    @staticmethod
    async def GetSenderInfo(aEvent):
        Sender = await aEvent.get_sender()

        Filtered = filter(None, (Sender.first_name, Sender.last_name))
        UserName = f'(@{Sender.username})' if hasattr(Sender, 'username') and Sender.username else ''
        return {
            'first_name': ' '.join(Filtered),
            'user_name': UserName,
            'time': aEvent.message.date.strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def LoadFileWordsRe(aFile: str) -> object:
        Lines = LoadFileTxt(aFile)
        Words = set(
            xLine.strip()
            for xLine in Lines
            if xLine.strip() and (not xLine.startswith('#'))
        )

        Pattern = r'\b(' + '|'.join(map(re.escape, Words)) + r')\b'
        return re.compile(Pattern, flags=re.IGNORECASE)

    @staticmethod
    def HighlightWords(aRe, aText: str) -> tuple:
        def _Highlight(aMatch):
            return f'\033[91m{aMatch.group()}\033[0m'

        Text = aRe.sub(_Highlight, aText)
        return (Text, Text.count('[0m'))

    async def OnEvent(self, aEvent):
        raise NotImplementedError()
