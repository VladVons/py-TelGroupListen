#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import os
import sys

__version__ = '1.0.1'
__date__ =  '2025.03.16'

def GetAppVer() -> dict:
    File = sys.modules['__main__'].__file__

    return {
        'app_name': os.path.basename(File),
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  'Vladimir Vons, VladVons@gmail.com'
    }
