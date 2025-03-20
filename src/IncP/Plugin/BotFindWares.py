#Created:     2025.03.19
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


from . import TPlugin

class TPluginBotFindWares(TPlugin):
    def __init__(self, aChat, aConf: dict):
        super().__init__(aConf)
        self.Chat = aChat

    async def OnEvent(self, aEvent):
        print('got it')
        pass
