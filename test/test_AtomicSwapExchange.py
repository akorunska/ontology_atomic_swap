#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import AtomicSwapExchangeWrapper
import WalletWrapper
import SdkUtils
import random
import string
import time
from ontology.util import Address
import hashlib

addr = Address(bytes.fromhex('8f651d459b4f146380dab28e7cfb9d4bb9c3fcd1'))


def randomSecret(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return bytes(str(time.time()) + ''.join(random.choice(letters) for i in range(stringLength)), 'utf-8')

def getHashlock(secret):
    m = hashlib.sha256()
    m.update(secret)
    return m.digest()


class TestCompiler(unittest.TestCase):
    def test_initiate_order_new_hashlock(self):
        hashlock = randomSecret()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        try:
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        except Exception as e:
            self.fail(e)

    def test_initiate_order_as_other_user(self):
        hashlock = randomSecret()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, initiator=WalletWrapper.BobAddress())

    def test_initiate_order_existing_hashlock(self):
        hashlock = randomSecret()
        amountOfOntToSellInitial = 100
        amountOfEthToBuyInitial = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, hashlock)
        SdkUtils.WaitNextBlock()
        amountOfOntToSellUpdated = 200
        amountOfEthToBuyUpdated = 3
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellUpdated, amountOfEthToBuyUpdated, hashlock)

    def test_initiate_order_data_is_saved(self):
        hashlock = randomSecret()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        initiator = WalletWrapper.AliceAddress()
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        savedAmountOfOntToSell = AtomicSwapExchangeWrapper.get_amount_of_ont_to_sell(hashlock)
        savedAmountOfEthToBuy = AtomicSwapExchangeWrapper.get_amount_of_eth_to_buy(hashlock)
        savedHashlock = AtomicSwapExchangeWrapper.get_hashlock(hashlock)

        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_initiator(hashlock)))
        savedInitiator = savedAddress.b58encode()

        self.assertEqual(savedAmountOfOntToSell, amountOfOntToSell)
        self.assertEqual(savedAmountOfEthToBuy, amountOfEthToBuy)
        self.assertEqual(savedHashlock, hashlock)
        self.assertEqual(savedInitiator, initiator)

    def test_claim_correct_hashlock(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret)
        self.assertTrue(len(txHash))

    def test_claim_correct_hashlock_claim_twice(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret)
        self.assertTrue(len(txHash))

        SdkUtils.WaitNextBlock()
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.claim(hashlock, secret)


    def test_claim_wrong_secret(self):
        secret = randomSecret()
        hashlock = getHashlock(getHashlock(secret)) + b"blah"
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.claim(hashlock, secret)


if __name__ == '__main__':
    unittest.main()
