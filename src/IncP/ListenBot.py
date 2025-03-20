# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
from telethon import events
#
from .Listen import TListen


class TListenBot(TListen):
    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(bot_token=self.ConfTask['bot_token'])

        Me = await aClient.get_me()
        logging.info('name: %s', Me.first_name)

    async def _OnPlugin(self, aClient, aConf: dict, aTClass: object) -> bool:
        Class = aTClass(None, aConf)

        ConfEvent = aConf.get('event', 'NewMessage')
        EventType = getattr(events, ConfEvent, None)
        assert(EventType), f'no event supported {ConfEvent}'
        aClient.add_event_handler(Class.OnEvent, EventType())
        logging.info('joined bot')
