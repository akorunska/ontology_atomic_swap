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


def randomString(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return str(time.time()) + ''.join(random.choice(letters) for i in range(stringLength))

def getHashlock(secret):
    m = hashlib.sha256()
    m.update(bytes(secret, "utf-8"))
    return m.hexdigest()


class TestCompiler(unittest.TestCase):
    # def test_initiate_order_new_hashlock(self):
    #     hashlock = randomString()
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2
    #     try:
    #         AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     except Exception as e:
    #         self.fail(e)

    # def test_initiate_order_as_other_user(self):
    #     hashlock = randomString()
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, initiator=WalletWrapper.BobAddress())

    # def test_initiate_order_existing_hashlock(self):
    #     hashlock = randomString()
    #     amountOfOntToSellInitial = 100
    #     amountOfEthToBuyInitial = 2
    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, hashlock)
    #     SdkUtils.WaitNextBlock()
    #     amountOfOntToSellUpdated = 200
    #     amountOfEthToBuyUpdated = 3
    #     with self.assertRaises(Exception):
    #         AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellUpdated, amountOfEthToBuyUpdated, hashlock)

    # def test_initiate_order_data_is_saved(self):
    #     hashlock = randomString()
    #     amountOfOntToSell = 100
    #     amountOfEthToBuy = 2
    #     initiator = WalletWrapper.AliceAddress()
    #     AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
    #     savedAmountOfOntToSell = AtomicSwapExchangeWrapper.get_amount_of_ont_to_sell(hashlock)
    #     savedAmountOfEthToBuy = AtomicSwapExchangeWrapper.get_amount_of_eth_to_buy(hashlock)
    #     savedHashlock = AtomicSwapExchangeWrapper.get_hashlock(hashlock)

    #     savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_initiator(hashlock)))
    #     savedInitiator = savedAddress.b58encode()

    #     self.assertEqual(savedAmountOfOntToSell, amountOfOntToSell)
    #     self.assertEqual(savedAmountOfEthToBuy, amountOfEthToBuy)
    #     self.assertEqual(savedHashlock, hashlock)
    #     self.assertEqual(savedInitiator, initiator)

    def test_claim_correct_hashlock(self):
        secret = "ttt"
        hashlock = getHashlock(getHashlock(secret))
        print(hashlock)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        print("order created")
        claimResult = AtomicSwapExchangeWrapper.claim(hashlock, secret)
        print(claimResult)
        # self.assertTrue(claimResult)

    def test_claim_correct_hashlock_claim_twice(self):
        secret = randomString()
        hashlock = getHashlock(getHashlock(secret))
        print(hashlock)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        claimResult = AtomicSwapExchangeWrapper.claim(hashlock, secret)
        self.assertTrue(claimResult)
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.claim(hashlock, secret)


    def test_claim_wrong_secret(self):
        secret = randomString()
        hashlock = getHashlock(getHashlock(secret)) + "blah"
        print(hashlock)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.claim(hashlock, secret)


if __name__ == '__main__':
    unittest.main()

# 33663763353435373166616565303234653366643638363033633563393566366134633865663733613339383834306239373466336635373733376131313666
# 3f7c54571faee024e3fd68603c5c95f6a4c8ef73a398840b974f3f57737a116f

# sha256(order_id) > 71e5436fd26a07ad2122644400056f26d53d5eb74d85d8b70dfa02768f135a69
# sha256(sha256(secret)) > 946131dc0564dc9c1eb295d7fdf946939003f230a93710876d8c6bc494f18d6f