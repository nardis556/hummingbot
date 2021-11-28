import logging
import unittest

from os.path import join, realpath
import sys; sys.path.insert(0, realpath(join(__file__, "../../../../../")))

from hummingbot.connector.exchange.idex.idex_utils import validate_idex_contract_blockchain


class TestUtils(unittest.TestCase):

    def test_validate_idex_contract_blockchain(self):
        self.assertEqual(validate_idex_contract_blockchain("MATIC"), True)
        with self.assertRaises(Exception):
            validate_idex_contract_blockchain("ETH")


def main():
    logging.basicConfig(level=logging.INFO)
    unittest.main()


if __name__ == "__main__":
    main()
