from spotware_connect import protobuf as pb


class Requests(object):

    def _sendRequest(self, proto):
        raise NotImplementedError()

    def _createRequest(self, proto_name, data):
        del data['self']
        proto = getattr(pb, proto_name)(**data)
        return self._sendRequest(proto)

    def AccountAuthReq(self, ctidTraderAccountId, accessToken):
        return self._createRequest("ProtoOAAccountAuthReq", locals())

    def AccountLogoutReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOAAccountLogoutReq", locals())

    def AmendOrderReq(self, ctidTraderAccountId, orderId, volume, limitPrice, stopPrice, expirationTimestamp, stopLoss, takeProfit, slippageInPoints, relativeStopLoss, relativeTakeProfit, guaranteedStopLoss, trailingStopLoss, stopTriggerMethod=1):
        return self._createRequest("ProtoOAAmendOrderReq", locals())

    def AmendPositionSLTPReq(self, ctidTraderAccountId, positionId, stopLoss, takeProfit, guaranteedStopLoss, trailingStopLoss, stopLossTriggerMethod=1):
        return self._createRequest("ProtoOAAmendPositionSLTPReq", locals())

    def ApplicationAuthReq(self, clientId, clientSecret):
        return self._createRequest("ProtoOAApplicationAuthReq", locals())

    def AssetClassListReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOAAssetClassListReq", locals())

    def AssetListReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOAAssetListReq", locals())

    def CancelOrderReq(self, ctidTraderAccountId, orderId):
        return self._createRequest("ProtoOACancelOrderReq", locals())

    def CashFlowHistoryListReq(self, ctidTraderAccountId, fromTimestamp, toTimestamp):
        return self._createRequest("ProtoOACashFlowHistoryListReq", locals())

    def ClosePositionReq(self, ctidTraderAccountId, positionId, volume):
        return self._createRequest("ProtoOAClosePositionReq", locals())

    def DealListReq(self, ctidTraderAccountId, fromTimestamp, toTimestamp, maxRows):
        return self._createRequest("ProtoOADealListReq", locals())

    def ExpectedMarginReq(self, ctidTraderAccountId, symbolId, volume):
        return self._createRequest("ProtoOAExpectedMarginReq", locals())

    def GetAccountListByAccessTokenReq(self, accessToken):
        return self._createRequest("ProtoOAGetAccountListByAccessTokenReq", locals())

    def GetCtidProfileByTokenReq(self, accessToken):
        return self._createRequest("ProtoOAGetCtidProfileByTokenReq", locals())

    def GetTickDataReq(self, ctidTraderAccountId, symbolId, type, fromTimestamp, toTimestamp):
        return self._createRequest("ProtoOAGetTickDataReq", locals())

    def GetTrendbarsReq(self, ctidTraderAccountId, fromTimestamp, toTimestamp, period, symbolId):
        return self._createRequest("ProtoOAGetTrendbarsReq", locals())

    def NewOrderReq(self, ctidTraderAccountId, symbolId, orderType, tradeSide, volume, limitPrice, stopPrice, expirationTimestamp, stopLoss, takeProfit, comment, baseSlippagePrice, slippageInPoints, label, positionId, clientOrderId, relativeStopLoss, relativeTakeProfit, guaranteedStopLoss, trailingStopLoss, timeInForce=2, stopTriggerMethod=1):
        return self._createRequest("ProtoOANewOrderReq", locals())

    def ReconcileReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOAReconcileReq", locals())

    def SubscribeDepthQuotesReq(self, ctidTraderAccountId, symbolId):
        return self._createRequest("ProtoOASubscribeDepthQuotesReq", locals())

    def SubscribeLiveTrendbarReq(self, ctidTraderAccountId, period, symbolId):
        return self._createRequest("ProtoOASubscribeLiveTrendbarReq", locals())

    def SubscribeSpotsReq(self, ctidTraderAccountId, symbolId):
        return self._createRequest("ProtoOASubscribeSpotsReq", locals())

    def SymbolByIdReq(self, ctidTraderAccountId, symbolId):
        return self._createRequest("ProtoOASymbolByIdReq", locals())

    def SymbolCategoryListReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOASymbolCategoryListReq", locals())

    def SymbolsForConversionReq(self, ctidTraderAccountId, firstAssetId, lastAssetId):
        return self._createRequest("ProtoOASymbolsForConversionReq", locals())

    def SymbolsListReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOASymbolsListReq", locals())

    def TraderReq(self, ctidTraderAccountId):
        return self._createRequest("ProtoOATraderReq", locals())

    def UnsubscribeDepthQuotesReq(self, ctidTraderAccountId, symbolId):
        return self._createRequest("ProtoOAUnsubscribeDepthQuotesReq", locals())

    def UnsubscribeLiveTrendbarReq(self, ctidTraderAccountId, period, symbolId):
        return self._createRequest("ProtoOAUnsubscribeLiveTrendbarReq", locals())

    def UnsubscribeSpotsReq(self, ctidTraderAccountId, symbolId):
        return self._createRequest("ProtoOAUnsubscribeSpotsReq", locals())

    def VersionReq(self, ):
        return self._createRequest("ProtoOAVersionReq", locals())

