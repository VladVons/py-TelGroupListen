# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import os
import sys
import logging
import json
import sqlite3
#

__version__ = '1.0.8'
__date__ =  '2025.03.25'

gDbConn = None

def GetAppVer() -> dict:
    File = sys.modules['__main__'].__file__
    File = os.path.basename(File)
    AppName = File.rsplit('.', maxsplit=1)[0]

    return {
        'app_name': AppName,
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

def LoadFileConf(aFile: str) -> list[str]:
    Lines = LoadFileTxt(aFile)
    Res = (
        xLine.strip()
        for xLine in Lines
        if xLine.strip() and (not xLine.startswith('#'))
    )
    return Res

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

class TDbLog():
    def __init__(self):
        AppVer = GetAppVer()
        self.Conn = sqlite3.connect(AppVer['app_name'] + '.db')
        self.Cursor = self.Conn.cursor()

        self.Cursor.execute('''
            create table if not exists plugin (
                id integer primary key autoincrement,
                created text default current_timestamp,
                plugin char(32) not null,
                grp text not null,
                user char(32) not null,
                msg text,
                msg_hash char(32) unique
            )
        ''')

    def __del__(self):
        self.Conn.commit()
        self.Conn.close()

    def Add(self, aPlugin: str, aGroup: str, aUser: str, aMessage: str):
        Sql = f'''
            INSERT INTO plugin (plugin, grp, user, msg)
            VALUES ('{aPlugin}', '{aGroup}', '{aUser}', '{aMessage}')
        '''
        self.Cursor.execute(Sql)
        self.Conn.commit()

DbLog = TDbLog()
