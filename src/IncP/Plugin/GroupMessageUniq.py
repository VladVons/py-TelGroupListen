#Created:     2025.03.17
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import logging
import hashlib

#
from IncP.Common import DbLog
from . import TPlugin

class TPluginGroupMessageUniq(TPlugin):
    def __init__(self, aChat, aConf: dict):
        super().__init__(aConf)
        self.Chat = aChat

    async def OnNewMessage(self, aEvent):
        Sender = await aEvent.get_sender()
        Text = aEvent.message.text
        Hash = hashlib.md5(Text.encode('utf-8')).hexdigest()
        User = Sender.username if Sender.username else Sender.id
        SQL = f'''
            INSERT OR IGNORE INTO plugin
            (plugin, grp, user, msg, msg_hash)
            VALUES ('MessageUniq', '{aEvent.chat.username}', '{User}', '{Text}', '{Hash}')
        '''
        DbLog.Cursor.execute(SQL)
        DbLog.Conn.commit()
