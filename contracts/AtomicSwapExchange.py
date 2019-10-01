# from ontology.interop.System.Runtime import GetTime, CheckWitness, Log, Notify, Serialize, Deserialize
from ontology.interop.System.Storage import Put, Get, GetContext
from ontology.builtins import *
from LibUtils.ContractUtils import ConcatKey, Revert

context = GetContext()

HASH = 'Hash'
ONT_TO_SELL =  'OntToSell'
ETH_TO_BUY = 'EthToBuy'


def Main(operation, args):
    if operation == 'intiate_order':
        ont_to_sell = args[0]
        eth_to_buy = args[1]
        hashlock = args[2]
        return intiate_order(ont_to_sell, eth_to_buy, hashlock)


def intiate_order(ont_to_sell, eth_to_buy, hashlock):
    exchange_id = hashlock
    if len(Get(context, ConcatKey(exchange_id, HASH))) != 0:
        Revert()
    Put(context, ConcatKey(exchange_id, HASH), hashlock)
    
    