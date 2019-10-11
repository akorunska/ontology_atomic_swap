from punica.invoke.invoke_contract import Invoke
from punica.test.test import Test
from ontology.utils.util import parse_neo_vm_contract_return_type_integer, parse_neo_vm_contract_return_type_string
import WalletWrapper
import SdkUtils
from Utils import GetDeployedContractAddress, FormatOntIdParam


gas_limit = SdkUtils.g_gasLimit
gas_price = 0
abi_path = './contracts/build/AtomicSwapExchange_abi.json'
contract_address = bytes.fromhex(GetDeployedContractAddress("AtomicSwapExchange"))
abi_info = Test.get_abi_info(abi_path)
alice = WalletWrapper.Alice()
aliceAddress = WalletWrapper.AliceAddress()

def initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, initiator=aliceAddress):
    preExec = False
    params = dict()
    params["amountOfOntToSell"] = amountOfOntToSell
    params["amountOfEthToBuy"] = amountOfEthToBuy
    params["hashlock"] = "String:" + hashlock
    params["initiator"] = "ByteArray:" + initiator
    abiFunction = Invoke.get_function(params, 'intiate_order', abi_info)
    return SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)

def get_amount_of_ont_to_sell(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "String:" + hashlock
    abiFunction = Invoke.get_function(params, 'get_amount_of_ont_to_sell', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return parse_neo_vm_contract_return_type_integer(responce)
    
def get_amount_of_eth_to_buy(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "String:" + hashlock
    abiFunction = Invoke.get_function(params, 'get_amount_of_eth_to_buy', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return parse_neo_vm_contract_return_type_integer(responce)

def get_hashlock(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "String:" + hashlock
    abiFunction = Invoke.get_function(params, 'get_hashlock', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return parse_neo_vm_contract_return_type_string(responce)

# def get_orders():
#     preExec = True
#     params = dict()
#     abiFunction = Invoke.get_function(params, 'get_orders', abi_info)
#     responce = SdkUtils.SendTransaction()
#     return responce


