# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import asyncio
import logging
import psutil
#
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
#
from IncP.Common import LoadFileJson, DynImport


class TGroupListen():
    def __init__(self, aConfApp: dict, aConfTask: dict):
        self.ConfTask = aConfTask
        self.ConfApp = aConfApp

    @staticmethod
    def Conf2To1(aConf: dict) -> dict:
        Tasks = []
        for xTask in aConf['tasks']:
            Plugins = []
            for xGroup in xTask['groups']:
                Plugins.append({
                    'class': xTask['class'],
                    'group': xGroup,
                    'trigger': xTask['trigger']
                })
            Tasks.append({
                'enabled': xTask['enabled'],
                'session': xTask['session'],
                'plugins': Plugins
            })
        Res = {
            'ver': 1,
            'tasks': Tasks
        }
        return Res

    async def _AddPlugin(self, aClient, aConf: dict) -> bool:
        ConfGroup = aConf['group']
        try:
            if ('/joinchat/' in ConfGroup):
                Hash = ConfGroup.rsplit('/', maxsplit=1)[-1]
                Join = await aClient(ImportChatInviteRequest(Hash))
            else:
                Join = await aClient(JoinChannelRequest(ConfGroup))

            ConfClass = aConf['class']
            Plugin = f'{self.ConfApp["dir_plugins"]}/{ConfClass}'.replace('/', '.')
            TClass, Err = DynImport(Plugin, 'TPlugin' + ConfClass)
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
            for xConf in self.ConfTask['plugins']:
                if (xConf.get('enabled', True)):
                    Group = xConf['group'].lower()
                    if (Group in Groups):
                        logging.warning('group already exists %s', Group)
                    Groups.add(Group)

                    xConf['trigger'] = f'{self.ConfApp["dir_triggers"]}/{xConf["trigger"]}'
                    await self._AddPlugin(Client, xConf)

            BaseName = aName.rsplit('/', maxsplit=1)[-1]
            if (Groups):
                while True:
                    logging.info('listening session %s for events ...', BaseName)
                    try:
                        await Client.run_until_disconnected()
                    except Exception as E:
                        logging.critical('exception: %s', E)
                        await asyncio.sleep(30)
            else:
                logging.warning('no plugins in session %s', BaseName)

    async def Run(self):
        Process = psutil.Process(os.getpid())
        logging.info('memory used: %.2f Mb', Process.memory_info().rss / (1024 ** 2))

        Session = f'{self.ConfApp["dir_sessions"]}/{self.ConfTask["session"]}'
        Params = LoadFileJson(f'{Session}.json')
        await self._Session(Session, Params)
