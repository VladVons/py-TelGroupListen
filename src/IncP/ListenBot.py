# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
from .Listen import TListen


class TListenBot(TListen):
    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(bot_token=self.ConfTask['bot_token'])

        Me = await aClient.get_me()
        logging.info('name: %s', Me.first_name)

    async def _OnPlugin(self, aClient, aConf: dict, aTClass: object) -> bool:
        Class = aTClass(None, aConf)
        EventType, Method = self._EventMethod(aConf, Class)
        aClient.add_event_handler(Method, EventType())

        logging.info('joined bot')
