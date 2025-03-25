# Created: 2025.03.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import logging
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
#
from IncP.Client import TClient


class TGroup(TClient):
    @staticmethod
    def ConfCheck(aConf: dict) -> dict:
        # convert compact conf format v2 into v1
        def Conf2To1() -> dict:
            Tasks = []
            for xTask in aConf['tasks']:
                Plugins = []
                for xGroup in xTask['groups']:
                    Plugins.append({
                        'group': xGroup,
                        'class': xTask['class'],
                        'event': xTask['event'],
                        'method': xTask['method'],
                        'trigger': xTask['trigger']
                    })
                Tasks.append({
                    'enabled': xTask['enabled'],
                    'session': xTask['session'],
                    'plugins': Plugins
                })
            Res = {
                'ver': 1,
                'tasks': Tasks,
                'app': aConf['app']
            }
            return Res

        if (aConf.get('ver', 1) == 2):
            aConf = Conf2To1()
            # import json
            # with open('Conf2To1.json', 'w', encoding = 'utf-8') as F:
            #     json.dump(Conf, F, indent=2, ensure_ascii=False)
        return aConf

    async def _OnSession(self, aClient):
        if (not await aClient.is_user_authorized()):
            await aClient.start(phone=self.ConfTask['phone'])

        Me = await aClient.get_me()
        logging.info('name: %s %s, phone: %s', Me.first_name, Me.last_name, Me.phone)

    async def _OnPlugin(self, aConf: dict, aClient: TelegramClient, aTClass: object) -> bool:
        ConfGroup = aConf['group']
        if ('/joinchat/' in ConfGroup):
            Hash = ConfGroup.rsplit('/', maxsplit=1)[-1]
            Join = await aClient(ImportChatInviteRequest(Hash))
        else:
            Join = await aClient(JoinChannelRequest(ConfGroup))

        # each group has own class handler
        #CurChat = Join.chats[-1]
        self._GetKeys(aConf, ['method', 'event', 'trigger'])
        aConf['trigger'] = f'{self.ConfApp["dir_triggers"]}/{aConf["trigger"]}'
        Class = aTClass(aConf, aClient)
        Method = self._GetMethod(aConf, Class)
        Event = self._GetEvent(aConf)
        aClient.add_event_handler(Method, Event(chats=ConfGroup))

        logging.info('joined group %s %s.%s()', ConfGroup, Class.__class__.__name__, Method.__name__)
