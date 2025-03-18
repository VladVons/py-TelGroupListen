# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import asyncio
import logging
import argparse
#
from IncP.Common import InitLog, LoadFileJson, GetAppVer, Conf2To1
from IncP.GroupListen import TGroupListen

class TApp():
    def __init__(self):
        self.AppVer = GetAppVer()

    def _InitOptions(self):
        Usage = f'usage: {self.AppVer['app_name']} [options] arg'
        Parser = argparse.ArgumentParser(usage = Usage)
        Parser.add_argument('-t', '--task', help='task', default='task.json')
        return Parser.parse_args()

    async def Run(self):
        Options = self._InitOptions()

        AppName = self.AppVer['app_name'].rsplit('.', maxsplit=1)[0]
        InitLog(f'{AppName}.log')

        About = list(self.AppVer.values())
        logging.info(', '.join(About))

        Conf = LoadFileJson(f'data/{Options.task}')
        if (Conf.get('ver', 1) == 2):
            Conf = Conf2To1(Conf)
            # with open('Conf2To1.json', 'w', encoding = 'utf-8') as F:
            #     json.dump(Conf, F, indent=2, ensure_ascii=False)

        Tasks = []
        for xConf in Conf['tasks']:
            if (xConf.get('enabled', True)):
                Method = TGroupListen(xConf).Run()
                Task = asyncio.create_task(Method)
                Tasks.append(Task)

        if (Tasks):
            await asyncio.gather(*Tasks)
        else:
            logging.warning('no tasks to execute')

asyncio.run(TApp().Run())
