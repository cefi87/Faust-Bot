import _thread

from FaustBot.Communication.Connection import Connection
from FaustBot.Communication.Observable import Observable
from FaustBot.Model.IRCData import IRCData


class PrivmsgObservable(Observable):
    def notify_observers(self, data: IRCData, connection: Connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_priv_msg, (observer, data, connection))
