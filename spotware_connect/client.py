from itertools import count
from twisted.internet import defer, task, reactor
from twisted.protocols import basic
from twisted.logger import Logger
from spotware_connect import protobuf as pb
from spotware_connect.protocol import ProtoMessageProtocol
from spotware_connect.requests import Requests
from spotware_connect.responses import Responses

PROXY_DEMO_HOST = "demo.ctraderapi.com"
PROXY_DEMO_PORT = 5035
PROXY_LIVE_HOST = "live.ctraderapi.com"
PROXY_LIVE_PORT = 5035
log = Logger()


def connect(reactor, client, live=False):
    from twisted.internet import protocol, endpoints
    host = PROXY_LIVE_HOST if live else PROXY_DEMO_HOST
    port = PROXY_LIVE_PORT if live else PROXY_DEMO_PORT
    strport = f"ssl:{host}:{port}"
    log.info("Connection to Spotware '{con}'", con=("LIVE" if live else "DEMO"))
    endpoint = endpoints.clientFromString(reactor, strport)
    factory = protocol.Factory.forProtocol(client)
    return endpoint.connect(factory)


class HeartBeat(ProtoMessageProtocol):
    _hbLoop = None
    heartbeatInterval = 10

    def _createHeartbeat(self):
        return task.LoopingCall(self._sendHeartbeat)

    def _sendHeartbeat(self):
        hb = pb.ProtoHeartbeatEvent()
        self.sendMessage(hb)

    def stopHeartbeat(self):
        if self._hbLoop is not None:
            self._hbLoop.stop()
        self._hbLoop = None

    def startHeartbeat(self):
        self.stopHeartbeat()
        if self.heartbeatInterval is None:
            return
        self._hbLoop = self._createHeartbeat()
        self._hbLoop.start(self.heartbeatInterval, now=False)


class RPSLimiter(object):
    _rpsLoop = None
    _rpsLimit = None
    _rpsCounter = None
    _rpsTotal = 0
    _rpsRetryInterval = 0.5
    _rpsInterval = 1
    _rpsDefaultLimit = 25

    def getRpsLimit(self):
        return self._rpsLimit or self._rpsDefaultLimit

    def setRpsLimit(self, value):
        self._rpsLimit = int(value)
        if self._rpsLoop:
            self.startRpsLimit()

    rpsLimit = property(getRpsLimit, setRpsLimit)

    @property
    def rps(self):
        return self._rpsTotal

    def _incrementRps(self):
        if self._rpsTotal >= self.rpsLimit:
            return False
        self._rpsTotal = next(self._rpsCounter)
        return self._rpsTotal

    def _createRpsLimitClear(self):
        return task.LoopingCall(self._clearRpsCounter)

    def _clearRpsCounter(self):
        if self._rpsTotal > 0:
            log.info("Messages sent: {total}", total=self._rpsTotal)
        self._rpsTotal = 0
        self._rpsCounter = count(1)

    def stopRpsLimit(self):
        if self._rpsLoop is not None:
            self._rpsLoop.stop()
        self._rpsLoop = None

    def startRpsLimit(self):
        self.stopRpsLimit()
        if self.rps is None:
            return
        self._rpsLoop = self._createRpsLimitClear()
        self._rpsLoop.start(self._rpsInterval, now=True)

    @property
    def rpsAllowed(self):
        return self._incrementRps()

class ConnectClient(HeartBeat, Requests, Responses, RPSLimiter):

    @classmethod
    def connect(cls, reactor, live=False):
        return connect(reactor, cls, live=live)

    def connectionMade(self):
        basic.Int32StringReceiver.connectionMade(self)
        self.startHeartbeat()
        self.startRpsLimit()

    def connectionLost(self, reason):
        basic.Int32StringReceiver.connectionLost(self, reason)
        self.stopHeartbeat()
        self.stopRpsLimit()

    # Payload Request with RPS Limiting
    def _sendRequest(self, proto):
        if not self.rpsAllowed:
            return reactor.callLater(self._rpsRetryInterval, self._sendRequest, proto)
        d = defer.Deferred()
        d.addCallback(self.sendMessage)
        d.addErrback(self._sendRequestError)
        return d.callback(proto)

    def _sendRequestError(self, fail, payload, msgid=None):
        log.error("Error sending {payload}: {fail}", payload=payload.__class__.__name__, fail=fail)

    def _sendHeartbeat(self):
        self._sendRequest(pb.ProtoHeartbeatEvent())

    # Payload Callback Handle
    def _getPayloadCallback(self, payload, prefix=""):
        name = payload.__class__.__name__
        name = name.replace("ProtoOA", "")
        cbName = name + prefix
        if hasattr(self, cbName):
            return getattr(self, cbName)

    def _getPayloadCallbackError(self, payload):
        return self._getPayloadCallback(payload, prefix="Error")

    def onPayload(self, msgid, payload):
        cb = self._getPayloadCallback(payload)
        if not cb:
            cb = self._noCallback

        eb = self._getPayloadCallbackError(payload)
        if not eb:
            eb = self._defaultErrorBack

        d = defer.Deferred()
        d.addCallback(cb, msgid=msgid)
        d.addErrback(eb, payload=payload, msgid=msgid)
        return d.callback(payload)

    def _noCallback(self, payload, msgid=None):
        log.warn("No callback for {payload}", payload=payload.__class__.__name__)

    def _defaultErrorBack(self, fail, payload, msgid=None):
        if fail.type is NotImplementedError:
            log.warn(str(fail.value))
        else:
            log.error("Failure on payload: {fail}", fail=fail)

    # User Defined Callbacks
    def ErrorRes_(self, ctidTraderAccountId, errorCode, description):
        data = (ctidTraderAccountId, errorCode, description)
        raise Exception("Error response account %s code %s: %s" % data)

    # def VersionRes_(self, version):
    #     log.info("Version {v}", v=version)

    def wait(self, seconds=5):
        self.VersionReq()
        d = defer.Deferred(lambda c: c.callback("Wait complete"))
        d.addTimeout(seconds, reactor)
        return d
