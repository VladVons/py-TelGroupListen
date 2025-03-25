# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
from telethon import TelegramClient
from IncP.Client import TClient


class TBot(TClient):
    def __init__(self, aConfApp: dict, aConfTask: dict):
        super().__init__(aConfApp, aConfTask)
        self.Classes = {}

    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(bot_token=self.ConfTask['bot_token'])

        Me = await aClient.get_me()
        logging.info('name: %s', Me.first_name)

    async def _OnPlugin(self, aConf: dict, aClient: TelegramClient, aTClass: object) -> bool:
        # check class unique
        ConfClass = aConf['class']
        Class = self.Classes.get(ConfClass)
        if (not Class):
            Class = aTClass(None, aConf)
            self.Classes[ConfClass] = Class

        # add event handlers callback
        Method = self._GetMethod(aConf, Class)
        Event = self._GetEvent(aConf)
        aClient.add_event_handler(Method, Event())

        logging.info('joined bot method %s.%s()', Class.__class__.__name__, Method.__name__)
