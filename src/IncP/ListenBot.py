# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
from .Listen import TListen


class TListenBot(TListen):
    def __init__(self, aConfApp: dict, aConfTask: dict):
        super().__init__(aConfApp, aConfTask)
        self.Classes = {}

    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(bot_token=self.ConfTask['bot_token'])

        Me = await aClient.get_me()
        logging.info('name: %s', Me.first_name)

    async def _OnPlugin(self, aClient, aConf: dict, aTClass: object) -> bool:
        # check class unique
        ConfClass = aConf['class']
        Class = self.Classes.get(ConfClass)
        if (not Class):
            Class = aTClass(None, aConf)
            self.Classes[ConfClass] = Class

        # add event handlers callback
        EventType, Method = self._EventMethod(aConf, Class)
        aClient.add_event_handler(Method, EventType())

        logging.info('joined bot method %s.%s()', Class.__class__.__name__, Method.__name__)
