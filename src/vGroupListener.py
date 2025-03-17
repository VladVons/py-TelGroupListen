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
from IncP.Common import LoadJson, Logger

class TGroupListen():
    def __init__(self):
        self.reTriggerWords = None

    @staticmethod
    def LoadTriggerWords(aFile: str) -> set:
        with open(aFile, 'r', encoding='utf-8') as F:
            return set(
                xLine.strip()
                for xLine in F.readlines()
                if xLine.strip() and (not xLine.startswith('#'))
            )

    def HighlightTriggerWords(self, aText) -> tuple:
        def _Highlight(aMatch):
            return f'\033[91m{aMatch.group()}\033[0m'

        Text = self.reTriggerWords.sub(_Highlight, aText)
        return (Text, Text.count('[0m'))

    async def OnEvent(self, aEvent):
        Highlighted, WordsCount = self.HighlightTriggerWords(aEvent.message.text)
        if (WordsCount):
            #await asyncio.sleep(20)
            #await aEvent.respond('text of delayed response')
            pass

        Sender = await aEvent.get_sender()

        Filtered = filter(None, (Sender.first_name, Sender.last_name))
        FirstName = ' '.join(Filtered)

        UserName = f'(@{Sender.username})' if hasattr(Sender, 'username') and Sender.username else ''
        Time = aEvent.message.date.strftime('%Y-%m-%d %H:%M:%S')
        logging.info('[%s] %s %s: %s', Time, FirstName, UserName, Highlighted)

    async def Exec(self, aConf: dict):
        File = f'data/triggers/{aConf["trigger"]}'
        Words = set(self.LoadTriggerWords(File))
        Pattern = r'\b(' + '|'.join(map(re.escape, Words)) + r')\b'
        self.reTriggerWords = re.compile(Pattern, flags=re.IGNORECASE)

        Session = f'data/sessions/{aConf["session"]}'
        File = f'{Session}.json'
        Params = LoadJson(File)
        Group = aConf.get('group') if aConf.get('group') else aConf.get('invite_link')
        await self._Connect(f'{Session}.session', Group, Params)

    async def _Connect(self, aName: str, aGroupUser: str, aParams: dict):
        async with TelegramClient(aName, **aParams) as Client:
            await Client.start()

            Me = await Client.get_me()
            Logger.info('session: %s, name: %s %s, phone: %s', aName, Me.first_name, Me.last_name, Me.phone)

            Process = psutil.Process(os.getpid())
            Logger.info('Memory used: %.2f Mb', Process.memory_info().rss / (1024 * 1024))

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
                await self.OnEvent(event)

            await Client.run_until_disconnected()

async def Main(aFile: str):
    Conf = LoadJson(f'data/{aFile}')
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
