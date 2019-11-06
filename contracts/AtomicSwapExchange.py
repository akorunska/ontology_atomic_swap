# from ontology.interop.System.Runtime import Deserialize
from ontology.interop.System.Storage import Put, Get, GetContext
from ontology.builtins import *
from LibUtils.ContractUtils import ConcatKey, Revert, Require, WitnessRequire
from boa.interop.System.Runtime import  GetTime

context = GetContext()

ONT_ADDRESS = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')

HASH = 'Hash'
ONT_TO_SELL =  'OntToSell'
ETH_TO_BUY = 'EthToBuy'
INITIATOR = "Initiator"
CLAIMED = "Claimed"
BUYER = "Buyer"
REFUND_TIMELOCK = "RefundTimelock"

REFUND_TIMELOCK_DURATION = 20

def Main(operation, args):
    if operation == 'intiate_order':
        ont_to_sell = args[0]
        eth_to_buy = args[1]
        hashlock = args[2]
        initiator = args[3]
        return intiate_order(ont_to_sell, eth_to_buy, hashlock, initiator)
    if operation == 'get_amount_of_ont_to_sell':
        hashlock = args[0]
        return get_amount_of_ont_to_sell(hashlock)
    if operation == 'get_amount_of_eth_to_buy':
        hashlock = args[0]
        return get_amount_of_eth_to_buy(hashlock)
    if operation == 'get_hashlock':
        hashlock = args[0]
        return get_hashlock(hashlock)
    if operation == 'get_initiator':
        hashlock = args[0]
        return get_initiator(hashlock)
    if operation == 'set_buyer_address':
        hashlock = args[0]
        buyer = args[1]
        return set_buyer_address(hashlock, buyer)
    if operation == 'get_buyer':
        hashlock = args[0]
        return get_buyer(hashlock)
    if operation == 'get_refund_timelock':
        hashlock = args[0]
        return get_refund_timelock(hashlock)
    if operation == 'refund':
        hashlock = args[0]
        return refund(hashlock)
    if operation == 'claim':
        hashlock = args[0]
        secret = args[1]
        return claim(hashlock, secret)
    if operation == "get_ont_balance":
        return get_ont_balance()


def intiate_order(ont_to_sell, eth_to_buy, hashlock, initiator):
    WitnessRequire(initiator)
    order_id = hashlock
    if len(Get(context, ConcatKey(order_id, HASH))) != 0:
        Revert()
    Put(context, ConcatKey(order_id, HASH), hashlock)
    Put(context, ConcatKey(order_id, ETH_TO_BUY), eth_to_buy)
    Put(context, ConcatKey(order_id, ONT_TO_SELL), ont_to_sell)
    Put(context, ConcatKey(order_id, INITIATOR), initiator)
    Put(context, ConcatKey(order_id, CLAIMED), False)

    transfer_ont(initiator, GetExecutingScriptHash(), ont_to_sell)

def get_amount_of_ont_to_sell(order_id):
    return Get(context, ConcatKey(order_id, ONT_TO_SELL))

def get_amount_of_eth_to_buy(order_id):
    return Get(context, ConcatKey(order_id, ETH_TO_BUY))

def get_hashlock(order_id):
    return Get(context, ConcatKey(order_id, HASH))

def get_initiator(order_id):
    return Get(context, ConcatKey(order_id, INITIATOR))

def set_buyer_address(order_id, buyer):
    saved_initiator = Get(context, ConcatKey(order_id, INITIATOR))
    WitnessRequire(saved_initiator)

    Put(context, ConcatKey(order_id, BUYER), buyer)
    timelock = GetTime() + REFUND_TIMELOCK_DURATION
    Put(context, ConcatKey(order_id, REFUND_TIMELOCK), timelock) 

def get_buyer(order_id):
    return Get(context, ConcatKey(order_id, BUYER))

def get_refund_timelock(order_id):
    timelock = Get(context, ConcatKey(order_id, REFUND_TIMELOCK))
    return timelock if timelock is not None else 0

def refund(order_id):
    saved_initiator = Get(context, ConcatKey(order_id, INITIATOR))
    WitnessRequire(saved_initiator)

    timelock = Get(context, ConcatKey(order_id, REFUND_TIMELOCK))
    if timelock is None:
        timelock = 0
    Require(GetTime() >= timelock)
    ont_to_sell = Get(context, ConcatKey(order_id, ONT_TO_SELL))
    transfer_ont(GetExecutingScriptHash(), saved_initiator, ont_to_sell)
    
def claim(order_id, secret):
    claimed = Get(context, ConcatKey(order_id, CLAIMED))
    if claimed == True:
        Revert()

    hashlock = Get(context, ConcatKey(sha256(secret), HASH))
    if order_id != hashlock:
        Revert()

    saved_buyer = Get(context, ConcatKey(order_id, BUYER))
    WitnessRequire(saved_buyer)

    Put(context, ConcatKey(order_id, CLAIMED), True)
    ont_to_sell = Get(context, ConcatKey(order_id, ONT_TO_SELL))
    transfer_ont(GetExecutingScriptHash(), saved_buyer, ont_to_sell)

def transfer_ont(fromAcct, toAcct, amount):
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONT_ADDRESS, 'transfer', [param])
    return res

def get_ont_balance():
    param = GetExecutingScriptHash()
    return Invoke(0, ONT_ADDRESS, 'balanceOf', param)

    
    