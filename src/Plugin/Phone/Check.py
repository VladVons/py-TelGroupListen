# Created:     2025.03.19
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


import logging
import asyncio
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from IncP.Plugin import TPlugin


class TPCheck(TPlugin):
    async def Exec(self):
        for xPhone in self.Conf['phones']:
            Contact = InputPhoneContact(
                client_id = 0,
                phone = xPhone,
                first_name = f'tmp {xPhone}',
                last_name = ''
            )
            Contacts = await self.Client(ImportContactsRequest([Contact]))
            await asyncio.sleep(self.Conf['sleep'])
            if (Contacts.users):
                DCR = await self.Client(DeleteContactsRequest(id=[Contacts.users[0].id]))
                User = DCR.users[0]
                await asyncio.sleep(self.Conf['sleep'])
                logging.info('phone %s is in telegram. firstname %s', xPhone, User.first_name)
            else:
                logging.info('phone %s is not in telegram', xPhone)
