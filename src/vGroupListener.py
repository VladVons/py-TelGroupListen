# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import asyncio
import logging
#
from IncP.Common import InitLog, LoadFileJson, GetAppVer
from IncP.GroupListen import TGroupListen


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
            Method = TGroupListen(xConf).Exec()
            Task = asyncio.create_task(Method)
            Tasks.append(Task)

    if (Tasks):
        await asyncio.gather(*Tasks)
    else:
        logging.warning('No tasks to execute')

Job = 'job_01.json'
asyncio.run(Main(Job))
