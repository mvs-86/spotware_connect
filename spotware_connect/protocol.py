from datetime import datetime
from itertools import count
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet.protocol import ClientFactory
from twisted.logger import Logger
from twisted.internet import defer, task
from . import protobuf as pb


log = Logger()

class ConnectProtocol(Int32StringReceiver):
    """docstring for ConnectProtocol."""

    clock = None
    clientId = None
    clientSecret = None
    authorized = False
    version = None
    resTimeout = None

    callbackHandler = object()

    hbLoop = None
    hbLoopInterval = 10

    rpsLoop = None
    rps = 0
    rpsLoopInterval = 1.1
    rpsCounter = count(1)
    rpsLimit = 5

    defereds = dict()

    def connectionMade(self):
        super().connectionMade()

        getattr(self.callbackHandler, 'Started', lambda i: None)(self.send)

        if self.clientId and self.clientSecret:
            self.auth(self.clientId, self.clientSecret)

        if self.hbLoop and not self.hbLoop.running:
            self.hbLoop.start(self.hbLoopInterval, now=False)

        if self.rpsLoop and not self.rpsLoop.running:
            self.rpsLoop.start(self.rpsLoopInterval, now=False)

    def connectionLost(self, reason):
        super().connectionLost(reason)
        log.warn("Connection lost: {r!r}", r=reason)
        self.authorized = False
        self.defereds.clear()

        if self.hbLoop and self.hbLoop.running:
            self.hbLoop.stop()

        if self.hbLoop and self.hbLoop.running:
            self.rpsLoop.stop()

        getattr(self.callbackHandler, 'Stoped', lambda: None)()

    def send(self, payload):
        msgid = self.createMsgid(payload=payload)
        pm = pb.payload_to_message(payload, msgid)
        defered = self.createResponseDefer(msgid, payload)
        self.defereds[msgid] = defered
        self.sendString(pm.SerializeToString())
        return defered

    def sendString(self, string):
        self.rps = next(self.rpsCounter) #if self.rps < self.rpsLimit else self.rps
        if self.rpsLoop and self.rps >= self.rpsLimit:
            return self.clock.callLater(self.rpsLoopInterval/2, self.sendString, string)

        # log.info("SEND PM {s}", s=string)
        super().sendString(string)

    def createResponseDefer(self, msgid, payload):
        name = type(payload).__name__

        def canceler(d):
            log.warn("Cancel Response {name} {msgid}", msgid=msgid, name=name)
            self.defereds.pop(msgid, None)
            d.addCallback(self.getPayloadCancel(payload))
            d.callback(payload)
            return d

        def timeout(result, timeout):
            log.warn("Timeout Response {name} {msgid}: {r!r}", msgid=msgid, name=name, r=result)
            self.defereds.pop(msgid, None)
            return result

        d = defer.Deferred(canceler)
        if self.resTimeout:
            d.addTimeout(self.resTimeout, self.clock, onTimeoutCancel=timeout)
        return d

    def auth(self, clientId, secret):
        def _cb(payload):
            # log.info("Authorized App {cid}", cid=clientId)
            self.authorized = True
            return payload

        def _eb(fail, *args, **kwargs):
            log.error("Failed Authorize App {cid!r}", cid=clientId)
            self.authorized = False
            self.transport.loseConnection()
            return fail

        req = pb.ProtoOAApplicationAuthReq(
            clientId=clientId, clientSecret=secret)
        return self.send(req).addCallbacks(_cb, _eb)

    def sendHeartBeat(self):
        pm = pb.payload_to_message(pb.ProtoHeartbeatEvent())
        self.sendString(pm.SerializeToString())

    def clearRps(self):
        # if self.rpsLoop and self.rps >= self.rpsLimit:
        #     log.warn(
        #         "Request Limit reached {total} messages", total=self.rps)
        self.rps = 0
        self.rpsCounter = count(1)

    def createMsgid(self, payload=None, payloadType=None):
        assert payload or payloadType, "Expected payload or payloadType to create msgid"
        if not payloadType:
            payloadType = payload.payloadType
        ts = datetime.utcnow().timestamp()
        return "%s#%s" % (payloadType, ts)

    def stringReceived(self, data):
        pm = pb.message_from_bytes(data)

        if isinstance(pm, pb.ProtoHeartbeatEvent):
            return self.sendHeartBeat()

        if isinstance(pm, pb.ProtoErrorRes):
            return self.handleErrorRes(pm)

        msgid = pm.clientMsgId
        payload = pb.get_payload(pm)
        return self.handlePayload(msgid, pm, payload)

    def handleErrorRes(self, pm):
        e = Exception("Error received: %s" % (repr(pm), ))
        return defer.fail(e)

    def handlePayload(self, msgid, pm, payload):
        d = self.defereds.pop(msgid, None)
        d = d if d else self.createResponseDefer(msgid, payload)
        d.addCallback(self.getPayloadCb(payload))

        if not isinstance(payload, pb.ProtoOAErrorRes):
            d.addErrback(self.getPayloadEb(payload))

        if not payload:
            log.warn("Invalid Payload: {pm!r}", pm=pm)

        d.callback(payload)
        return d

    def getPayloadCb(self, payload, prefix=""):
        name = payload.__class__.__name__
        name = name.replace("ProtoOA", "")
        cbName = name + prefix

        return getattr(self.callbackHandler, cbName, lambda payload: payload)

    def getPayloadEb(self, payload):
        return self.getPayloadCb(payload, prefix="Fail")

    def getPayloadCancel(self, payload):
        return self.getPayloadCb(payload, prefix="Cancel")

    # Callback
    def ErrorRes(self, payload):
        cid = self.factory.clientId
        log.error("{cid} {e}: {desc}", cid=cid,
                  e=payload.errorCode, desc=payload.description)
        return payload


class ConnectClientFactory(ClientFactory):
    protocol = ConnectProtocol
    clientId = None
    clientSecret = None
    resTimeout = None
    callbackHandler = None
    clock = None

    def __init__(self, clientId, clientSecret, callbackHandler=None, resTimeout=5*60, clock=None):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.resTimeout = resTimeout
        self.callbackHandler = callbackHandler
        self.clock = clock

    def buildProtocol(self, addr):
        p = super().buildProtocol(addr)
        p.clock = self.clock
        p.clientId = self.clientId
        p.clientSecret = self.clientSecret
        p.resTimeout = self.resTimeout
        p.hbLoop = task.LoopingCall(p.sendHeartBeat)
        p.rpsLoop = task.LoopingCall(p.clearRps)
        p.hbLoop.clock = p.rpsLoop.clock = self.clock

        if self.callbackHandler:
            p.callbackHandler = self.callbackHandler
        else:
            p.callbackHandler = p

        return p

    def __repr__(self):
        data = (type(self).__name__, self.clientId, repr(self.callbackHandler))
        return "<%s clientId=%s callbackHandler=%s>" % data

PROXY_DEMO_HOST = "demo.ctraderapi.com"
PROXY_DEMO_PORT = 5035
PROXY_LIVE_HOST = "live.ctraderapi.com"
PROXY_LIVE_PORT = 5035

def connect(clientId, clientSecret, reactor=None, live=False, **kwargs):
    from twisted.internet.ssl import ClientContextFactory
    if not reactor:
        from twisted.internet import reactor
    host = PROXY_LIVE_HOST if live else PROXY_DEMO_HOST
    port = PROXY_LIVE_PORT if live else PROXY_DEMO_PORT
    log.info("Connection: Host {h}:{p}", h=host, p=port)
    f = ConnectClientFactory(clientId, clientSecret, **kwargs)
    f.clock = reactor
    return f, reactor.connectSSL(host, port, f, ClientContextFactory())

__all__ = ["ConnectProtocol", "ConnectClientFactory", "connect"]
