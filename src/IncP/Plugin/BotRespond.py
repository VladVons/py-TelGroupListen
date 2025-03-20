#Created:     2025.03.19
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import logging
from telethon.tl.custom import Button
from . import TPlugin


class TPluginBotRespond(TPlugin):
    def __init__(self, aChat, aConf: dict):
        super().__init__(aConf)

        self.Buttons = [
            [Button.inline('🔍 Пошук', b'search')],
            [Button.inline('ℹ️ Інформація', b'info'), Button.inline('⚙️ Налаштування', b'settings')]
        ]

    async def OnNewMessage(self, aEvent):
        logging.info('got it: %s', aEvent.message.text)
        match aEvent.message.text.strip():
            case '/start':
                await aEvent.respond('Оберіть дію:', buttons=self.Buttons)
            case _:
                await aEvent.respond(f'Отримав: {aEvent.message.text}')

    async def OnCallbackQuery(self, aEvent):
        Data = aEvent.data.decode("utf-8")
        logging.info('got it: %s', Data)
        match Data:
            case 'search':
                await aEvent.answer('🔍 Ви обрали - Пошук')
                await aEvent.respond('Пошук')
            case _:
                await aEvent.answer('Ви обрали щось інше')
