# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import logging
import psutil
#
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
#
from IncP.Common import LoadFileJson, DynImport


class TGroupListen():
    def __init__(self, aConf: dict):
        self.Conf = aConf

    async def _AddPlugin(self, aClient, aConf: dict) -> bool:
        ConfGroup = aConf['group']
        try:
            if ('/joinchat/' in ConfGroup):
                Hash = ConfGroup.rsplit('/', maxsplit=1)[-1]
                Join = await aClient(ImportChatInviteRequest(Hash))
            else:
                Join = await aClient(JoinChannelRequest(ConfGroup))

            ConfClass = aConf['class']
            TClass, Err = DynImport(f'IncP.Plugin.{ConfClass}', 'TPlugin' + ConfClass)
            assert(TClass), f'plugin loading error {Err}'
            Chat = Join.chats[-1]
            Class = TClass(Chat, aConf)

            ConfEvent = aConf.get('event', 'NewMessage')
            EventType = getattr(events, ConfEvent, None)
            assert(EventType), f'no event supported {ConfEvent}'
            aClient.add_event_handler(Class.OnEvent, EventType(chats=ConfGroup))

            logging.info('joined group %s', ConfGroup)
            return True
        except Exception as E:
            logging.error('joining group: %s. %s', ConfGroup, E)

    async def _Session(self, aName: str, aParams: dict):
        async with TelegramClient(aName, **aParams) as Client:
            Me = await Client.get_me()
            logging.info('session: %s, name: %s %s, phone: %s', aName, Me.first_name, Me.last_name, Me.phone)

            Groups = set()
            for xConf in self.Conf['plugins']:
                if (xConf.get('enabled', True)):
                    Group = xConf['group'].lower()
                    if (Group in Groups):
                        logging.warning('group already exists %s', Group)
                    Groups.add(Group)

                    await self._AddPlugin(Client, xConf)

            logging.info('listening for events ...')
            await Client.run_until_disconnected()

    async def Run(self):
        Process = psutil.Process(os.getpid())
        logging.info('memory used: %.2f Mb', Process.memory_info().rss / (1024 ** 2))

        Session = f'data/sessions/{self.Conf["session"]}'
        Params = LoadFileJson(f'{Session}.json')
        await self._Session(f'{Session}.session', Params)
