
import re
import itertools as it
from datetime import datetime, timedelta
from twisted.internet import defer, task
from spotware_connect import protobuf as pb

class SymbolsMixin(object):

    @defer.inlineCallbacks
    def loadSymbols(self, ctid, pattern="*", fields=('digits', 'pipPosition', 'swapLong', 'swapShort')):
        payload = yield self.r.SymbolsList(ctid)

        symbols = {s.symbolId: pb.to_dict(s) for s in payload.symbol if re.match(pattern, s.symbolName)}
        payload = yield self.r.SymbolById(ctid, symbols.keys())

        for s in payload.symbol:
            data = pb.to_dict(s, fields)
            symbols[s.symbolId].update(data)

        return symbols


class TrendBarsMixin(object):
    M5_MAX_ALLOWED = 302400000
    H1_MAX_ALLOWED = 21168000000
    D1_MAX_ALLOWED = 31622400000
    MN1_MAX_ALLOWED = 158112000000
    TB_MAX_ALLOWED = dict(M1=M5_MAX_ALLOWED, M2=M5_MAX_ALLOWED, M3=M5_MAX_ALLOWED,
                        M4=M5_MAX_ALLOWED, M5=M5_MAX_ALLOWED, M10=H1_MAX_ALLOWED, M15=H1_MAX_ALLOWED,
                        M30=H1_MAX_ALLOWED, H1=H1_MAX_ALLOWED, H4=D1_MAX_ALLOWED, H12=D1_MAX_ALLOWED,
                        D1=D1_MAX_ALLOWED, W1=MN1_MAX_ALLOWED, MN1=MN1_MAX_ALLOWED)

    @defer.inlineCallbacks
    def loadTrendBars(self, ctid, symbolIds, period, dateBegin, dateEnd=None):
        dateEnd = dateEnd if dateEnd else datetime.now()
        startTime = int(dateBegin.timestamp() * 1000)
        endTime = int(dateEnd.timestamp() * 1000)
        maxAllowed = TrendBarsMixin.TB_MAX_ALLOWED[period]
        batchs = int((endTime - startTime) / maxAllowed) + 1

        bars = []
        for i in range(batchs):
            fromTime = startTime + i * maxAllowed
            toTime = fromTime + maxAllowed - 1
            toTime = endTime if toTime > endTime else toTime

            for sid in symbolIds:
                payload = yield self.r.GetTrendbars(ctid, fromTime, toTime, period, sid)
                bars += [{'symbolId': payload.symbolId, **pb.to_dict(bar)} for bar in payload.trendbar]

        return bars


class TicksMixin(object):

    @defer.inlineCallbacks
    def load_ticks(self, ctid, sids, start_time, end_time, tick_types=[1, 2], max_time=15*60):
        start_timestamp = start_time.timestamp()
        end_timestamp = end_time.timestamp()
        tick_types = tick_types if isinstance(tick_types, list) else [tick_types]

        ticks = []
        batchs = int((end_time - start_time).total_seconds()) // max_time + 1
        for i, bid_or_ask, sid in it.product(range(batchs), tick_types, sids):
            from_time = int(start_timestamp + i * max_time)
            to_time = from_time + max_time
            if to_time > end_timestamp or from_time == to_time:
                continue

            # self.log.info("Get ticks {i} {sid} {bid} {t1},{t2}",
            #     t1=datetime.utcfromtimestamp(from_time),
            #     t2=datetime.utcfromtimestamp((to_time*1000-1)/1000),
            #     i=i, sid=sid, bid=bid_or_ask)
            payload = yield self.r.GetTickData(ctid, sid, bid_or_ask, from_time*1000, to_time*1000-1)

            timestamp = 0
            price = 0
            for data in payload.tickData:
                tick = {'symbolId': sid, 'hasMore': payload.hasMore,
                        'bidOrAsk': bid_or_ask, **pb.to_dict(data)}
                tick['timestamp_real'] = data.timestamp + timestamp
                tick['tick_real'] = data.tick + price
                ticks.append(tick)
                timestamp += data.timestamp
                price += data.tick

        return ticks
