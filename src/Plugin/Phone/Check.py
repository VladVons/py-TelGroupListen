# Created:     2025.03.19
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


import logging
from IncP.Plugin import TPlugin


class TPCheck(TPlugin):
    async def Exec(self):
        for xPhone in self.Conf['phones']:
            print(xPhone)
