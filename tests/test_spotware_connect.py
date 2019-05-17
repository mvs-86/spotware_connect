#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `spotware_connect` package."""

from twisted.trial import unittest
from twisted.test import proto_helpers
from spotware_connect.protocol.protocol import SpotwareConnectClientFactory
from spotware_connect.protocol.handler import AppAuthHandler, MarketDataHandler
# import unittest
# from click.testing import CliRunner

# from spotware_connect import spotware_connect
# from spotware_connect import cli


class Testspotware_connect(unittest.TestCase):
    """Tests for `spotware_connect` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        # self.app = AppAuthHandler('123', '123', 'ABC', 'TestAppAuth')
        factory = SpotwareConnectClientFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        # print("===--- ", self.tr.io.read())

    def tearDown(self):
        """Tear down test fixtures, if any."""


    def test_000_transmitProtoOAApplicationAuthReq(self):
        """Test something."""
        app = AppAuthHandler('123', '123', 'ABC')
        app.client = self.proto.factory
        app.handleConnected()
        self.assertEqual(self.tr.value(), "proto")


    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     assert 'spotware_connect.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
