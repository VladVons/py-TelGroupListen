# Created:     2025.03.17
# Author:      Vladimir Vons <VladVons@gmail.com>
# License:     GNU, see LICENSE for more details


import logging
import hashlib
#
from IncP.Common import DbLog
from IncP.Plugin import TPlugin


class TPMessageUniq(TPlugin):
    async def OnNewMessage(self, aEvent):
        Sender = await aEvent.get_sender()
        UserSender = Sender.username if Sender.username else Sender.id
        UserChat = aEvent.chat.username if aEvent.chat.username else aEvent.chat.id

        Text = aEvent.message.text
        Hash = hashlib.md5(Text.encode('utf-8')).hexdigest()
        SQL = f'''
            insert or ignore into plugin
            (plugin, grp, user, msg, msg_hash)
            values ('MessageUniq', '{UserChat}', '{UserSender}', '{Text}', '{Hash}')
        '''
        DbLog.Cursor.execute(SQL)
        DbLog.Conn.commit()
        logging.info('from %s, to %s', UserSender, UserChat)
