from punica.invoke.invoke_contract import Invoke
from punica.test.test import Test
from ontology.utils.util import parse_neo_vm_contract_return_type_integer, parse_neo_vm_contract_return_type_string, parse_neo_vm_contract_return_type_bytearray
import WalletWrapper
import SdkUtils
from Utils import GetDeployedContractAddress, FormatOntIdParam
import codecs


gas_limit = SdkUtils.g_gasLimit
gas_price = 0
abi_path = './contracts/build/AtomicSwapExchange_abi.json'
contract_address = bytes.fromhex(GetDeployedContractAddress("AtomicSwapExchange"))
abi_info = Test.get_abi_info(abi_path)
alice = WalletWrapper.Alice()
aliceAddress = WalletWrapper.AliceAddress()

def to_hex(str_to_convert):
    return codecs.encode(bytes(str_to_convert, 'utf-8'), 'hex').decode('ascii')

def initiate_order(amountOfOntToSell, amountOfEthToBuy, hashlock, initiator=aliceAddress):
    preExec = False
    params = dict()
    params["amountOfOntToSell"] = amountOfOntToSell
    params["amountOfEthToBuy"] = amountOfEthToBuy
    params["hashlock"] = "Hex:" + hashlock.hex()
    params["initiator"] = "ByteArray:" + initiator
    abiFunction = Invoke.get_function(params, 'intiate_order', abi_info)
    return SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)

def get_amount_of_ont_to_sell(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "Hex:" + hashlock.hex()

    abiFunction = Invoke.get_function(params, 'get_amount_of_ont_to_sell', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return parse_neo_vm_contract_return_type_integer(responce)
    
def get_amount_of_eth_to_buy(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "Hex:" + hashlock.hex()

    abiFunction = Invoke.get_function(params, 'get_amount_of_eth_to_buy', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return parse_neo_vm_contract_return_type_integer(responce)

def get_hashlock(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "Hex:" + hashlock.hex()

    abiFunction = Invoke.get_function(params, 'get_hashlock', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return bytes(parse_neo_vm_contract_return_type_string(responce), 'utf-8')

def get_initiator(hashlock):
    preExec = True
    params = dict()
    params["order_id"] = "Hex:" + hashlock.hex()

    abiFunction = Invoke.get_function(params, 'get_initiator', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return responce

def claim(hashlock, secret):
    preExec = False
    params = dict()
    params["order_id"] = "Hex:" + hashlock.hex()
    params["secret"] = "Hex:" + secret.hex()
    abiFunction = Invoke.get_function(params, 'claim', abi_info)
    responce = SdkUtils.SendTransaction(contract_address, alice, alice, gas_limit, gas_price, abiFunction, preExec)
    return responce


