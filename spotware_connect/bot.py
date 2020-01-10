from twisted.logger import Logger
from twisted.internet import defer, task
from twisted.application import service
from . import protobuf as pb
from . import requests as req
from .protocol import connect


class BotLogger(Logger):

    def emit(self, level, format=None, **kwargs):
        if self.source and self.source not in format:
            format = "[%s] %s" % (self.source, format)

        super().emit(level, format=format, **kwargs)


class Bot(object):
    r = req.Requests()
    log = BotLogger()

    def __init__(self, name=None, clock=None):
        self.name = name or self.name
        self.clock = clock
        self.d = defer.Deferred()
        self.log = BotLogger(source=self.name)

        if not self.clock:
            from twisted.internet import reactor
            self.clock = reactor

    def Started(self, sender):
        self.log.info("Started")
        self.r = req.Requests(sender)

        if self.d.called:
            self.d = defer.Deferred()

    def Stoped(self):
        self.log.info("Stopped")
        self.req = None
        if not self.d.called:
            self.d.callback(None)

    def ApplicationAuthRes(self, payload):
        self.log.info("Autohrized Application")

    def ErrorRes(self, payload):
        if hasattr(payload, 'errorCode'):
            self.log.error("Error {e} {desc}",
                  e=payload.errorCode, desc=payload.description)
        else:
            self.log.error("Unknown Error {e!r}", e=payload)

        return payload

    def createService(self, clientId, clientSecret, reactor=None, live=False, app=None):
        service = BotService(self, clientId, clientSecret, live=live)

        if app:
            service.setServiceParent(app)

        return service

    def __repr__(self):
        return "<%s name=%s>" % (type(self).__name__, self.name)

    def __str__(self):
        return self.__repr__()


class AccountBot(Bot):

    tokens = []

    def __init__(self, tokens, name=None, clock=None):
        super().__init__(name=name, clock=clock)
        self.tokens = tokens if isinstance(tokens, list) else [str(tokens)]

    def ApplicationAuthRes(self, payload):
        super().ApplicationAuthRes(payload)
        self.log.info("Getting Accounts for tokens")
        for t in self.tokens:
            self.r.GetAccountListByAccessToken(t)

    def GetAccountListByAccessTokenRes(self, payload):
        for acc in payload.ctidTraderAccount:
            self.r.AccountAuth(acc.ctidTraderAccountId, payload.accessToken)

    def AccountAuthRes(self, payload):
        self.log.info("Autohrized Account {acc}",
                      acc=payload.ctidTraderAccountId)


class BotService(service.Service):
    def __init__(self, bot, clientId, clientSecret, live=False):
        self.bot = bot
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.live = live

    def startService(self):
        self._factory, self._port = connect(
                    self.clientId, self.clientSecret,
                    live=self.live, callbackHandler=self.bot)

    # def stopService(self):
    #     return self._port.stopListening()


__all__ = ["Bot", "BotService"]
