# -*- coding: utf-8 -*-

import re
import time
from datetime import datetime, timedelta
from spotware_connect import protobuf
from spotware_connect import protocol
from twisted.internet import reactor
from twisted.internet import task


class Handler(object):
    log = None
    client = None
    handlerId = None
    handleAllProtobuf = False

    def __init__(self, handlerId=None, handleAllProtobuf=False):
        self.handlerId = handlerId if handlerId else id(self)
        self.handlerName = "%s#%s" % (self.__class__.__name__, self.handlerId)
        self.handleAllProtobuf = handleAllProtobuf
        self.log = protocol.Logger(namespace=self.handlerName)

    def getProtobufFuncName(self, protoOrPayload, prefix='', suffix=''):
        name = protoOrPayload if isinstance(protoOrPayload, str) else protoOrPayload.__class__.__name__
        if name.endswith('Req'):
            return "%s%s%s%s" % (prefix, "transmit", name, suffix)
        if name.endswith('Res') or name.endswith('Event'):
            return "%s%s%s%s" % (prefix, "receive", name, suffix)
        return ""

    def callReceiver(self, msgid, proto, payload=None, fail=None, suffix=''):
        for p in [proto, payload]:
            funcName = self.getProtobufFuncName(p, suffix=suffix)
            if funcName and hasattr(self, funcName):
                func = getattr(self, funcName)
                if fail:
                    func(fail, msgid, proto, payload)
                else:
                    func(msgid, proto, payload)

    def getTransmiter(self, transmitName):
        protoName = transmitName.replace('transmit', '')
        if not protoName:
            return self.transmit
        proto = getattr(protobuf, protoName)
        t = self.transmit

        def transmitProtobuf(info=None, delay=0, **kwargs):
            return t(proto(**kwargs), info=info, delay=delay)
        return transmitProtobuf

    def handleConnected(self, *args, **kwargs):
        self.log.info("{log_namespace} Online")

    def handleDisconnected(self, *args, **kwargs):
        self.log.warn("{log_namespace} Offline")

    def handleProtobufReceived(self, result, msgid, proto, payload=None):
        protoBelongsToHandler = msgid and msgid.startswith(self.handlerName)
        if not self.handleAllProtobuf and not protoBelongsToHandler:
            return
        self.log.debug("{log_namespace} Protobuf Received [{msgid}]: {proto} ; {payload}",
                       msgid=msgid, proto=proto.clientMsgId, payload=payload.__class__.__name__)
        self.callReceiver(msgid, proto, payload)

    def handleProtobufDone(self, result, msgid, proto, payload=None):
        protoBelongsToHandler = msgid and msgid.startswith(self.handlerName)
        if not self.handleAllProtobuf and not protoBelongsToHandler:
            return
        self.log.debug("{log_namespace} Protobuf Received Complete [{msgid}]: {proto} ; {payload}",
                       msgid=msgid, proto=proto.clientMsgId, payload=payload.__class__.__name__)
        self.callReceiver(msgid, proto, payload, suffix='Done')

    def handleProtobufError(self, fail, msgid, proto, payload=None):
        self.log.error("{log_namespace} Error on Protobuf Received {msgid}, {fail}", msgid=msgid, fail=fail)
        self.callReceiver(msgid, proto, payload, fail=fail, suffix='Error')

    def handleConnectedError(self, fail, *args, **kwargs):
        self.log.error("{log_namespace} Error on Connection: {fail}:", fail=fail)

    def handleDisconnectedError(self, fail, *args, **kwargs):
        self.log.error(
            "{log_namespace} Error on Disconnection: {fail}:", fail=fail)

    def transmit(self, proto, info=None, delay=0):
        info = info if info else id(proto)
        msgid = "%s#%s#%s" % (self.handlerName, proto.__class__.__name__, info)
        reactor.callLater(delay, self.client.send, proto, msgid)
        return msgid

    def receiveProtoOAErrorRes(self, msgid, proto, payload):
        self.log.warn("{log_namespace} Error Response on Payload \"{error}\" {msgid} [{proto} {payload}]",
                      error=payload.description, msgid=msgid, proto=proto.clientMsgId, payload=payload.__class__.__name__)

    def receiveProtoErrorRes(self, msgid, proto, payload):
        self.log.warn("{log_namespace} Error Response \"{error}\" {msgid} [{proto} {payload}]",
                      error=payload.description, msgid=msgid, proto=proto.clientMsgId, payload=payload.__class__.__name__)

    def __getattr__(self, name):
        if 'transmit' in name:
            return self.getTransmiter(name)
        raise AttributeError(f"{name} is not an attribute")

    def __repr__(self):
        return self.handlerName

class AppAuthHandler(Handler):
    clientId = ""
    clientSecret = ""
    authorized = None
    version = None
    tokens = []
    accounts = dict()

    @classmethod
    def connectApp(cls, name, clientId, clientSecret, *tokens, live=False, loggers=[], **kwargs):
        app = cls(clientId, clientSecret, *tokens, handlerId=name, **kwargs)
        protocol.SpotwareConnectClientFactory.connect(handlers=[app], live=live, loggers=loggers)
        return app

    def __init__(self, clientId, clientSecret, *tokens, handlerId=None, handleAllProtobuf=False):
        super().__init__(handlerId=handlerId, handleAllProtobuf=handleAllProtobuf)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tokens = tokens

    def handleConnected(self, *args, **kwargs):
        super().handleConnected(*args, **kwargs)
        self.transmitProtoOAApplicationAuthReq(
            clientId=self.clientId, clientSecret=self.clientSecret)

    def handleDisconnected(self, *args, **kwargs):
        super().handleDisconnected(*args, **kwargs)
        self.authorized = None
        self.version = None

    def receiveProtoOAApplicationAuthRes(self, msgid, proto, payload):
        self.log.info("{log_namespace} App Authorized")
        self.authorized = True
        self.transmitProtoOAVersionReq()

    def receiveProtoOAVersionRes(self, msgid, proto, payload):
        self.log.info("{log_namespace} Version " + payload.version)
        self.version = payload.version
        for token in self.tokens:
            self.transmitProtoOAGetAccountListByAccessTokenReq(accessToken=token)

    def receiveProtoOAGetAccountListByAccessTokenRes(self, msgid, proto, payload):
        self.log.info("{log_namespace} Received {accounts} accounts for {tokenId}", accounts=len(payload.ctidTraderAccount), tokenId=payload.accessToken)
        for acc in payload.ctidTraderAccount:
            if acc.isLive ^ self.client.live:
                continue
            self.accounts[acc.ctidTraderAccountId] = self.accounts.get(acc.ctidTraderAccountId, dict())
            self.accounts[acc.ctidTraderAccountId].update(dict(token=payload.accessToken, scope=payload.permissionScope))
            self.transmitProtoOAAccountAuthReq(ctidTraderAccountId=acc.ctidTraderAccountId, accessToken=payload.accessToken)

    def receiveProtoOAAccountAuthRes(self, msgid, proto, payload):
        self.log.info("{log_namespace} Account {ctid} Authorized",
                      ctid=payload.ctidTraderAccountId)
        self.transmitProtoOATraderReq(ctidTraderAccountId=payload.ctidTraderAccountId)

    def receiveProtoOATraderRes(self, msgid, proto, payload):
        self.accounts[payload.ctidTraderAccountId]['trader'] = payload
        self.log.info("{log_namespace} Trader Account Received: {acc}", acc=payload.ctidTraderAccountId)

    def receiveProtoOAErrorRes(self, msgid, proto, payload):
        if payload.errorCode == "ALREADY_LOGGED_IN":
            self.log.debug("{log_namespace} App Already Autorized")
        else:
            super().receiveProtoOAErrorRes(msgid, proto, payload)


class SymbolsHandler(Handler):
    symbols = dict()
    symbolsLight = dict()
    symbolsIds = dict()
    symbolsFilter = "EURUSD"

    def receiveProtoOASymbolsListResError(self, fail, msgid, proto, payload):
        self.log.error("{log_namespace} Error Receiving Symbols List {msgid}", msgid=msgid)

    def receiveProtoOASymbolByIdResError(self, fail, msgid, proto, payload):
        self.log.error("{log_namespace} Error Receiving Full Symbols {msgid}", msgid=msgid)

    def receiveProtoOASymbolsListRes(self, msgid, proto, payload):
        symbolIds = dict()
        symbolsFiltered = dict()

        for sym in payload.symbol:
            if not re.match(self.symbolsFilter, sym.symbolName):
                continue
            symbolIds[sym.symbolId] = sym.symbolName
            symbolsFiltered[sym.symbolName] = sym

        ctid = payload.ctidTraderAccountId
        self.symbolsIds[ctid] = symbolIds
        self.symbolsLight[ctid] = symbolsFiltered
        self.transmitProtoOASymbolByIdReq(
            ctidTraderAccountId=ctid, symbolId=list(symbolIds.keys()))

    def receiveProtoOASymbolByIdRes(self, msgid, proto, payload):
        ctid = payload.ctidTraderAccountId
        ids = self.symbolsIds[ctid]
        symbols = {ids[sym.symbolId]: sym for sym in payload.symbol}
        self.symbols[ctid] = symbols
        self.log.info("{log_namespace} Received {symbols} symbols", symbols=len(self.symbols[ctid]))


class DealsHandler(Handler):
    DEALS_MIN_TIMESTAMP = 0
    DEALS_MAX_TIMESTAMP = 2147483646000
    DEALS_MAX_ALLOWED = 604800000

    deals = dict()

    def transmitProtoOADealListReq(self, ctidTraderAccountId, fromTimestamp, toTimestamp, maxRows=100):
        fromTimestamp = fromTimestamp.timestamp() if isinstance(fromTimestamp, datetime) else fromTimestamp
        toTimestamp = toTimestamp.timestamp() if isinstance(toTimestamp, datetime) else toTimestamp
        window = (toTimestamp - fromTimestamp) * 1000
        periods = int(window / DealsHandler.DEALS_MAX_ALLOWED) or 1
        transmiter = self.getTransmiter("transmitProtoOADealListReq")
        for i in range(periods):
            startTime = int(fromTimestamp * 1000) + i * DealsHandler.DEALS_MAX_ALLOWED
            endTime = startTime + (DealsHandler.DEALS_MAX_ALLOWED-1)
            transmiter(ctidTraderAccountId=ctidTraderAccountId, fromTimestamp=startTime,
                toTimestamp=endTime, maxRows=maxRows, delay=i/10)

    def receiveProtoOADealListResError(self, fail, msgid, proto, payload):
        self.log.error("{log_namespace} Error Receiving Deals {fail}", fail=fail)

    def receiveProtoOADealListRes(self, msgid, proto, payload):
        ctid = payload.ctidTraderAccountId
        deals = {d.dealId: d for d in payload.deal}
        self.deals[ctid] = self.deals.get(ctid, dict())
        self.deals[ctid].update(deals)
        self.log.debug("{log_namespace} Deals total {deals}", deals=len(self.deals[ctid]))


class TrendBarsHandler(Handler):
    M5_MAX_ALLOWED = 302400000
    H1_MAX_ALLOWED = 21168000000
    D1_MAX_ALLOWED = 31622400000
    MN1_MAX_ALLOWED = 158112000000
    TRENDBARS_MAX_ALLOWED = dict(M1=M5_MAX_ALLOWED, M2=M5_MAX_ALLOWED, M3=M5_MAX_ALLOWED, M4=M5_MAX_ALLOWED, M5=M5_MAX_ALLOWED,
                                M10=H1_MAX_ALLOWED, M15=H1_MAX_ALLOWED, M30=H1_MAX_ALLOWED, H1=H1_MAX_ALLOWED,
                                H4=D1_MAX_ALLOWED, H12=D1_MAX_ALLOWED, D1=D1_MAX_ALLOWED,
                                W1=MN1_MAX_ALLOWED, MN1=MN1_MAX_ALLOWED)

    trendBars = dict()

    def transmitProtoOAGetTrendbarsReq(self, ctidTraderAccountId, fromTimestamp, toTimestamp, symbolId, period='H1'):
        fromTimestamp = fromTimestamp.timestamp() if isinstance(fromTimestamp, datetime) else fromTimestamp
        toTimestamp = toTimestamp.timestamp() if isinstance(toTimestamp, datetime) else toTimestamp
        period = protobuf.ProtoOATrendbarPeriod.Value(period) if isinstance(period, str) else period
        window = (toTimestamp - fromTimestamp) * 1000
        maxAllowed = TrendBarsHandler.TRENDBARS_MAX_ALLOWED[protobuf.ProtoOATrendbarPeriod.Name(period)]
        periods = int(window / maxAllowed) + 1
        transmiter = self.getTransmiter("transmitProtoOAGetTrendbarsReq")
        for i in range(periods):
            startTime = int(fromTimestamp * 1000) + i * maxAllowed
            endTime = startTime + (maxAllowed-1)
            transmiter(ctidTraderAccountId=ctidTraderAccountId, fromTimestamp=startTime,
                toTimestamp=endTime, symbolId=symbolId, period=period, delay=i/10)

    def receiveProtoOAGetTrendbarsResError(self, fail, msgid, proto, payload):
        self.log.error("{log_namespace} Error Receiving Trendbars {fail}", fail=fail)

    def receiveProtoOAGetTrendbarsRes(self, msgid, proto, payload):
        ctid = payload.ctidTraderAccountId
        symbolId = payload.symbolId
        period = payload.period
        self.trendBars[ctid] = self.trendBars.get(ctid, dict())
        self.trendBars[ctid][symbolId] = self.trendBars[ctid].get(symbolId, dict())
        self.trendBars[ctid][symbolId][period] = self.trendBars[ctid][symbolId].get(period, dict())

        bars = {t.utcTimestampInMinutes: t for t in payload.trendbar}
        self.trendBars[ctid][symbolId][period].update(bars)
        self.log.info("{log_namespace} Trendbars for {symbolId} {bars}", symbolId=symbolId, bars=len(self.trendBars[ctid][symbolId][period]))

class MarketDataHandler(AppAuthHandler, DealsHandler, SymbolsHandler, TrendBarsHandler):
    # _loopSwap = None

    # def handleConnected(self, *args, **kwargs):
    #     super().handleConnected(*args, **kwargs)

    #     def update():
    #         if not self.authorized:
    #             return
    #         for ctid in self.accounts.keys():
    #             self.transmitProtoOASymbolsListReq(ctidTraderAccountId=ctid)
    #     if not self._loopSwap:
    #         self._loopSwap = task.LoopingCall(update)
    #         self._loopSwap.start(10)

    def receiveProtoOAAccountAuthRes(self, msgid, proto, payload):
        AppAuthHandler.receiveProtoOAAccountAuthRes(self, msgid, proto, payload)
        self.transmitProtoOASymbolsListReq(ctidTraderAccountId=payload.ctidTraderAccountId)
        # self.transmitProtoOADealListReq(payload.ctidTraderAccountId)

    # def receiveProtoOADealListRes(self, msgid, proto, payload):
    #     DealsHandler.receiveProtoOADealListRes(self, msgid, proto, payload)
    #     self.log.info("{log_namespace} Account {ctid} Deals: {deals}", ctid=payload.ctidTraderAccountId, deals=repr(payload))

    def receiveProtoOASymbolByIdRes(self, msgid, proto, payload):
        super().receiveProtoOASymbolByIdRes(msgid, proto, payload)
        ctid = payload.ctidTraderAccountId

        keys = self.symbolsIds[ctid].keys()
        symbolId = list(keys)[0]
        self.log.info("{log_namespace} Requesting trend bars for symbol {symbol}", symbol=self.symbolsIds[ctid][symbolId])

        now = datetime.now()
        start = now - timedelta(days=365*2)
        self.transmitProtoOAGetTrendbarsReq(ctid, start, now, symbolId, period='H1')


class ForexSwapBot(MarketDataHandler):
    symbolsFilter = "(USD|EUR|CAD|CHF|JPY|AUD|NZD){2}"
    swaps = dict()

    def receiveProtoOASymbolByIdResDone(self, msgid, proto, payload):
        ctid = payload.ctidTraderAccountId
        self.log.info("{log_namespace} Got {symbols} Symbols for {ctid}",
                      symbols=len(payload.symbol), ctid=ctid)

        swaps = {idx: dict(long=sym.swapLong, short=sym.swapShort) for idx, sym in self.symbols[ctid].items()}
        self.swaps[ctid] = swaps
        self.log.info("{log_namespace} Swaps {swaps}", swaps=repr(self.swaps[ctid]))
