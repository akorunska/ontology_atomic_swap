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


refundTimelockDuration = 20
contractAddress = AtomicSwapExchangeWrapper.contract_address

alice = WalletWrapper.Alice()
aliceAddress = WalletWrapper.AliceAddress()
bob = WalletWrapper.Bob()
bobAddress = WalletWrapper.BobAddress()
eve = WalletWrapper.Eve()
eveAddress = WalletWrapper.EveAddress()

def randomSecret(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase + string.ascii_uppercase
    return bytes(str(time.time()) + ''.join(random.choice(letters) for i in range(stringLength)), 'utf-8')

def getHashlock(secret):
    m = hashlib.sha256()
    m.update(secret)
    return m.digest()

def getONTBalance(address):
    asset = "ONT"
    return SdkUtils.sdk.native_vm().asset().query_balance(asset, address)

class TestAtomicSwapExchange(unittest.TestCase):
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
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, initiator=bobAddress)
        
        # mentioned initiator can still create order
        try:
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        except Exception as e:
            self.fail(e)

    def test_initiate_order_existing_hashlock(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSellInitial = 100
        amountOfEthToBuyInitial = 2
        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, hashlock)
        SdkUtils.WaitNextBlock()
        amountOfOntToSellUpdated = 200
        amountOfEthToBuyUpdated = 3
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellUpdated, amountOfEthToBuyUpdated, hashlock)
        
        # initiating order with non-repeated secret is still possible
        secret = randomSecret()
        newHashlock = getHashlock(secret)
        print(hashlock, newHashlock)
        try:
            AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSellInitial, amountOfEthToBuyInitial, newHashlock)
        except Exception as e:
            self.fail(e)

    def test_initiate_order_data_is_saved(self):
        hashlock = randomSecret()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        initiator = aliceAddress
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

    def test_initiate_order_ont_is_locked(self):
        hashlock = randomSecret()
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        initiator = aliceAddress
        initiatorBalanceBefore = getONTBalance(initiator)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        initiatorBalanceAfter = getONTBalance(initiator)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(initiatorBalanceAfter, initiatorBalanceBefore - amountOfOntToSell)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore + amountOfOntToSell)
        

    def test_set_buyer_address_as_initiator(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        txHash = AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        self.assertTrue(len(txHash))
        
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        self.assertEqual(savedBuyer, buyerAddress)

    def test_set_buyer_address_as_buyer(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)

        SdkUtils.WaitNextBlock()
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_initiator(hashlock)))
        savedInitiator = savedAddress.b58encode()
        buyerAddress = WalletWrapper.BobAddress()
        with self.assertRaises(Exception):
            tx = AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyer=buyerAddress, sender=bob)
        
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        self.assertNotEqual(savedBuyer, buyerAddress)

        # alice still can set buyer address
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyer=buyerAddress, sender=alice)
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        self.assertEqual(savedBuyer, buyerAddress)

    def test_set_buyer_address_as_random_user(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=eve)
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        self.assertNotEqual(savedBuyer, buyerAddress)

        # alice still can set buyer address
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        savedAddress = Address(bytes.fromhex(AtomicSwapExchangeWrapper.get_buyer(hashlock)))
        savedBuyer = savedAddress.b58encode()
        self.assertEqual(savedBuyer, buyerAddress)

    def test_set_buyer_address_refund_timelock_is_set(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, sender=alice)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        refundTimelockBefore = AtomicSwapExchangeWrapper.get_refund_timelock(hashlock)
        timeBefore = time.time()
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        refundTimelockAfter = AtomicSwapExchangeWrapper.get_refund_timelock(hashlock)
        self.assertEqual(refundTimelockBefore, 0)
        self.assertTrue(refundTimelockAfter > timeBefore and refundTimelockAfter < timeBefore + 200)

    def test_claim_correct_hashlock(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)

        buyerBalanceBefore = getONTBalance(buyerAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=bob)
        self.assertTrue(len(txHash))

        buyerBalanceAfter = getONTBalance(buyerAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(buyerBalanceAfter, buyerBalanceBefore + amountOfOntToSell)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore - amountOfOntToSell)

    def test_claim_correct_hashlock_claim_twice(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=bob)
        self.assertTrue(len(txHash))

        buyerBalanceBefore = getONTBalance(buyerAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        SdkUtils.WaitNextBlock()
        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=bob)

        buyerBalanceAfter = getONTBalance(buyerAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(buyerBalanceAfter, buyerBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)


    def test_claim_wrong_secret(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        wrongSecret = secret + b"blah"
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)

        buyerBalanceBefore = getONTBalance(buyerAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.claim(hashlock, wrongSecret, sender=bob)

        buyerBalanceAfter = getONTBalance(buyerAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(buyerBalanceAfter, buyerBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)

        # claim with correct hashlock is not failing
        txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=bob)
        self.assertTrue(len(txHash))

    def test_claim_buyer_not_set(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()

        initiatorBalanceBefore = getONTBalance(aliceAddress)
        eveBalanceBefore = getONTBalance(eveAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        with self.assertRaises(Exception):
            # initiator cannot claim coins
            AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=alice)
        with self.assertRaises(Exception):
            # a random user cannot claim coins
            AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=eve)

        initiatorBalanceAfter = getONTBalance(aliceAddress)
        eveBalanceAfter = getONTBalance(eveAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()

        self.assertEqual(initiatorBalanceAfter, initiatorBalanceBefore)
        self.assertEqual(eveBalanceAfter, eveBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)

        # after setting buyer's address buyer can claim ont
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)

        try:
            AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=bob)
        except Exception as e:
            self.fail(e)

    def test_claim_wrong_buyer_address(self): 
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)

        initiatorBalanceBefore = getONTBalance(aliceAddress)
        eveBalanceBefore = getONTBalance(eveAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        with self.assertRaises(Exception):
            # initiator cannot claim coins
            AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=alice)
        with self.assertRaises(Exception):
            # a random user cannot claim coins
            AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=eve)
        
        initiatorBalanceAfter = getONTBalance(aliceAddress)
        eveBalanceAfter = getONTBalance(eveAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()

        self.assertEqual(initiatorBalanceAfter, initiatorBalanceBefore)
        self.assertEqual(eveBalanceAfter, eveBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)

        # the buyer can claim coins anyway
        try:
            buyerBalanceBefore = getONTBalance(buyerAddress)

            txHash = AtomicSwapExchangeWrapper.claim(hashlock, secret, sender=bob)
            self.assertTrue(len(txHash))

            buyerBalanceAfter = getONTBalance(buyerAddress)
            contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
            self.assertEqual(buyerBalanceAfter, buyerBalanceBefore + amountOfOntToSell)
            self.assertEqual(contractBalanceAfter, contractBalanceBefore - amountOfOntToSell)
        except Exception as e:
            self.fail(e)

    def test_refund_for_initiator_after_locktime(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        initiator = aliceAddress

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        SdkUtils.WaitNextBlock()
        time.sleep(refundTimelockDuration)

        initiatorBalanceBefore = getONTBalance(initiator)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        txHash = AtomicSwapExchangeWrapper.refund(hashlock, sender=alice)
        self.assertTrue(len(txHash))
        
        initiatorBalanceAfter = getONTBalance(initiator)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(initiatorBalanceAfter, initiatorBalanceBefore + amountOfOntToSell)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore - amountOfOntToSell)

    def test_refund_for_initiator_buyer_not_set(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2
        initiator = aliceAddress

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress

        initiatorBalanceBefore = getONTBalance(initiator)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        txHash = AtomicSwapExchangeWrapper.refund(hashlock, sender=alice)
        self.assertTrue(len(txHash))
        
        initiatorBalanceAfter = getONTBalance(initiator)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(initiatorBalanceAfter, initiatorBalanceBefore + amountOfOntToSell)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore - amountOfOntToSell)

    def test_refund_for_initiator_before_locktime(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)

        initiatorBalanceBefore = getONTBalance(aliceAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.refund(hashlock, sender=alice)

        initiatorBalanceAfter = getONTBalance(aliceAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(initiatorBalanceAfter, initiatorBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)

        # after locktime expires initiator can refund ont
        time.sleep(refundTimelockDuration)
        try:
            AtomicSwapExchangeWrapper.refund(hashlock, sender=alice)
        except Exception as e:
            self.fail(e)
    
    def test_refund_for_buyer(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        time.sleep(refundTimelockDuration)

        userBalanceBefore = getONTBalance(buyerAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()

        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.refund(hashlock, sender=bob)

        userBalanceAfter = getONTBalance(buyerAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(userBalanceAfter, userBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)

        # after that initiator can refund ont
        try:
            AtomicSwapExchangeWrapper.refund(hashlock, sender=alice)
        except Exception as e:
            self.fail(e)

    def test_refund_for_random_user(self):
        secret = randomSecret()
        hashlock = getHashlock(secret)
        amountOfOntToSell = 100
        amountOfEthToBuy = 2

        AtomicSwapExchangeWrapper.initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock)
        SdkUtils.WaitNextBlock()
        buyerAddress = bobAddress
        AtomicSwapExchangeWrapper.set_buyer_address(hashlock, buyerAddress, sender=alice)
        time.sleep(refundTimelockDuration)

        userBalanceBefore = getONTBalance(eveAddress)
        contractBalanceAfter = AtomicSwapExchangeWrapper.get_ont_balance()

        with self.assertRaises(Exception):
            AtomicSwapExchangeWrapper.refund(hashlock, sender=eve)

        userBalanceAfter = getONTBalance(eveAddress)
        contractBalanceBefore = AtomicSwapExchangeWrapper.get_ont_balance()
        self.assertEqual(userBalanceAfter, userBalanceBefore)
        self.assertEqual(contractBalanceAfter, contractBalanceBefore)

        # after that initiator can refund ont
        try:
            AtomicSwapExchangeWrapper.refund(hashlock, sender=alice)
        except Exception as e:
            self.fail(e)

if __name__ == '__main__':
    unittest.main()
