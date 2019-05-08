# -*- coding: utf-8 -*-

import random
from collections import namedtuple
from spotware_connect import protobuf
from spotware_connect import protocol
from twisted.internet import reactor

Account = namedtuple('Account', ['token', 'ctid', 'traderLogin', 'authorized',
                                 'canTrade', 'expire'],
                        defaults=dict(canTrade=False, authorized=False, expire=''))

class Handler(object):
    log = protocol.Logger()
    client = None
    authorized = False
    version = None
    handleAllProtobuf = False
    handlerId= None
    clientId = None
    clientSecret = None
    accountsTokens = []
    accounts = dict()

    def __init__(self, clientId=None, clientSecret=None,
                 accountsTokens=[], handlerId=None, handleAllProtobuf=False):
        self.handlerId = handlerId if handlerId else random.randint(100, 999)
        self.handlerName = "%s#%s" % (self.__class__.__name__, self.handlerId)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.handleAllProtobuf = handleAllProtobuf
        self.accountsTokens = list(accountsTokens)

    def addAccountsTokens(self, *tokens):
        self.accountsTokens += list(tokens)
        self.getAccountsByTokens(*tokens)

    def handleConnected(self, *args, **kwargs):
        self.log.info("{log_namespace} Online")
        self.getVersion()
        if self.clientId and self.clientSecret:
            self.auth(self.clientId, self.clientSecret)

    def handleDisconnected(self, *args, **kwargs):
        self.log.warn("{log_namespace} Offline")

    def handleProtobufReceived(self, result, msgid, proto, payload=None):
        if not self.handleAllProtobuf and msgid and not msgid.startswith(self.handlerName):
            return
        self.log.debug("{log_namespace} Protobuf Received {msgid}: {proto} ; {payload}",
                       msgid=msgid, proto=protobuf.print(proto), payload=protobuf.print(payload))
        self.callIfProtobuf(self.authReceived, 'ProtoOAApplicationAuthRes', payload)
        self.callIfProtobuf(self.versionReceived, 'ProtoOAVersionRes', payload)
        self.callIfProtobuf(self.accountListReceived,
                            'ProtoOAGetAccountListByAccessTokenRes', payload)
        self.callIfProtobuf(self.authAccountReceived,
                            'ProtoOAAccountAuthRes', payload)

    def callIfProtobuf(self, func, protobufCls, protoOrPayload, *args, **kwargs):
        if isinstance(protobufCls, str):
            protobufCls = getattr(protobuf, protobufCls)
        if isinstance(protoOrPayload, protobufCls):
            return func(protoOrPayload, *args, **kwargs)

    def handleProtobufError(self, fail, msgid, proto, payload=None):
        self.treatError(fail, msgid=msgid, proto=proto, payload=payload)

    def handleConnectedError(self, fail, *args, **kwargs):
        self.treatError(fail, *args, **kwargs)

    def handleDisconnectedError(self, fail, *args, **kwargs):
        self.treatError(fail, *args, **kwargs)

    def treatError(self, fail, *args, **kwargs):
        self.log.error("{log_namespace} Error: {fail}\nargs={args}\nkwargs={kwargs}",
                       fail=fail, args=args, kwargs=kwargs)

    def handleProtobufReceivedError(self, fail, *args, msgid=None, proto=None, payload=None):
        self.log.error(
            "{log_namespace} Protobuf Received Error {fail}", fail=fail)

    def transmit(self, protobuf, info=None):
        info = info if info else random.randint(10000, 99999)
        msgid = "%s#%s" % (self.handlerName, info)
        reactor.callLater(0, self.client.send, protobuf, msgid)
        return msgid

    def auth(self, clientId, clientSecret):
        self.transmit(protobuf.ProtoOAApplicationAuthReq(
            clientId=clientId, clientSecret=clientSecret))

    def authReceived(self, payload):
        self.log.info("{log_namespace} Authorized")
        self.authorized = True
        self.getAccountsByTokens(*self.accountsTokens)

    def getAccountsByTokens(self, *tokens):
        for token in tokens:
            self.transmit(protobuf.ProtoOAGetAccountListByAccessTokenReq(accessToken=token))

    def accountListReceived(self, payload):
        for ctid_acc in payload.ctidTraderAccount:
            if ctid_acc.isLive and not self.client.live:
                continue
            acc = self.accounts.get(ctid_acc.ctidTraderAccountId, None)
            if not acc:
                acc = Account(
                    ctid=ctid_acc.ctidTraderAccountId, token=payload.accessToken,
                    canTrade=(payload.permissionScope == 'SCOPE_TRADE'),
                    traderLogin=ctid_acc.traderLogin)
            self.accounts[ctid_acc.ctidTraderAccountId] = acc
            self.authAccount(acc.ctid, acc.token)

    def authAccount(self, ctid, token, info=None):
        self.transmit(protobuf.ProtoOAAccountAuthReq(
            ctidTraderAccountId=ctid, accessToken=token), info)

    def authAccountReceived(self, payload):
        ctid = payload.ctidTraderAccountId
        self.log.info("Account Authorized {ctid}", ctid=ctid)
        acc = self.accounts.get(ctid, None)
        if not acc:
            self.log.warn('Account {ctid} not found', ctid=ctid)
            return
        self.accounts[ctid] = acc._replace(authorized=True)

    def getVersion(self):
        self.transmit(protobuf.ProtoOAVersionReq())

    def versionReceived(self, payload):
        self.version = payload.version

    def __repr__(self):
        fields_names = ["authorized", "clientId", "clientSecret", "accountsTokens",
                        "version", "accounts", "handleAllProtobuf"]
        fields_repr = ["%s=%s" % (fn, repr(getattr(self, fn))) for fn in fields_names]
        return "%s(%s)" % (self.handlerName, fields_repr)
