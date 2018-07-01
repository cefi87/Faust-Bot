import _thread

from FaustBot.Communication.Observable import Observable
from FaustBot.Model.IRCData import IRCData


class NickChangeObservable(Observable):
    def notify_observers(self, data: IRCData, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_nick_change, (observer, data, connection))
