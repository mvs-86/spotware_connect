# -*- coding: utf-8 -*-

"""Console script for spotware_connect."""
import sys
import logging
# from spotware_connect.protocol.handler import MarketDataHandler


from twisted.internet import protocol, defer, endpoints, task
from twisted.python import failure
from twisted.logger import Logger

log = Logger()

def main(args=None):
    """Console script for spotware_connect."""
    from twisted.internet import reactor

    logging.root.setLevel(logging.INFO)
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s')

    clientId = "695_vTlnJOeAj5A3dR3VvRpHGxa2WfCrOGTG8lbakzin8hywVtrCw2"
    secret = "TG9kCqh1Sc0WWOYVvBF2nL7rczSUp7Lkc93Yb9nxRZ2UccrptE"
    token = "OhhN97KUYgalpvoMGb15DeitaJCgR6hDQuBS3YUHv6E"

    # f1 = MarketDataHandler.connectApp("One", clientId, secret, token)
    # f2 = protocol.handler.connectApp("Two", clientId, secret, token)
    reactor.run()


@defer.inlineCallbacks
def test(reactor2, clientId="", password="",
         strport="ssl:demo.ctraderapi.com:5035"):
    import spotware_connect.client as client
    from twisted.logger import globalLogPublisher, STDLibLogObserver
    logging.root.setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
    globalLogPublisher.addObserver(STDLibLogObserver())
    # endpoint = endpoints.clientFromString(reactor2, strport)
    # factory = protocol.Factory.forProtocol(sc.client.ConnectClient)
    # try:
    #     client = yield endpoint.connect(factory)
    #     # yield client.login(username, password)
    #     # yield client.select('INBOX')
    #     # info = yield client.fetchEnvelope(imap4.MessageSet(1))
    #     # print('First message subject:', info[1]['ENVELOPE'][1])
    # except:
    #     print("IMAP4 client interaction failed")
    #     failure.Failure().printTraceback()
    import time
    try:
        # client = yield client.connect(reactor2, sc.client.ConnectClient)
        client = yield client.ConnectClient.connect(reactor2)
        # yield client.VersionReq()
        # client.totalSent = 0
        # client.total = 0

        def request():
            import random
            calls = 67 #random.randint(1, 10)
            log.info("Sending {calls} requests", calls=calls)
            for i in range(calls):
                t = 0 #random.randint(0,5)
                reactor2.callLater(.1*t, client.VersionReq)
            client.totalSent += calls

        def calculateTotal(self, payload, msgid):
            self.total = self.total + 1 if hasattr(self, "total") else 0

        # client.VersionRes = calculateTotal

        # d = client.VersionReq()
        # d.addCallback(lambda)

        # loop = task.LoopingCall(request)
        # log.info("Started calls")
        # loop.start(1)
        # request()
        yield client.wait(2)
        # loop.stop()
        # log.info("Stopped calls")
        # log.info("Sent {calls} requests", calls=client.totalSent)
        # log.info("Received a total of {calls} requests", calls=client.total)
    except:
        log.error("Client interaction failed")
        failure.Failure().printTraceback()

def main2():
    task.react(test)

if __name__ == "__main__":
    sys.exit(main2())  # pragma: no cover
