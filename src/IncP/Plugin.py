# Created:     2025.03.17
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


import logging
from telethon import TelegramClient


class TPlugin():
    def __init__(self, aConf: dict, aClient: TelegramClient):
        self.Conf = aConf
        self.Client = aClient

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

    async def OnEvent(self, _aEvent):
        logging.warning('called default method OnEvent()')
