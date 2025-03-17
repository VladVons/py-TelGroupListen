# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
import re
import asyncio
import logging
import psutil
#
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
#
from IncP.Common import InitLog, LoadFileJson, LoadFileTxt, GetAppVer, DynImport

class TGroupListen():
    def __init__(self):
        self.reTriggerWords = None
        self.Plugin = None

    async def Exec(self, aConf: dict):
        PluginName = aConf['plugin']['name']
        Class, Err = DynImport(f'IncP.Plugin.{PluginName}', 'TPlugin' + PluginName)
        assert(Class), f'Plugin loading error {Err}'
        self.Plugin = Class(aConf['plugin'])

        Session = f'data/sessions/{aConf["session"]}'
        Params = LoadFileJson(f'{Session}.json')
        Group = aConf.get('group') if aConf.get('group') else aConf.get('invite_link')
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
            async def HandleNewMessage(event):
                await self.Plugin.OnEvent(event)

            await Client.run_until_disconnected()

async def Main(aFile: str):
    AppVer = GetAppVer()
    AppName = AppVer["app_name"].rsplit('.', maxsplit=1)[0]
    InitLog(f'{AppName}.log')

    Values = list(AppVer.values())
    logging.info(', '.join(Values))

    Conf = LoadFileJson(f'data/{aFile}')
    Tasks = []
    for xConf in Conf:
        if (xConf.get('enabled', True)):
            Method = TGroupListen().Exec(xConf)
            Task = asyncio.create_task(Method)
            Tasks.append(Task)

    if (Tasks):
        await asyncio.gather(*Tasks)
    else:
        logging.warning('No tasks to execute')

Job = 'job_01.json'
asyncio.run(Main(Job))
