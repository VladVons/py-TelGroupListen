#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import re
#
from IncP.Common import LoadFileTxt

class TPlugin():
    def __init__(self, aConf: dict):
        self.Conf = aConf

    @staticmethod
    async def GetSenderInfo(aEvent) -> dict:
        Sender = await aEvent.get_sender()
        Res = {
            'first_name': getattr(Sender, 'first_name', None),
            'last_name': getattr(Sender, 'last_name', None),
            'user_name': getattr(Sender, 'username', None),
            'time': aEvent.message.date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return Res

    @staticmethod
    def HighlightWords(aRe, aText: str) -> tuple:
        def _Highlight(aMatch):
            return f'\033[91m{aMatch.group()}\033[0m'

        Text = aRe.sub(_Highlight, aText)
        return (Text, Text.count('[0m'))

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

    async def OnEvent(self, aEvent):
        raise NotImplementedError()
