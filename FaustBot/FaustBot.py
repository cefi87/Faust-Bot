import os

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.Config import Config
from FaustBot.Modules import ActivityObserver, IdentNickServObserver, GiveCookieObserver, LoveAndPeaceObserver, \
    FreeHugsObserver, WhoObserver, ModulePrototype, PingAnswerObserver, SeenObserver, TitleObserver, \
    UserList, WikiObserver, GiveDrinkObserver, GiveFoodObserver, ComicObserver, HelpObserver, \
    IntroductionObserver, HangmanObserver, DuckObserver, AllSeenObserver
from FaustBot.Modules.CustomUserModules import GlossaryModule, ICDObserver, ModmailObserver
from FaustBot.Modules.ModuleType import ModuleType


class FaustBot(object):
    def __init__(self, config_path: str):
        config_path = os.path.join(os.getcwd(), config_path)
        self._config = Config(config_path)
        self._connection = Connection(self._config)

    @property
    def config(self):
        return self._config

    def _setup(self):
        self._connection.establish()
        user_list = UserList.UserList()
        self.add_module(user_list)
        self.add_module(ActivityObserver.ActivityObserver())
        self.add_module(WhoObserver.WhoObserver(user_list))
        self.add_module(AllSeenObserver.AllSeenObserver(user_list))
        self.add_module(PingAnswerObserver.ModulePing())
        # self.add_module(Kicker.Kicker(user_list, self._config.idle_time))
        self.add_module(SeenObserver.SeenObserver())
        self.add_module(TitleObserver.TitleObserver())
        self.add_module(WikiObserver.WikiObserver())
        self.add_module(ModmailObserver.ModmailObserver())
        self.add_module(ICDObserver.ICDObserver())
        self.add_module(GlossaryModule.GlossaryModule(self._config))
        self.add_module(IdentNickServObserver.IdentNickServObserver())
        self.add_module(GiveDrinkObserver.GiveDrinkObserver())
        self.add_module(GiveCookieObserver.GiveCookieObserver())
        self.add_module(LoveAndPeaceObserver.LoveAndPeaceObserver())
        self.add_module(FreeHugsObserver.FreeHugsObserver())
        self.add_module(GiveFoodObserver.GiveFoodObserver())
        self.add_module(ComicObserver.ComicObserver())
        self.add_module(HangmanObserver.HangmanObserver())
        self.add_module(HelpObserver.HelpObserver())
        self.add_module(IntroductionObserver.IntroductionObserver(user_list))
        self.add_module(DuckObserver.DuckObserver())

    def run(self):
        self._setup()
        running = True
        while running:
            if not self._connection.receive():
                return

    def add_module(self, module: ModulePrototype):
        # if module.__class__.__name__ in self._config.blacklist:
        #    print(module.__class__.__name__ + " not loaded because of blacklisting")
        #    return
        for module_type in module.get_module_types():
            observable = self._get_observable_by_module_type(module_type)
            observable.add_observer(module)
        module.config = self._config

    def _get_observable_by_module_type(self, module_type: str):
        if module_type == ModuleType.ON_JOIN:
            return self._connection.join_observable

        if module_type == ModuleType.ON_LEAVE:
            return self._connection.leave_observable

        if module_type == ModuleType.ON_KICK:
            return self._connection.kick_observable

        if module_type == ModuleType.ON_MSG:
            return self._connection.priv_msg_observable

        if module_type == ModuleType.ON_NICK_CHANGE:
            return self._connection.nick_change_observable

        if module_type == ModuleType.ON_PING:
            return self._connection.ping_observable

        if module_type == ModuleType.ON_NOTICE:
            return self._connection.notice_observable

        if module_type == ModuleType.ON_MAGIC_NUMBER:
            return self._connection.magic_number_observable
