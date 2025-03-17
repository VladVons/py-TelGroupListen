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

        PluginName = aConf['plugin']['name']
        Class, Err = DynImport(f'IncP.Plugin.{PluginName}', 'TPlugin' + PluginName)
        assert(Class), f'Plugin loading error {Err}'
        self.Plugin = Class(aConf['plugin'])

    async def Exec(self):
        Session = f'data/sessions/{self.Conf["session"]}'
        Params = LoadFileJson(f'{Session}.json')
        Group = self.Conf.get('group') if self.Conf.get('group') else self.Conf.get('invite_link')
        await self._Connect(f'{Session}.session', Group, Params)

    async def _Connect(self, aName: str, aGroupUser: str, aParams: dict):
        async with TelegramClient(aName, **aParams) as Client:
            await Client.start()

            Me = await Client.get_me()
            logging.info('session: %s, name: %s %s, phone: %s', aName, Me.first_name, Me.last_name, Me.phone)

            Process = psutil.Process(os.getpid())
            logging.info('Memory used: %.2f Mb', Process.memory_info().rss / (1024 * 1024))

            try:
                if ('/joinchat/' in aGroupUser):
                    Hash = aGroupUser.rsplit('/', maxsplit=1)[-1]
                    await Client(ImportChatInviteRequest(Hash))
                else:
                    await Client(JoinChannelRequest(aGroupUser))
                logging.info('Joined group')
            except Exception as E:
                logging.error('joining group: %s', E)
                return

            logging.info('Listening for messages ...')
            @Client.on(events.NewMessage())
            async def _HandleNewMessage(event):
                await self.Plugin.OnEvent(event)

            await Client.run_until_disconnected()
