# Created:     2025.03.17
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


import os
import asyncio
import logging
import psutil
from telethon import TelegramClient, events
from IncP.Common import LoadFileJson, DynImport


class TClient():
    def __init__(self, aConfApp: dict, aConfTask: dict):
        self.ConfTask = aConfTask
        self.ConfApp = aConfApp

    async def _OnPlugin(self, aConf: dict, aClient: TelegramClient, aTClass: object) -> bool:
        raise EnvironmentError()

    async def _OnSession(self, aClient):
        return aClient

    def _GetKeys(self, aConf: dict, aKeys: list[str]) -> object:
        for xKey in aKeys:
            if (xKey not in aConf):
                aConf[xKey] = self.ConfTask[xKey]

    def _GetMethod(self, aConf: dict, aClass) -> object:
        ConfMethod = aConf['method']
        Res = getattr(aClass, ConfMethod, None)
        assert(Res), f'no method `{ConfMethod}` in class `{aClass.__class__.__name__}`'
        return Res

    def _GetEvent(self, aConf: dict) -> events:
        ConfEvent = aConf['event']
        Res = getattr(events, ConfEvent, None)
        assert(Res), f'no event `{ConfEvent}` supported'
        return Res

    async def _Session(self, aName: str, aParams: dict):
        logging.info('session: %s %s', aName, self.ConfTask.get('comment', ''))

        Client = TelegramClient(aName, **aParams)
        await Client.connect()
        await self._OnSession(Client)

        # dynamic plugin class loader
        PluginCount = 0
        for xConf in self.ConfTask.get('plugins', []):
            if (xConf.get('enabled', True)):
                self._GetKeys(xConf, ['class'])
                ConfClass = xConf['class']

                TClass, Err = DynImport(f'Plugin.{self.ConfApp["class"]}.{ConfClass}', 'TP' + ConfClass)
                assert(TClass), f'plugin loading error {Err}'
                try:
                    await self._OnPlugin(xConf, Client, TClass)
                    PluginCount += 1
                except Exception as E:
                    logging.error('add plugin: %s', E)

        # run eternal loop for handling prepared events
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
