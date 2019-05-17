from spotware_connect import protobuf as pb


class Responses(object):

    def _createResponse(self, proto_name, payload, fields):
        params = {f:getattr(payload, f) for f in fields if hasattr(payload, f)}
        method = getattr(self, proto_name)
        return method(**params)

    def AccountAuthRes_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOAAccountAuthRes not implemented")

    def AccountAuthRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("AccountAuthRes_", payload, fields)

    def AccountLogoutRes_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOAAccountLogoutRes not implemented")

    def AccountLogoutRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("AccountLogoutRes_", payload, fields)

    def ApplicationAuthRes_(self, ):
        raise NotImplementedError("ProtoOAApplicationAuthRes not implemented")

    def ApplicationAuthRes(self, payload, msgid=None):
        fields = [""]
        return self._createResponse("ApplicationAuthRes_", payload, fields)

    def AssetClassListRes_(self, ctidTraderAccountId, assetClass):
        raise NotImplementedError("ProtoOAAssetClassListRes not implemented")

    def AssetClassListRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "assetClass"]
        return self._createResponse("AssetClassListRes_", payload, fields)

    def AssetListRes_(self, ctidTraderAccountId, asset):
        raise NotImplementedError("ProtoOAAssetListRes not implemented")

    def AssetListRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "asset"]
        return self._createResponse("AssetListRes_", payload, fields)

    def CashFlowHistoryListRes_(self, ctidTraderAccountId, depositWithdraw):
        raise NotImplementedError("ProtoOACashFlowHistoryListRes not implemented")

    def CashFlowHistoryListRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "depositWithdraw"]
        return self._createResponse("CashFlowHistoryListRes_", payload, fields)

    def DealListRes_(self, ctidTraderAccountId, deal, hasMore):
        raise NotImplementedError("ProtoOADealListRes not implemented")

    def DealListRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "deal", "hasMore"]
        return self._createResponse("DealListRes_", payload, fields)

    def ErrorRes_(self, ctidTraderAccountId, errorCode, description):
        raise NotImplementedError("ProtoOAErrorRes not implemented")

    def ErrorRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "errorCode", "description"]
        return self._createResponse("ErrorRes_", payload, fields)

    def ExpectedMarginRes_(self, ctidTraderAccountId, margin):
        raise NotImplementedError("ProtoOAExpectedMarginRes not implemented")

    def ExpectedMarginRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "margin"]
        return self._createResponse("ExpectedMarginRes_", payload, fields)

    def GetAccountListByAccessTokenRes_(self, accessToken, permissionScope, ctidTraderAccount):
        raise NotImplementedError("ProtoOAGetAccountListByAccessTokenRes not implemented")

    def GetAccountListByAccessTokenRes(self, payload, msgid=None):
        fields = ["accessToken", "permissionScope", "ctidTraderAccount"]
        return self._createResponse("GetAccountListByAccessTokenRes_", payload, fields)

    def GetCtidProfileByTokenRes_(self, profile):
        raise NotImplementedError("ProtoOAGetCtidProfileByTokenRes not implemented")

    def GetCtidProfileByTokenRes(self, payload, msgid=None):
        fields = ["profile"]
        return self._createResponse("GetCtidProfileByTokenRes_", payload, fields)

    def GetTickDataRes_(self, ctidTraderAccountId, tickData, hasMore):
        raise NotImplementedError("ProtoOAGetTickDataRes not implemented")

    def GetTickDataRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "tickData", "hasMore"]
        return self._createResponse("GetTickDataRes_", payload, fields)

    def GetTrendbarsRes_(self, ctidTraderAccountId, period, timestamp, trendbar, symbolId):
        raise NotImplementedError("ProtoOAGetTrendbarsRes not implemented")

    def GetTrendbarsRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "period", "timestamp", "trendbar", "symbolId"]
        return self._createResponse("GetTrendbarsRes_", payload, fields)

    def ReconcileRes_(self, ctidTraderAccountId, position, order):
        raise NotImplementedError("ProtoOAReconcileRes not implemented")

    def ReconcileRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "position", "order"]
        return self._createResponse("ReconcileRes_", payload, fields)

    def SubscribeDepthQuotesRes_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOASubscribeDepthQuotesRes not implemented")

    def SubscribeDepthQuotesRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("SubscribeDepthQuotesRes_", payload, fields)

    def SubscribeSpotsRes_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOASubscribeSpotsRes not implemented")

    def SubscribeSpotsRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("SubscribeSpotsRes_", payload, fields)

    def SymbolByIdRes_(self, ctidTraderAccountId, symbol):
        raise NotImplementedError("ProtoOASymbolByIdRes not implemented")

    def SymbolByIdRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbol"]
        return self._createResponse("SymbolByIdRes_", payload, fields)

    def SymbolCategoryListRes_(self, ctidTraderAccountId, symbolCategory):
        raise NotImplementedError("ProtoOASymbolCategoryListRes not implemented")

    def SymbolCategoryListRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbolCategory"]
        return self._createResponse("SymbolCategoryListRes_", payload, fields)

    def SymbolsForConversionRes_(self, ctidTraderAccountId, symbol):
        raise NotImplementedError("ProtoOASymbolsForConversionRes not implemented")

    def SymbolsForConversionRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbol"]
        return self._createResponse("SymbolsForConversionRes_", payload, fields)

    def SymbolsListRes_(self, ctidTraderAccountId, symbol):
        raise NotImplementedError("ProtoOASymbolsListRes not implemented")

    def SymbolsListRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbol"]
        return self._createResponse("SymbolsListRes_", payload, fields)

    def TraderRes_(self, ctidTraderAccountId, trader):
        raise NotImplementedError("ProtoOATraderRes not implemented")

    def TraderRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "trader"]
        return self._createResponse("TraderRes_", payload, fields)

    def UnsubscribeDepthQuotesRes_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOAUnsubscribeDepthQuotesRes not implemented")

    def UnsubscribeDepthQuotesRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("UnsubscribeDepthQuotesRes_", payload, fields)

    def UnsubscribeSpotsRes_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOAUnsubscribeSpotsRes not implemented")

    def UnsubscribeSpotsRes(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("UnsubscribeSpotsRes_", payload, fields)

    def VersionRes_(self, version):
        raise NotImplementedError("ProtoOAVersionRes not implemented")

    def VersionRes(self, payload, msgid=None):
        fields = ["version"]
        return self._createResponse("VersionRes_", payload, fields)

    def AccountDisconnectEvent_(self, ctidTraderAccountId):
        raise NotImplementedError("ProtoOAAccountDisconnectEvent not implemented")

    def AccountDisconnectEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId"]
        return self._createResponse("AccountDisconnectEvent_", payload, fields)

    def AccountsTokenInvalidatedEvent_(self, ctidTraderAccountIds, reason):
        raise NotImplementedError("ProtoOAAccountsTokenInvalidatedEvent not implemented")

    def AccountsTokenInvalidatedEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountIds", "reason"]
        return self._createResponse("AccountsTokenInvalidatedEvent_", payload, fields)

    def ClientDisconnectEvent_(self, reason):
        raise NotImplementedError("ProtoOAClientDisconnectEvent not implemented")

    def ClientDisconnectEvent(self, payload, msgid=None):
        fields = ["reason"]
        return self._createResponse("ClientDisconnectEvent_", payload, fields)

    def DepthEvent_(self, ctidTraderAccountId, symbolId, newQuotes, deletedQuotes):
        raise NotImplementedError("ProtoOADepthEvent not implemented")

    def DepthEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbolId", "newQuotes", "deletedQuotes"]
        return self._createResponse("DepthEvent_", payload, fields)

    def ExecutionEvent_(self, ctidTraderAccountId, executionType, position, order, deal, bonusDepositWithdraw, depositWithdraw, errorCode, isServerEvent):
        raise NotImplementedError("ProtoOAExecutionEvent not implemented")

    def ExecutionEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "executionType", "position", "order", "deal", "bonusDepositWithdraw", "depositWithdraw", "errorCode", "isServerEvent"]
        return self._createResponse("ExecutionEvent_", payload, fields)

    def MarginChangedEvent_(self, ctidTraderAccountId, positionId, usedMargin):
        raise NotImplementedError("ProtoOAMarginChangedEvent not implemented")

    def MarginChangedEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "positionId", "usedMargin"]
        return self._createResponse("MarginChangedEvent_", payload, fields)

    def OrderErrorEvent_(self, ctidTraderAccountId, errorCode, orderId, positionId, description):
        raise NotImplementedError("ProtoOAOrderErrorEvent not implemented")

    def OrderErrorEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "errorCode", "orderId", "positionId", "description"]
        return self._createResponse("OrderErrorEvent_", payload, fields)

    def SpotEvent_(self, ctidTraderAccountId, symbolId, bid, ask, trendbar):
        raise NotImplementedError("ProtoOASpotEvent not implemented")

    def SpotEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbolId", "bid", "ask", "trendbar"]
        return self._createResponse("SpotEvent_", payload, fields)

    def SymbolChangedEvent_(self, ctidTraderAccountId, symbolId):
        raise NotImplementedError("ProtoOASymbolChangedEvent not implemented")

    def SymbolChangedEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "symbolId"]
        return self._createResponse("SymbolChangedEvent_", payload, fields)

    def TraderUpdatedEvent_(self, ctidTraderAccountId, trader):
        raise NotImplementedError("ProtoOATraderUpdatedEvent not implemented")

    def TraderUpdatedEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "trader"]
        return self._createResponse("TraderUpdatedEvent_", payload, fields)

    def TrailingSLChangedEvent_(self, ctidTraderAccountId, positionId, orderId, stopPrice, utcLastUpdateTimestamp):
        raise NotImplementedError("ProtoOATrailingSLChangedEvent not implemented")

    def TrailingSLChangedEvent(self, payload, msgid=None):
        fields = ["ctidTraderAccountId", "positionId", "orderId", "stopPrice", "utcLastUpdateTimestamp"]
        return self._createResponse("TrailingSLChangedEvent_", payload, fields)

