#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import AtomicSwapExchangeWrapper
import SdkUtils
import random
import string
import time


def randomString(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return str(time.time()) + ''.join(random.choice(letters) for i in range(stringLength))


class TestCompiler(unittest.TestCase):
    def test_initiate_order_new_hashlock(self):
        hashlock = randomString()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        try:
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        except Exception as e:
            self.fail(e)

    def test_initiate_order_existing_hashlock(self):
        hashlock = randomString()
        amountOfOntToSellInitial = 100
        amountOfEthToBuyInitial = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, hashlock)
        SdkUtils.WaitNextBlock()
        amountOfOntToSellUpdated = 200
        amountOfEthToBuyUpdated = 3
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellUpdated, amountOfEthToBuyUpdated, hashlock)

    def test_initiate_order_data_is_saved(self):
        hashlock = randomString()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        savedAmountOfOntToSell = AtomicSwapExchangeWrapper.get_amount_of_ont_to_sell(hashlock)
        savedAmountOfEthToBuy = AtomicSwapExchangeWrapper.get_amount_of_eth_to_buy(hashlock)
        print(savedAmountOfOntToSell)
        print(savedAmountOfEthToBuy)
        self.assertEqual(savedAmountOfOntToSell, amountOfOntToSell)
        self.assertEqual(savedAmountOfEthToBuy, amountOfEthToBuy)


if __name__ == '__main__':
    unittest.main()
