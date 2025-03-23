# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
import logging
import argparse
#
from IncP.Common import InitLog, LoadFileJson, GetAppVer


class TApp():
    def __init__(self):
        self.AppVer = GetAppVer()

    def _InitOptions(self):
        # command line parser
        Usage = f'usage: {self.AppVer['app_name']} [options] arg'
        Parser = argparse.ArgumentParser(usage = Usage)
        Parser.add_argument('-t', '--task', help='task', default='task.json')
        return Parser.parse_args()

    async def Run(self):
        Options = self._InitOptions()

        AppName = self.AppVer['app_name'].rsplit('.', maxsplit=1)[0]
        InitLog(f'{AppName}.log')

        # show version, author etc
        About = list(self.AppVer.values())
        logging.info(', '.join(About))

        # instead of static import use dynamic. IncP.ListenBot, IncP.ListenGroup, etc
        Conf = LoadFileJson(f'data/{Options.task}')
        ConfClass = Conf['app']['class']
        Module = __import__(f'IncP.{ConfClass}', fromlist=['T' + ConfClass])
        Class = getattr(Module, 'T' + ConfClass)

        # check conf version. it may supports multiple formats
        if (hasattr(Class, 'ConfCheck')):
            Conf = Class.ConfCheck(Conf)

        # create async tasks
        Tasks = []
        for xConf in Conf['tasks']:
            if (xConf.get('enabled', True)):
                Method = Class(Conf['app'], xConf).Run()
                Task = asyncio.create_task(Method)
                Tasks.append(Task)

        # run async tasks
        if (Tasks):
            await asyncio.gather(*Tasks)
        else:
            logging.warning('no tasks to execute')

MainTask = TApp().Run()
asyncio.run(MainTask)
