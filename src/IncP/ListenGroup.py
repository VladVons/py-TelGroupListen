# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
#
from telethon import events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
#
from .Listen import TListen


class TListenGroup(TListen):
    @staticmethod
    def ConfCheck(aConf: dict) -> dict:
        def Conf2To1() -> dict:
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

        if (aConf.get('ver', 1) == 2):
            aConf = Conf2To1()
            # import json
            # with open('Conf2To1.json', 'w', encoding = 'utf-8') as F:
            #     json.dump(Conf, F, indent=2, ensure_ascii=False)

    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(phone=self.ConfTask['phone'])

        Me = await aClient.get_me()
        logging.info('name: %s %s, phone: %s', Me.first_name, Me.last_name, Me.phone)

    async def _OnPlugin(self, aClient, aConf: dict, aTClass: object) -> bool:
        ConfGroup = aConf['group']
        if ('/joinchat/' in ConfGroup):
            Hash = ConfGroup.rsplit('/', maxsplit=1)[-1]
            Join = await aClient(ImportChatInviteRequest(Hash))
        else:
            Join = await aClient(JoinChannelRequest(ConfGroup))

        Chat = Join.chats[-1]
        aConf['trigger'] = f'{self.ConfApp["dir_triggers"]}/{aConf["trigger"]}'
        Class = aTClass(Chat, aConf)
        EventType, Method = self._EventMethod(aConf, Class)
        aClient.add_event_handler(Method, EventType(chats=ConfGroup))

        logging.info('joined  %s', ConfGroup)
