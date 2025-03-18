# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
import sys
import logging
import json
#
from . import __version__, __date__

def GetAppVer() -> dict:
    File = sys.modules['__main__'].__file__

    return {
        'app_name': os.path.basename(File),
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  'Vladimir Vons, VladVons@gmail.com'
    }

def InitLog(aFile: str):
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(aFile)
        ]
    )

    return logging.getLogger()

def LoadFileJson(aFile: str) -> dict:
    with open(aFile, 'r', encoding='utf8') as F:
        return json.load(F)

def LoadFileTxt(aFile: str) -> list[str]:
    with open(aFile, 'r', encoding='utf8') as F:
        return F.readlines()

def DynImport(aPath: str, aClass: str) -> tuple:
    TClass, Err = (None, None)
    try:
        Mod = __import__(aPath, None, None, [aClass])
        TClass = getattr(Mod, aClass, None)
        if (not TClass):
            Err = f'Class {aClass} not found in {aPath}'
    except ModuleNotFoundError as E:
        Err = str(E)
    return (TClass, Err)

def Conf2To1(aConf: dict):
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
