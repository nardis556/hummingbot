#!/usr/bin/env python
from os.path import join, realpath
import sys; sys.path.insert(0, realpath(join(__file__, "../../../../../")))
import asyncio
import logging
import unittest
import os

import hummingbot.connector.exchange.idex.idex_resolve

from hummingbot.connector.exchange.idex.idex_user_stream_tracker import IdexUserStreamTracker
from hummingbot.connector.exchange.idex.idex_auth import IdexAuth
from hummingbot.core.utils.async_utils import safe_ensure_future

import conf


"""
To run this integration test before the idex connector is initialized you must set environment variables for API key,
API secret and ETH Wallet. Example in bash (these are not real api key and address, substitute your own):

export IDEX_API_KEY='d88c5070-42ea-435f-ba26-8cb82064a972'
export IDEX_API_SECRET_KEY='pLrUpy53o8enXTAHkOqsH8pLpQVMQ47p'
export IDEX_WALLET_PRIVATE_KEY='ad10037142dc378b3f004bbb4803e24984b8d92969ec9407efb56a0135661576'
export IDEX_DOMAIN='sandbox_matic'
"""


# force resolution of api base url for conf values provided to this test
hummingbot.connector.exchange.idex.idex_resolve._IS_IDEX_SANDBOX = True
hummingbot.connector.exchange.idex.idex_resolve._IDEX_BLOCKCHAIN = 'ETH'


class IdexUserStreamTrackerUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()

        api_key = (
            getattr(conf, 'idex_sandbox_matic_api_key', None) or getattr(conf, 'idex_api_key', None) or
            os.environ.get('IDEX_API_KEY', '--not-set--')
        )
        secret_key = (
            getattr(conf, 'idex_sandbox_matic_api_secret_key', None) or getattr(conf, 'idex_api_secret_key', None) or
            os.environ.get('IDEX_API_SECRET_KEY', '--not-set--')
        )
        wallet_private_key = (
            getattr(conf, 'idex_sandbox_matic_wallet_private_key', None) or
            getattr(conf, 'idex_wallet_private_key', None) or os.environ.get('IDEX_WALLET_PRIVATE_KEY', '--not-set--')
        )
        domain = (
            'sandbox_matic' if getattr(conf, 'idex_sandbox_matic_api_key', None) else
            os.environ.get('IDEX_DOMAIN', 'matic')
        )

        cls.idex_auth = IdexAuth(
            api_key=api_key, secret_key=secret_key, wallet_private_key=wallet_private_key, domain=domain
        )

        cls.user_stream_tracker: IdexUserStreamTracker = IdexUserStreamTracker(
            idex_auth=cls.idex_auth, trading_pairs=['DIL-ETH'], domain=domain
        )
        cls.user_stream_tracker_task: asyncio.Task = safe_ensure_future(cls.user_stream_tracker.start())

    def run_async(self, task):
        return self.ev_loop.run_until_complete(task)

    def test_user_stream(self):
        self.ev_loop.run_until_complete(asyncio.sleep(20.0))
        print(self.user_stream_tracker.user_stream)


def main():
    logging.basicConfig(level=logging.INFO)
    unittest.main()


if __name__ == "__main__":
    main()
