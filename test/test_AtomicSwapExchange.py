#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import AtomicSwapExchangeWrapper
import SdkUtils
import random
import string
from datetime import datetime


def randomString(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return str(datetime.now()) + ''.join(random.choice(letters) for i in range(stringLength))


class TestCompiler(unittest.TestCase):
    def test_initiate_order_new_hashlock(self):
        hashlock = randomString()
        print(hashlock)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)

    def test_initiate_order_existing_hashlock(self):
        hashlock = randomString()
        print(hashlock)
        amountOfOntToSellInitial = 100
        amountOfEthToBuyInitial = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, hashlock)
        SdkUtils.WaitNextBlock()
        amountOfOntToSellUpdated = 200
        amountOfEthToBuyUpdated = 3
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellUpdated, amountOfEthToBuyUpdated, hashlock)

    def test_initiate_order_data_is_saved(self):
        self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()
