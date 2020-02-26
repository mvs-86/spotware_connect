#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `spotware_connect` package."""

import unittest
import spotware_connect as sc


class Testspotware_connect(unittest.TestCase):
    """Tests for `spotware_connect` package."""

    _timeout = 5

    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_connect_api(self):
        """Test basic basic Open Api functions"""
        c = sc.Client()
        self.version = ""

        @c.event
        def connect():
            c.emit("VersionReq")

        @c.message(msgtype="VersionRes")
        def version(version, **kargs):
            self.version = version
            c.stop()

        @c.event
        def disconnect():
            pass

        def receive_heartbeat(protocol):
            from spotware_connect.messages.OpenApiCommonMessages_pb2 \
                import ProtoMessage, ProtoHeartbeatEvent

            payload = ProtoHeartbeatEvent()
            msg = ProtoMessage(payloadType=payload.payloadType,
                               payload=payload.SerializeToString())
            protocol.stringReceived(msg.SerializeToString())

        c.whenConnected().addCallback(receive_heartbeat)
        c.start(timeout=self._timeout)
        self.assertEqual(self.version, "66")
