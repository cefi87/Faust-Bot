from Communication.Connection import Connection
from Controler.ModulePrototype import ModuleProtoype


class ModulePing(ModuleProtoype):
    """
    A Class only reacting to pings
    """
    def update(self, data):
        msg = 'PONG ' + data['server']
        Connection.singleton().raw_send(msg)

