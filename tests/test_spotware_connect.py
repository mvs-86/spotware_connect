#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `spotware_connect` package."""

import unittest
import configparser
from twisted.internet import reactor, defer
from twisted.python import failure
from twisted.application import service
from spotware_connect import requests, bot, botutils, protobuf as pb
from spotware_connect.messages import OpenApiVersion


class Testspotware_connect(unittest.TestCase):
    """Tests for `spotware_connect` package."""

    _timeout = 10
    cfg = None

    def _stop(self, *args, **kwargs):
        if reactor.running:
            reactor.stop()
            self.fail("Reactor running exceeded timeout of %s sec" % (self._timeout))

    def setUp(self):
        """Set up test fixtures, if any."""

        if not self.cfg:
            self.cfg = configparser.ConfigParser()
            self.cfg.read('test_credentials.ini')
            self.client_id = self.cfg.get('app', 'client_id')
            self.client_secret = self.cfg.get('app', 'client_secret')
            self.access_token = self.cfg.get('app', 'access_token')

        if not self.client_id or not self.client_secret or not self.access_token:
            self.fail("You need to provide the credentials in ./tests_credentials.ini")

        reactor.callLater(self._timeout, self._stop)


    def tearDown(self):
        """Tear down test fixtures, if any."""
        self._stop()


    def test_connect_api(self):
        """Test basic basic Open Api functions"""

        class TestBot(bot.AccountBot):
            name = "TestBot"

            def Started(self, sender):
                super().Started(sender)

            def ApplicationAuthRes(self, payload):
                super().ApplicationAuthRes(payload)
                self.app_res = payload
                self.r.Version()

            def AccountAuthRes(self, payload):
                super().AccountAuthRes(payload)
                self.auth_res = payload
                reactor.stop()

            def VersionRes(self, payload):
                self.ver_res = payload


        test_bot = TestBot(self.access_token)
        test_bot.d.addCallback(self._stop)
        application = service.Application("Test Spotware Connect Api")
        s = test_bot.createService(self.client_id, self.client_secret, app=application)

        s.startService()
        reactor.run()

        self.assertIsInstance(test_bot.r, requests.Requests)
        self.assertIsNotNone(test_bot.r.reqSendFunc)
        self.assertIsInstance(test_bot.app_res, pb.ProtoOAApplicationAuthRes)
        self.assertIsInstance(test_bot.auth_res, pb.ProtoOAAccountAuthRes)
        self.assertIsInstance(test_bot.ver_res, pb.ProtoOAVersionRes)
