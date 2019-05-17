from datetime import datetime
from twisted.protocols import basic
from spotware_connect import protobuf as pb


class ProtoMessageSender(object):
    def sendMessage(self, payload=None, payloadType=None, msgid=None):
        if not msgid:
            msgid = self.createMsgid(payload=payload, payloadType=payloadType)
        pm = pb.payload_to_message(payload, msgid)
        self._sendData(pm)
        return (payload, msgid)

    def createMsgid(self, payload=None, payloadType=None):
        if not payloadType:
            payloadType = payload.payloadType
        ts = datetime.utcnow().timestamp()
        return "%s#%s" % (payloadType, ts)

    def _sendData(self, proto):
        raise NotImplementedError()


class ProtoMessageReceiver(object):
    def onReceive(self, pm):

        if isinstance(pm, pb.ProtoHeartbeatEvent):
            return self.onHeartBeat(pm)

        if isinstance(pm, pb.ProtoErrorRes):
            return self.onError(pm)

        payload = pb.get_payload(pm)
        self.onPayload(pm.clientMsgId, payload)

    def onHeartBeat(self, pm):
        pass

    def onError(self, pm):
        raise Exception("Error response: " + repr(pm))

    def onPayload(self, msgid, payload):
        raise NotImplementedError()


class ProtoMessageProtocol(basic.Int32StringReceiver, ProtoMessageReceiver, ProtoMessageSender):
    """docstring for ProtoMessageProtocol."""

    def stringReceived(self, data):
        pm = pb.message_from_bytes(data)
        self.onReceive(pm)

    def _sendData(self, proto):
        self.sendString(proto.SerializeToString())

    def onHeartBeat(self, pm):
        self.sendProtoBuf(pm)

# class SpotwareConnectClientFactory(protocol.ReconnectingClientFactory):
#     """docstring for SpotwareConnectClientFactory."""
#     protocol = ProtobufProtocol
#     log = None
#     online = False
#     connectedProtocol = None
#     handlers = []
#     maxDelay = 5*60
#     live = False

#     def __init__(self, *handlers, maxSendRetries=5, live=False):
#         self.live = live
#         self.maxSendRetries = maxSendRetries
#         self.addHandlers(*handlers)
#         self.log = Logger(namespace="SpotwareConnectClientFactory")

#     def startedConnecting(self, connector):
#         self.log.debug("{log_namespace} Connection Starting")
#         super().startedConnecting(connector)

#     def clientConnectionLost(self, connector, reason):
#         self.log.debug("{log_namespace} Connection Lost, reconecting")
#         super().clientConnectionFailed(connector, reason)

#     def clientConnectionFailed(self, connector, reason):
#         self.log.debug("{log_namespace} Connection Failed, reconecting")
#         super().clientConnectionFailed(connector, reason)

#     def addHandlers(self, *handlers):
#         for h in handlers:
#             h.client = self
#             self.handlers.append(h)

#     def connected(self):
#         self.log.info("{log_namespace} Connected {type}", type=('LIVE' if self.live else 'DEMO'))
#         self.resetDelay()
#         self.online = True
#         self.dispatchToHandlers("handleConnected", "handleConnectedError", "handleConnectedDone")

#     def disconnected(self):
#         self.log.warn("{log_namespace} Spotware Disconnected")
#         self.online = False
#         self.dispatchToHandlers(
#             "handleDisconnected", "handleDisconnectedError", "handleDisconnectedDone")

#     def send(self, payload, msgid, retry=0):
#         # if not self.online or not self.connectedProtocol:
#         #     self.log.warn('{log_namespace} Failed to send {payload}, resendind in {delay}',
#         #                   payload=payload.__class__.__name__, delay=self.delay)
#         #     if retry < self.maxSendRetries:
#         #         reactor.callLater(self.delay+1, self.send, payload, msgid, retry+1)
#         #     return

#         self.log.debug("{log_namespace} Sending Protobuf {payload}", payload=payload.__class__.__name__)
#         if isinstance(payload, pb.ProtoHeartbeatEvent) or isinstance(payload, pb.ProtoMessage):
#             self.connectedProtocol.sendProtoMessage(payload)
#         else:
#             self.connectedProtocol.sendProtoBuf(payload, msgid)

#     def handleProtoBufReceived(self, msgid, proto, payload):

#         self.log.debug(
#             '{log_namespace} Dispatching ProtoBuf Received {proto}', proto=proto.clientMsgId)
#         self.dispatchToHandlers(
#             "handleProtobufReceived", "handleProtobufError", "handleProtobufDone",
#             msgid=msgid, proto=proto, payload=payload)

#     def dispatchToHandlers(self, callBackName='', errorCallBackName='', bothCallBackName='', result='', **kwargs):
#         defers = []
#         for h in self.handlers:
#             cb, eb, bc =  self._getHandlerCallbacks(h, callBackName, errorCallBackName, bothCallBackName)
#             d = defer.Deferred()
#             if cb:
#                 d.addCallback(cb, **kwargs)
#             if eb:
#                 d.addErrback(eb, **kwargs)
#             if bc:
#                 d.addBoth(bc, **kwargs)
#             defers.append(d)
#             reactor.callLater(0, d.callback, result)
#             # reactor.callFromThread(d.callback, result)

#     def _getHandlerCallbacks(self, handler, hCallbackName, hErrbackName, hBothName):
#         hCallback = getattr(handler, hCallbackName) if hasattr(handler, hCallbackName) else None
#         hErrback = getattr(handler, hErrbackName) if hasattr(handler, hErrbackName) else None
#         hBoth = getattr(handler, hBothName) if hasattr(handler, hBothName) else None
#         return (hCallback, hErrback, hBoth)

#     @classmethod
#     def connect(cls, live=False, handlers=[], loggers=[]):
#         from twisted.internet.ssl import ClientContextFactory
#         from twisted.logger import globalLogPublisher, STDLibLogObserver

#         for l in loggers:
#             globalLogPublisher.addObserver(l)
#         else:
#             globalLogPublisher.addObserver(STDLibLogObserver())

#         factory = cls(*handlers)
#         host = PROXY_LIVE_HOST if live else PROXY_DEMO_HOST
#         port = PROXY_LIVE_PORT if live else PROXY_DEMO_PORT
#         reactor.connectSSL(host, port, factory, ClientContextFactory())
#         return factory
