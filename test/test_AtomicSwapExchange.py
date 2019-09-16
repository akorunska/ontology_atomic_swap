#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import AtomicSwapExchangeWrapper
import SdkUtils


class TestCompiler(unittest.TestCase):
    def test_initiate_order_new_hashlock(self):
        hashlock = "lock"
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)

    def test_initiate_order_existing_hashlock(self):
        hashlock = "lock1"
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)

    # def test_initiate_order_data_is_saved(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
