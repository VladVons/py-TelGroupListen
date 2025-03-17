# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import logging
import json

def GetAppName() -> str:
    ModMain = sys.modules['__main__']
    MainFile = ModMain.__file__
    return os.path.basename(MainFile)

def InitLog():
    AppName = GetAppName()
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{AppName}.log')
        ]
    )

    return logging.getLogger()

def LoadJson(aFile: str) -> dict:
    with open(aFile, 'r', encoding='utf8') as F:
        return json.load(F)

Logger = InitLog()
