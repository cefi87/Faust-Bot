from FaustBot.Communication import Connection
from FaustBot.Model.IRCData import IRCData
from FaustBot.Model.RemoteUser import RemoteUser
from FaustBot.Modules.MagicNumberObserverPrototype import MagicNumberObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType
from FaustBot.Modules.PingObserverPrototype import PingObserverPrototype
from FaustBot.Modules.UserList import UserList


class WhoObserver(MagicNumberObserverPrototype, PingObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, user_list: UserList):
        super().__init__()
        self.user_list = user_list
        self.pings_seen = 1
        self.pending_whos = []

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MAGIC_NUMBER, ModuleType.ON_PING]

    def update_on_magic_number(self, data: IRCData, connection):
        if data.command == '352':  # RPL_WHOREPLY
            self.input_who(data, connection)
        elif data.command == '315':  # RPL_ENDOFWHO
            self.end_who()

    def input_who(self, data, connection: Connection):
        # target #channel user host server nick status :0 gecos
        target, channel, user, host, server, nick, *ign = data.message.split(' ')
        self.pending_whos.append(RemoteUser(nick, user, host))

    def end_who(self):
        self.user_list.clear_list()
        for remuser in self.pending_whos:
            self.user_list.add_user(remuser)
        self.pending_whos = []

    def update_on_ping(self, data, connection: Connection):
        for c in connection.config.channel:
            if self.pings_seen % 90 == 0:  # 90 * 2 min = 3 Stunden
                connection.raw_send('WHO ' + c.name)
                self.pings_seen += 1
