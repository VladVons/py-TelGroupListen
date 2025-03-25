# Created: 2025.03.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
from telethon import TelegramClient
from IncP.Client import TClient


class TPhone(TClient):
    def __init__(self, aConfApp: dict, aConfTask: dict):
        super().__init__(aConfApp, aConfTask)
        self.Classes = {}

    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(bot_token=self.ConfTask['phone'])

        Me = await aClient.get_me()
        logging.info('name: %s', Me.first_name)

    async def _OnPlugin(self, aConf: dict, aClient: TelegramClient, aTClass: object) -> bool:
        Class = aTClass(aConf, aClient)
        Method = self._GetMethod(aConf, Class)
        await Method()
