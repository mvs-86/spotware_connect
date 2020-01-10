from twisted.internet import defer
from spotware_connect import protobuf as pb


class Requests(object):

    reqSendFunc = None

    def __init__(self, reqSendFunc=None):
        self.reqSendFunc = reqSendFunc

    def create(self, proto_name, data):
        del data['self']
        proto = getattr(pb, proto_name)(**data)
        return proto

    def send(self, payload):
        if not self.reqSendFunc:
            return defer.fail(Exception("No send function"))

        return defer.maybeDeferred(self.reqSendFunc, payload)

    def createAndSend(self, proto_name, data):
        proto = self.create(proto_name, data)
        return self.send(proto)

    def AccountAuth(self, ctidTraderAccountId, accessToken):
        return self.createAndSend("ProtoOAAccountAuthReq", locals())

    def AccountLogout(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOAAccountLogoutReq", locals())

    def AmendOrder(self, ctidTraderAccountId, orderId, volume, limitPrice, stopPrice, expirationTimestamp, stopLoss, takeProfit, slippageInPoints, relativeStopLoss, relativeTakeProfit, guaranteedStopLoss, trailingStopLoss, stopTriggerMethod=1):
        return self.createAndSend("ProtoOAAmendOrderReq", locals())

    def AmendPositionSLTP(self, ctidTraderAccountId, positionId, stopLoss, takeProfit, guaranteedStopLoss, trailingStopLoss, stopLossTriggerMethod=1):
        return self.createAndSend("ProtoOAAmendPositionSLTPReq", locals())

    def ApplicationAuth(self, clientId, clientSecret):
        return self.createAndSend("ProtoOAApplicationAuthReq", locals())

    def AssetClassList(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOAAssetClassListReq", locals())

    def AssetList(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOAAssetListReq", locals())

    def CancelOrder(self, ctidTraderAccountId, orderId):
        return self.createAndSend("ProtoOACancelOrderReq", locals())

    def CashFlowHistoryList(self, ctidTraderAccountId, fromTimestamp, toTimestamp):
        return self.createAndSend("ProtoOACashFlowHistoryListReq", locals())

    def ClosePosition(self, ctidTraderAccountId, positionId, volume):
        return self.createAndSend("ProtoOAClosePositionReq", locals())

    def DealList(self, ctidTraderAccountId, fromTimestamp, toTimestamp, maxRows):
        return self.createAndSend("ProtoOADealListReq", locals())

    def ExpectedMargin(self, ctidTraderAccountId, symbolId, volume):
        return self.createAndSend("ProtoOAExpectedMarginReq", locals())

    def GetAccountListByAccessToken(self, accessToken):
        return self.createAndSend("ProtoOAGetAccountListByAccessTokenReq", locals())

    def GetCtidProfileByToken(self, accessToken):
        return self.createAndSend("ProtoOAGetCtidProfileByTokenReq", locals())

    def GetTickData(self, ctidTraderAccountId, symbolId, type, fromTimestamp, toTimestamp):
        return self.createAndSend("ProtoOAGetTickDataReq", locals())

    def GetTrendbars(self, ctidTraderAccountId, fromTimestamp, toTimestamp, period, symbolId):
        return self.createAndSend("ProtoOAGetTrendbarsReq", locals())

    def MarginCallList(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOAMarginCallListReq", locals())

    def MarginCallUpdate(self, ctidTraderAccountId, marginCall):
        return self.createAndSend("ProtoOAMarginCallUpdateReq", locals())

    def NewOrder(self, ctidTraderAccountId, symbolId, orderType, tradeSide, volume, limitPrice, stopPrice, expirationTimestamp, stopLoss, takeProfit, comment, baseSlippagePrice, slippageInPoints, label, positionId, clientOrderId, relativeStopLoss, relativeTakeProfit, guaranteedStopLoss, trailingStopLoss, timeInForce=2, stopTriggerMethod=1):
        return self.createAndSend("ProtoOANewOrderReq", locals())

    def Reconcile(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOAReconcileReq", locals())

    def SubscribeDepthQuotes(self, ctidTraderAccountId, symbolId):
        return self.createAndSend("ProtoOASubscribeDepthQuotesReq", locals())

    def SubscribeLiveTrendbar(self, ctidTraderAccountId, period, symbolId):
        return self.createAndSend("ProtoOASubscribeLiveTrendbarReq", locals())

    def SubscribeSpots(self, ctidTraderAccountId, symbolId):
        return self.createAndSend("ProtoOASubscribeSpotsReq", locals())

    def SymbolById(self, ctidTraderAccountId, symbolId):
        return self.createAndSend("ProtoOASymbolByIdReq", locals())

    def SymbolCategoryList(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOASymbolCategoryListReq", locals())

    def SymbolsForConversion(self, ctidTraderAccountId, firstAssetId, lastAssetId):
        return self.createAndSend("ProtoOASymbolsForConversionReq", locals())

    def SymbolsList(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOASymbolsListReq", locals())

    def Trader(self, ctidTraderAccountId):
        return self.createAndSend("ProtoOATraderReq", locals())

    def UnsubscribeDepthQuotes(self, ctidTraderAccountId, symbolId):
        return self.createAndSend("ProtoOAUnsubscribeDepthQuotesReq", locals())

    def UnsubscribeLiveTrendbar(self, ctidTraderAccountId, period, symbolId):
        return self.createAndSend("ProtoOAUnsubscribeLiveTrendbarReq", locals())

    def UnsubscribeSpots(self, ctidTraderAccountId, symbolId):
        return self.createAndSend("ProtoOAUnsubscribeSpotsReq", locals())

    def Version(self):
        return self.createAndSend("ProtoOAVersionReq", locals())

