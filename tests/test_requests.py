from twisted.trial import unittest
from twisted.test import proto_helpers
from spotware_connect import protocol, requests
from spotware_connect import protobuf as pb

class Testspotware_connect_requests(unittest.TestCase):
    """Tests for `spotware_connect.requests` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.tr = proto_helpers.StringTransport()
        self.proto = protocol.ConnectProtocol()
        self.proto.makeConnection(self.tr)
        self.r = requests.Requests(self.proto.send)

    def _assertRequest(self, payload_type, data={}):
        payload = payload_type(**data)
        pm = pb.payload_to_message(payload)
        self.assertIn(payload.SerializeToString(), self.tr.value())

    def test_AccountAuthReq(self):
        """Test AccountAuthReq"""
        data = dict(ctidTraderAccountId=1, accessToken="X")
        d = self.r.AccountAuth(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAAccountAuthReq)
        return d

    def test_AccountLogoutReq(self):
        """Test AccountLogoutReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.AccountLogout(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAAccountLogoutReq)
        return d

    def test_AmendOrderReq(self):
        """Test AmendOrderReq"""
        data = dict(ctidTraderAccountId=1, orderId=1, volume=1, limitPrice=1, stopPrice=1, expirationTimestamp=1, stopLoss=1, takeProfit=1, slippageInPoints=1, relativeStopLoss=1, relativeTakeProfit=1, guaranteedStopLoss=1, trailingStopLoss=1, stopTriggerMethod=1)
        d = self.r.AmendOrder(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAAmendOrderReq)
        return d

    def test_AmendPositionSLTPReq(self):
        """Test AmendPositionSLTPReq"""
        data = dict(ctidTraderAccountId=1, positionId=1, stopLoss=1, takeProfit=1, guaranteedStopLoss=1, trailingStopLoss=1, stopLossTriggerMethod=1)
        d = self.r.AmendPositionSLTP(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAAmendPositionSLTPReq)
        return d

    def test_ApplicationAuthReq(self):
        """Test ApplicationAuthReq"""
        data = dict(clientId="X", clientSecret="X")
        d = self.r.ApplicationAuth(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAApplicationAuthReq)
        return d

    def test_AssetClassListReq(self):
        """Test AssetClassListReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.AssetClassList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAAssetClassListReq)
        return d

    def test_AssetListReq(self):
        """Test AssetListReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.AssetList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAAssetListReq)
        return d

    def test_CancelOrderReq(self):
        """Test CancelOrderReq"""
        data = dict(ctidTraderAccountId=1, orderId=1)
        d = self.r.CancelOrder(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOACancelOrderReq)
        return d

    def test_CashFlowHistoryListReq(self):
        """Test CashFlowHistoryListReq"""
        data = dict(ctidTraderAccountId=1, fromTimestamp=1, toTimestamp=1)
        d = self.r.CashFlowHistoryList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOACashFlowHistoryListReq)
        return d

    def test_ClosePositionReq(self):
        """Test ClosePositionReq"""
        data = dict(ctidTraderAccountId=1, positionId=1, volume=1)
        d = self.r.ClosePosition(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAClosePositionReq)
        return d

    def test_DealListReq(self):
        """Test DealListReq"""
        data = dict(ctidTraderAccountId=1, fromTimestamp=1, toTimestamp=1, maxRows=1)
        d = self.r.DealList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOADealListReq)
        return d

    def test_ExpectedMarginReq(self):
        """Test ExpectedMarginReq"""
        data = dict(ctidTraderAccountId=1, symbolId=1, volume=[1])
        d = self.r.ExpectedMargin(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAExpectedMarginReq)
        return d

    def test_GetAccountListByAccessTokenReq(self):
        """Test GetAccountListByAccessTokenReq"""
        data = dict(accessToken="X")
        d = self.r.GetAccountListByAccessToken(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAGetAccountListByAccessTokenReq)
        return d

    def test_GetCtidProfileByTokenReq(self):
        """Test GetCtidProfileByTokenReq"""
        data = dict(accessToken="X")
        d = self.r.GetCtidProfileByToken(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAGetCtidProfileByTokenReq)
        return d

    def test_GetTickDataReq(self):
        """Test GetTickDataReq"""
        data = dict(ctidTraderAccountId=1, symbolId=1, type=1, fromTimestamp=1, toTimestamp=1)
        d = self.r.GetTickData(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAGetTickDataReq)
        return d

    def test_GetTrendbarsReq(self):
        """Test GetTrendbarsReq"""
        data = dict(ctidTraderAccountId=1, fromTimestamp=1, toTimestamp=1, period=1, symbolId=1)
        d = self.r.GetTrendbars(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAGetTrendbarsReq)
        return d

    def test_MarginCallListReq(self):
        """Test MarginCallListReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.MarginCallList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAMarginCallListReq)
        return d

    def test_MarginCallUpdateReq(self):
        """Test MarginCallUpdateReq"""
        data = dict(ctidTraderAccountId=1, marginCall=pb.ProtoOAMarginCall(marginCallType=61, marginLevelThreshold=1))
        d = self.r.MarginCallUpdate(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAMarginCallUpdateReq)
        return d

    def test_NewOrderReq(self):
        """Test NewOrderReq"""
        data = dict(ctidTraderAccountId=1, symbolId=1, orderType=1, tradeSide=1, volume=1, limitPrice=1, stopPrice=1, timeInForce=2, expirationTimestamp=1, stopLoss=1, takeProfit=1, comment="X", baseSlippagePrice=1, slippageInPoints=1, label="X", positionId=1, clientOrderId="X", relativeStopLoss=1, relativeTakeProfit=1, guaranteedStopLoss=1, trailingStopLoss=1, stopTriggerMethod=1)
        d = self.r.NewOrder(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOANewOrderReq)
        return d

    def test_ReconcileReq(self):
        """Test ReconcileReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.Reconcile(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAReconcileReq)
        return d

    def test_SubscribeDepthQuotesReq(self):
        """Test SubscribeDepthQuotesReq"""
        data = dict(ctidTraderAccountId=1, symbolId=[1])
        d = self.r.SubscribeDepthQuotes(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASubscribeDepthQuotesReq)
        return d

    def test_SubscribeLiveTrendbarReq(self):
        """Test SubscribeLiveTrendbarReq"""
        data = dict(ctidTraderAccountId=1, period=1, symbolId=1)
        d = self.r.SubscribeLiveTrendbar(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASubscribeLiveTrendbarReq)
        return d

    def test_SubscribeSpotsReq(self):
        """Test SubscribeSpotsReq"""
        data = dict(ctidTraderAccountId=1, symbolId=[1])
        d = self.r.SubscribeSpots(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASubscribeSpotsReq)
        return d

    def test_SymbolByIdReq(self):
        """Test SymbolByIdReq"""
        data = dict(ctidTraderAccountId=1, symbolId=[1])
        d = self.r.SymbolById(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASymbolByIdReq)
        return d

    def test_SymbolCategoryListReq(self):
        """Test SymbolCategoryListReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.SymbolCategoryList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASymbolCategoryListReq)
        return d

    def test_SymbolsForConversionReq(self):
        """Test SymbolsForConversionReq"""
        data = dict(ctidTraderAccountId=1, firstAssetId=1, lastAssetId=1)
        d = self.r.SymbolsForConversion(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASymbolsForConversionReq)
        return d

    def test_SymbolsListReq(self):
        """Test SymbolsListReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.SymbolsList(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOASymbolsListReq)
        return d

    def test_TraderReq(self):
        """Test TraderReq"""
        data = dict(ctidTraderAccountId=1)
        d = self.r.Trader(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOATraderReq)
        return d

    def test_UnsubscribeDepthQuotesReq(self):
        """Test UnsubscribeDepthQuotesReq"""
        data = dict(ctidTraderAccountId=1, symbolId=[1])
        d = self.r.UnsubscribeDepthQuotes(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAUnsubscribeDepthQuotesReq)
        return d

    def test_UnsubscribeLiveTrendbarReq(self):
        """Test UnsubscribeLiveTrendbarReq"""
        data = dict(ctidTraderAccountId=1, period=1, symbolId=1)
        d = self.r.UnsubscribeLiveTrendbar(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAUnsubscribeLiveTrendbarReq)
        return d

    def test_UnsubscribeSpotsReq(self):
        """Test UnsubscribeSpotsReq"""
        data = dict(ctidTraderAccountId=1, symbolId=[1])
        d = self.r.UnsubscribeSpots(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAUnsubscribeSpotsReq)
        return d

    def test_VersionReq(self):
        """Test VersionReq"""
        data = dict()
        d = self.r.Version(**data)
        d.addCallback(self._assertRequest, data)
        d.callback(pb.ProtoOAVersionReq)
        return d

