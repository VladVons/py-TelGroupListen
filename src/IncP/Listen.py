#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import os
import asyncio
import logging
import psutil
from telethon import TelegramClient, events
from IncP.Common import LoadFileJson, DynImport


class TListen():
    def __init__(self, aConfApp: dict, aConfTask: dict):
        self.ConfTask = aConfTask
        self.ConfApp = aConfApp

    async def _OnPlugin(self, aClient, aConf, aTClass) -> bool:
        raise EnvironmentError()

    async def _OnSession(self, aClient):
        return aClient

    @staticmethod
    def _EventMethod(aConf: dict, aClass) -> tuple:
        # default 'event' is events.NewMessage()
        ConfEvent = aConf.get('event', 'NewMessage')
        EventType = getattr(events, ConfEvent, None)
        assert(EventType), f'no event supported {ConfEvent}'

        # default class 'method' is OnEvent()
        ConfMethod = aConf.get('method', 'OnEvent')
        Method = getattr(aClass, ConfMethod, None)
        assert(Method), f'no method supported {ConfMethod}'

        return (EventType, Method)

    async def _Session(self, aName: str, aParams: dict):
        logging.info('session: %s %s', aName, self.ConfTask.get('comment', ''))

        Client = TelegramClient(aName, **aParams)
        await Client.connect()
        await self._OnSession(Client)

        PluginCount = 0
        for xConf in self.ConfTask.get('plugins', []):
            if (xConf.get('enabled', True)):
                ConfClass = xConf['class']
                TClass, Err = DynImport(f'IncP.Plugin.{ConfClass}', 'TPlugin' + ConfClass)
                assert(TClass), f'plugin loading error {Err}'
                try:
                    await self._OnPlugin(Client, xConf, TClass)
                    PluginCount += 1
                except Exception as E:
                    logging.error('add plugin: %s', E)

        if (PluginCount):
            while True:
                logging.info('listening session %s for events ...', aName)
                try:
                    await Client.run_until_disconnected()
                except Exception as E:
                    logging.critical('exception: %s', E)
                    await asyncio.sleep(30)
        else:
            logging.warning('no plugins loaded')

    async def Run(self):
        Process = psutil.Process(os.getpid())
        logging.info('memory used: %.2f Mb', Process.memory_info().rss / (1024 ** 2))

        Session = f'{self.ConfApp["dir_sessions"]}/{self.ConfTask["session"]}'
        Params = LoadFileJson(f'{Session}.json')
        await self._Session(Session, Params)
